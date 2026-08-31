#!/usr/bin/env node
// Copy the Braids skills into a host's skill directory.
//
// Braids is plain Agent Skills plus manifests, so installing is a file copy.
// Hosts with a real plugin system (Claude Code, Codex, Cursor) should use their
// own marketplace command instead; this exists for the hosts that have none, and
// for anyone who wants the skills in a project without a package manager.

import { cpSync, existsSync, mkdirSync, readdirSync, rmSync, statSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const SKILLS = join(ROOT, "skills");

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

const args = process.argv.slice(2);
const flag = (name) => args.includes(`--${name}`);
const host = args.find((a) => !a.startsWith("--")) ?? "agents";
const scope = flag("user") ? "user" : "project";

if (flag("help") || !TARGETS[host]) {
  const known = Object.keys(TARGETS).join(", ");
  console.log(`braids-skill — copy the Braids skills into a host skill directory

  npx braids-skill <host> [--user] [--uninstall]

hosts:   ${known}
default: agents (the cross-host .agents/skills convention)

  --user       install for the current user instead of this project
  --uninstall  remove previously installed Braids skills

Claude Code, Codex and Cursor have real plugin systems; prefer those:
  claude plugin marketplace add vyas-devgna/braids && claude plugin install braids@braids
  codex plugin marketplace add https://github.com/vyas-devgna/braids && codex plugin add braids@braids --json`);
  process.exit(TARGETS[host] ? 0 : 1);
}

const base = TARGETS[host][scope];
if (!base) {
  console.error(`${host} has no documented ${scope} skill directory. Try without --user.`);
  process.exit(1);
}

const names = readdirSync(SKILLS).filter((n) => existsSync(join(SKILLS, n, "SKILL.md")));
if (names.length === 0) {
  console.error(`no skills found under ${SKILLS}`);
  process.exit(1);
}

if (flag("uninstall")) {
  let removed = 0;
  for (const name of names) {
    const target = join(base, name);
    if (existsSync(target)) {
      rmSync(target, { recursive: true, force: true });
      removed += 1;
      console.log(`removed ${target}`);
    }
  }
  console.log(removed ? `\nRemoved ${removed} skill(s). Restart ${host}.` : "Nothing to remove.");
  process.exit(0);
}

mkdirSync(base, { recursive: true });
for (const name of names) {
  const target = join(base, name);
  if (existsSync(target)) rmSync(target, { recursive: true, force: true });
  cpSync(join(SKILLS, name), target, {
    recursive: true,
    filter: (src) => !src.includes("__pycache__") && !src.endsWith(".pyc"),
  });
}

console.log(`Installed ${names.length} Braids skills to ${base}`);
console.log(`  ${names.join(", ")}`);
console.log(`\nRestart ${host} to pick them up. Braids is advisory: it ships no hooks and enforces nothing.`);
if (statSync(base).isDirectory() && scope === "project") {
  console.log("Consider committing this directory so your team gets the same behaviour.");
}
