# Distribution and package managers

Braids ships as plain Agent Skills plus generated manifests, so most "package managers" here are really plugin marketplaces. Nothing below requires a build step.

## What a user runs today

| Host | Command |
|---|---|
| Claude Code | `claude plugin marketplace add vyas-devgna/braids` then `claude plugin install braids@braids` |
| Codex CLI/desktop | `codex plugin marketplace add https://github.com/vyas-devgna/braids` then `codex plugin add braids@braids --json` |
| Cursor | clone into `~/.cursor/plugins/local/braids` |
| Everything else | `npx github:vyas-devgna/braids <host>` |

The repository root is itself the installable plugin: `skills/` sits at the root and `build_adapters.py --install-root` writes `.claude-plugin/`, `.codex-plugin/` and `.cursor-plugin/` manifests beside it. There is no `dist/` to publish and no second copy of the kernel.

## Cutting a release

1. Bump `braids.json`, `plugin.json` and `package.json` to the same version. `scripts/validate.py` fails if the plugin and package versions disagree; the release workflow additionally fails if the git tag disagrees.
2. Update `CHANGELOG.md`, including anything newly *not* true.
3. Re-run the gates locally — the workflow runs the same ones.
4. Tag `vX.Y.Z` and push. `.github/workflows/release.yml` re-verifies, checks the tag against both manifests, and publishes to npm with provenance.

`NPM_TOKEN` must exist as a repository secret. Without it the publish job fails loudly rather than half-releasing.

## npm

Package name `braids-skill`. It exists to serve `npx braids-skill <host>` for hosts with no plugin system, and to give the skills a versioned artifact. It is not a library: there is no runtime import surface, and `bin` points at a file copier.

The package is ready but not yet present in the npm registry: the first publish requires account 2FA or a granular publish token with 2FA bypass. Until that is configured, `npx github:vyas-devgna/braids <host>` runs the same installer directly from the public repository.

`files` is an allowlist with `__pycache__` and `*.pyc` negated, so the tarball carries only skills, commands, adapters, manifests and the installer — about 100 kB. Brand assets are deliberately excluded; they are repository material and must never enter model context.

## Marketplace submission

> [!IMPORTANT]
> Braids is **not** submitted to any curated marketplace yet, and should not be until the behavioural evidence exists. `docs/22` fails an adapter that claims support it has not demonstrated, and every adapter is currently `experimental`. Submitting now would publish exactly the unevidenced claim the methodology forbids.

The order to follow, from `docs/07`:

1. source repository install (**done**)
2. local plugin installs (**done** — exercised on Claude Code, Codex, OpenCode, Copilot)
3. third-party and community marketplaces
4. official marketplaces, after conformance maturity

Step 3 becomes defensible once the 99-case suite is graded on at least two hosts and the adapters for those hosts reach `tested`. Step 4 additionally needs the `docs/22` per-host minimums.

### When the time comes

- **Claude Code** — community marketplaces take a git URL pointing at a repository containing `.claude-plugin/marketplace.json`. Braids already serves as its own marketplace, so listing is a pull request adding the repository URL to the target marketplace's manifest.
- **Codex** — `codex plugin marketplace add` accepts any git URL, so no submission is required for users to install. Curated listing is separate.
- **Cursor** — publishing goes through `cursor.com/marketplace/publish`. Cursor documents no plugin uninstall contract, so that limitation must be stated in the listing.
- **Copilot** — plugins install from `owner/repo` directly; the `copilot-plugins` and `awesome-copilot` marketplaces are the curated routes.

Do not optimise for marketplace acceptance before behavioural quality is established.
