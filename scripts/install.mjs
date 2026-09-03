#!/usr/bin/env node
// Copy the Braids skills into a host's skill directory.
//
// Braids is plain Agent Skills plus manifests, so installing is a file copy.
// Hosts with a real plugin system (Claude Code, Codex, Cursor) should use their
// own marketplace command instead; this exists for the hosts that have none, and
// for anyone who wants the skills in a project without a package manager.
//
// The copy is the easy half. The hard half is never destroying something the
// user wrote. A skill directory is shared ground: `braids-review` in
// `.agents/skills/` may be ours, may be a fork of ours, or may be an unrelated
// skill that happens to share the name. So every write and every delete is
// gated on provenance, recorded in a receipt at `<base>/.braids-install.json`
// and re-checked against on-disk content hashes. Anything we cannot prove we
// installed and that nobody has edited since is left alone and reported.

import { createHash } from "node:crypto";
import {
  cpSync, existsSync, mkdirSync, readdirSync, readFileSync,
  rmSync, statSync, writeFileSync,
} from "node:fs";
import { homedir } from "node:os";
import { dirname, join, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const SKILLS = join(ROOT, "skills");
const RECEIPT = ".braids-install.json";
const RECEIPT_VERSION = 1;

// Where each host reads skills from. Project-relative unless marked user scope.
const TARGETS = {
  "claude-code": { project: ".claude/skills", user: join(homedir(), ".claude/skills") },
  codex: { project: ".agents/skills", user: join(homedir(), ".agents/skills") },
  cursor: { project: ".cursor/skills", user: null },
  antigravity: { project: ".agents/skills", user: null },
  copilot: { project: ".github/skills", user: join(homedir(), ".copilot/skills") },
  opencode: { project: ".opencode/skill", user: join(homedir(), ".config/opencode/skill") },
  cline: { project: ".cline/skills", user: join(homedir(), ".cline/skills") },
  windsurf: { project: ".windsurf/skills", user: join(homedir(), ".codeium/windsurf/skills") },
  agents: { project: ".agents/skills", user: join(homedir(), ".agents/skills") },
};

const KNOWN_FLAGS = new Set(["user", "uninstall", "force", "dry-run", "help"]);

const argv = process.argv.slice(2);
const flags = argv.filter((a) => a.startsWith("--")).map((a) => a.slice(2));
const positional = argv.filter((a) => !a.startsWith("--"));
const flag = (name) => flags.includes(name);

// A mistyped `--uninstal` must not silently become an install.
const unknown = flags.filter((f) => !KNOWN_FLAGS.has(f));

const host = positional[0] ?? "agents";
const scope = flag("user") ? "user" : "project";
const dryRun = flag("dry-run");
const force = flag("force");
// `TARGETS[host]` alone would accept "constructor" and other Object.prototype keys.
const knownHost = Object.hasOwn(TARGETS, host);

function usage() {
  return `braids-skill — copy the Braids skills into a host skill directory

  npx braids-skill <host> [--user] [--uninstall] [--force] [--dry-run]

hosts:   ${Object.keys(TARGETS).join(", ")}
default: agents (the cross-host .agents/skills convention)

  --user       install for the current user instead of this project
  --uninstall  remove skills this installer previously installed
  --force      overwrite or delete a modified or unrecognised skill directory
  --dry-run    report what would change and write nothing

Braids never overwrites or deletes a skill directory it cannot prove it
installed and that nobody has edited since. Those are reported and skipped;
--force overrides, and destroys local edits.

Claude Code, Codex and Cursor have real plugin systems; prefer those:
  claude plugin marketplace add vyas-devgna/braids && claude plugin install braids@braids
  codex plugin marketplace add https://github.com/vyas-devgna/braids && codex plugin add braids@braids --json`;
}

if (unknown.length) {
  console.error(`unknown option${unknown.length > 1 ? "s" : ""}: ${unknown.map((f) => `--${f}`).join(", ")}\n`);
  console.error(usage());
  process.exit(2);
}

if (flag("help") || !knownHost) {
  if (!knownHost && positional.length) console.error(`unknown host: ${positional[0]}\n`);
  console.log(usage());
  process.exit(knownHost || flag("help") ? 0 : 1);
}

if (positional.length > 1) {
  console.error(`expected one host, got: ${positional.join(", ")}`);
  process.exit(2);
}

const base = TARGETS[host][scope];
if (!base) {
  console.error(`${host} has no documented ${scope} skill directory. Try without --user.`);
  process.exit(1);
}

/** Every file under `dir`, as repo-relative POSIX paths, sorted. */
function walk(dir) {
  const out = [];
  const visit = (current) => {
    for (const entry of readdirSync(current, { withFileTypes: true })) {
      const full = join(current, entry.name);
      if (entry.isDirectory()) {
        if (entry.name === "__pycache__") continue;
        visit(full);
      } else if (entry.isFile() && !entry.name.endsWith(".pyc")) {
        out.push(relative(dir, full).split(sep).join("/"));
      }
    }
  };
  visit(dir);
  return out.sort();
}

/** Content hashes for a skill directory: { relativePath: sha256 }. */
function hashTree(dir) {
  const hashes = {};
  for (const file of walk(dir)) {
    hashes[file] = createHash("sha256").update(readFileSync(join(dir, file))).digest("hex");
  }
  return hashes;
}

const sameTree = (a, b) => {
  const keys = Object.keys(a);
  return keys.length === Object.keys(b).length && keys.every((k) => a[k] === b[k]);
};

function readReceipt() {
  const path = join(base, RECEIPT);
  if (!existsSync(path)) return null;
  try {
    const parsed = JSON.parse(readFileSync(path, "utf8"));
    if (parsed?.receiptVersion !== RECEIPT_VERSION || typeof parsed.skills !== "object") return null;
    return parsed;
  } catch {
    return null; // A corrupt receipt proves nothing; fall back to content comparison.
  }
}

/**
 * Decide whether we may write over / delete `<base>/<name>`.
 *
 *   absent      nothing there
 *   ours-clean  we installed it and it is byte-identical to the receipt
 *   identical   no receipt, but it already matches what we would install
 *   modified    we installed it and it has been edited since
 *   foreign     we have no record of it and it is not our content
 */
function classify(name, receipt, sourceHashes) {
  const target = join(base, name);
  if (!existsSync(target)) return { state: "absent" };
  let current;
  try {
    current = hashTree(target);
  } catch (error) {
    return { state: "foreign", detail: `unreadable (${error.code ?? error.message})` };
  }
  const recorded = receipt?.skills?.[name]?.files;
  if (recorded && sameTree(recorded, current)) return { state: "ours-clean", current };
  if (sameTree(sourceHashes, current)) return { state: "identical", current };
  if (recorded) return { state: "modified", current };
  return { state: "foreign", current };
}

const names = existsSync(SKILLS)
  ? readdirSync(SKILLS).filter((n) => existsSync(join(SKILLS, n, "SKILL.md"))).sort()
  : [];
if (names.length === 0) {
  console.error(`no skills found under ${SKILLS}`);
  process.exit(1);
}

const receipt = readReceipt();
const sources = Object.fromEntries(names.map((n) => [n, hashTree(join(SKILLS, n))]));
const say = (line) => console.log(dryRun ? `would ${line}` : line);

// ---------------------------------------------------------------- uninstall
if (flag("uninstall")) {
  let removed = 0;
  const kept = [];
  for (const name of names) {
    const target = join(base, name);
    const { state } = classify(name, receipt, sources[name]);
    if (state === "absent") continue;
    if (state === "modified" && !force) {
      kept.push([name, "edited since Braids installed it"]);
      continue;
    }
    if (state === "foreign" && !force) {
      kept.push([name, "not installed by Braids"]);
      continue;
    }
    if (!dryRun) rmSync(target, { recursive: true, force: true });
    removed += 1;
    say(`remove ${target}`);
  }

  if (receipt && !dryRun) {
    const remaining = Object.fromEntries(
      Object.entries(receipt.skills).filter(([name]) => existsSync(join(base, name))),
    );
    const path = join(base, RECEIPT);
    if (Object.keys(remaining).length === 0) rmSync(path, { force: true });
    else writeFileSync(path, `${JSON.stringify({ ...receipt, skills: remaining }, null, 2)}\n`, "utf8");
  }

  for (const [name, why] of kept) console.log(`kept ${join(base, name)} — ${why}`);
  if (kept.length && !force) {
    console.log(`\n${kept.length} director${kept.length > 1 ? "ies were" : "y was"} left in place. Re-run with --force to delete ${kept.length > 1 ? "them" : "it"} and lose those edits.`);
  }
  console.log(removed ? `\n${dryRun ? "Would remove" : "Removed"} ${removed} skill(s).${dryRun ? "" : ` Restart ${host}.`}` : "\nNothing to remove.");
  process.exit(0);
}

// ------------------------------------------------------------------ install
const planned = [];
const blocked = [];
for (const name of names) {
  const { state } = classify(name, receipt, sources[name]);
  if (state === "modified" && !force) blocked.push([name, "you have edited this copy"]);
  else if (state === "foreign" && !force) blocked.push([name, "a different skill of that name is already here"]);
  else planned.push([name, state]);
}

if (blocked.length && !force) {
  for (const [name, why] of blocked) console.error(`refusing ${join(base, name)} — ${why}`);
  console.error(`\nBraids will not overwrite ${blocked.length > 1 ? "these" : "this"}. Move ${blocked.length > 1 ? "them" : "it"} aside, or re-run with --force to overwrite and lose those edits.`);
  if (planned.length === 0) process.exit(1);
}

if (!dryRun) mkdirSync(base, { recursive: true });
const installed = {};
for (const [name, state] of planned) {
  const target = join(base, name);
  if (!dryRun) {
    if (existsSync(target)) rmSync(target, { recursive: true, force: true });
    cpSync(join(SKILLS, name), target, {
      recursive: true,
      filter: (src) => !src.includes("__pycache__") && !src.endsWith(".pyc"),
    });
  }
  installed[name] = { files: sources[name] };
  if (state === "identical") say(`refresh ${target} (already up to date)`);
  else if (state === "ours-clean") say(`update ${target}`);
  else say(`install ${target}`);
}

if (!dryRun && planned.length) {
  writeFileSync(
    join(base, RECEIPT),
    `${JSON.stringify({
      receiptVersion: RECEIPT_VERSION,
      installedBy: "braids-skill",
      installedAt: new Date().toISOString(),
      skills: { ...(receipt?.skills ?? {}), ...installed },
    }, null, 2)}\n`,
    "utf8",
  );
}

console.log(`\n${dryRun ? "Would install" : "Installed"} ${planned.length} Braids skill(s) to ${base}`);
if (planned.length) console.log(`  ${planned.map(([n]) => n).join(", ")}`);
if (blocked.length) console.log(`  skipped: ${blocked.map(([n]) => n).join(", ")}`);
if (!dryRun) {
  console.log(`\nRestart ${host} to pick them up. Braids is advisory: it ships no hooks and enforces nothing.`);
  if (scope === "project" && existsSync(base) && statSync(base).isDirectory()) {
    console.log("Consider committing this directory so your team gets the same behaviour.");
  }
}
