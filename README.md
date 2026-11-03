# NovelAI Scripting Skill

A comprehensive **AI agent skill** for writing, debugging, and reviewing [NovelAI](https://novelai.net) User Scripts. It gives your coding agent the full NovelAI scripting API reference, TypeScript guidelines tuned for the Web Worker runtime, UI component patterns, theme tokens, model context limits, and more.

> [!IMPORTANT]
> This skill relies on the `references/` subdirectory — the agent reads `SKILL.md` as an entry point and then follows links into the reference files as needed. **Your agent must support multi-file skills** (a skill folder with subdirectories, not just a single flat file). If your agent only supports a single-file skill or instruction document, this skill won't work correctly.

## What's Included

```
novel-ai-scripting/
├── SKILL.md                              Entry point: architecture, API map, TypeScript rules,
│                                         script header/config, styling, model table
├── CHANGELOG.md                          Every correction, with how it was verified
└── references/
    ├── NovelAI_Scripting_API_Complete_Documentation.md   Full api.v1 reference
    ├── NovelAI_TYPESCRIPT_GUIDELINES.md                  Pitfalls & checklist for the Web Worker compiler
    ├── NovelAI_Text_Generation_Documentation.md          Editor features, models, context settings
    ├── NovelAI_UI_Component_System.md                    Reusable, scalable UI architecture
    ├── NovelAI_JSX_Guide.md                              Preact JSX parts (opt-in)
    ├── NovelAI_Script_Types.d.ts                         Official type definitions (source of truth)
    ├── NovelAI_JSX_Types.d.ts                            Community JSX typings
    ├── NovelAI_Script_Types_Experimental.d.ts            Experimental API types
    └── script_config_examples.ts                         Script header & config examples
```

The skill uses **progressive disclosure**: the agent only reads `SKILL.md` up front (~300 lines), then pulls in the larger reference files as needed, keeping your context window lean.

---

## Installing

A skill is just a folder with a `SKILL.md` in it. Install it by putting the `novel-ai-scripting/` folder in your agent's skills directory. Use the global path to have it in every project, or the project path to keep it to one repo:

| Agent | Global (all projects) | Project only |
| :--- | :--- | :--- |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `.gemini/skills/` |
| OpenAI Codex | `~/.agents/skills/` | `.agents/skills/` |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` |
| VS Code (Copilot) | `~/.copilot/skills/` | `.github/skills/` |

Other agents: check their docs for "Agent Skills" or "SKILL.md". Many also read `.agents/skills/`.

When it's in the right place, the folder looks like this, e.g. for Claude Code:
```
~/.claude/skills/novel-ai-scripting/
├── SKILL.md
├── CHANGELOG.md
└── references/
    └── ...
```

### Option A: Clone the repo (easiest to update)

Clone straight into your skills directory (swap in your agent's path from the table):
```bash
git clone https://github.com/MidMeantime/nai-scripting-skill.git ~/.claude/skills/novel-ai-scripting
```
```powershell
# Windows (PowerShell)
git clone https://github.com/MidMeantime/nai-scripting-skill.git "$HOME\.claude\skills\novel-ai-scripting"
```

To update later, run `git pull` in that folder.

### Option B: The `skills` CLI

If you have Node.js, the community [`skills` CLI](https://github.com/vercel-labs/skills) can install it for whichever agents it finds on your machine:
```bash
npx skills add MidMeantime/nai-scripting-skill        # this project
npx skills add MidMeantime/nai-scripting-skill -g     # all projects
```

### Option C: Download a release

Grab the latest release from the [Releases page](https://github.com/MidMeantime/nai-scripting-skill/releases):

| File | What it is |
| :--- | :--- |
| `novel-ai-scripting.skill` | Zip that already contains the `novel-ai-scripting/` folder. Upload it directly on claude.ai (Settings → Capabilities → Skills), or extract it into a skills directory. |
| `novel-ai-scripting.zip` | The skill's files with no top folder, for extracting into a folder you name yourself. |

<details>
<summary><strong>Windows (PowerShell)</strong></summary>

```powershell
$skills = "$HOME\.claude\skills"   # your agent's skills directory

# .skill package (already contains the novel-ai-scripting folder)
Copy-Item novel-ai-scripting.skill novel-ai-scripting-skill.zip   # Expand-Archive only accepts .zip
Expand-Archive novel-ai-scripting-skill.zip -DestinationPath $skills

# or the plain .zip
Expand-Archive novel-ai-scripting.zip -DestinationPath "$skills\novel-ai-scripting"
```

</details>

<details>
<summary><strong>macOS / Linux</strong></summary>

```bash
SKILLS=~/.claude/skills   # your agent's skills directory

# .skill package (already contains the novel-ai-scripting folder)
unzip novel-ai-scripting.skill -d "$SKILLS"

# or the plain .zip
unzip novel-ai-scripting.zip -d "$SKILLS/novel-ai-scripting"
```

</details>

---

## Updating

- **Cloned:** `git pull` in the skill folder.
- **`skills` CLI:** `npx skills update`.
- **Downloaded:** grab the latest release and extract it over the old folder (or delete the old folder first, so removed files don't linger).

Check the [CHANGELOG](CHANGELOG.md) for what changed between versions.

---

## Contributing

Contributions, corrections, and additions are welcome! This is a community resource — if you've found an API quirk, a missing type, or a better pattern, please share it.

### What to contribute

- **API corrections:** Found something in the docs that doesn't match NovelAI's actual behavior? Open an issue or PR.
- **New patterns & examples:** Useful UI patterns, generation techniques, or hook recipes that aren't covered yet.
- **Type updates:** When NovelAI updates `script-types.d.ts`, the bundled types should be updated to match.
- **Verified findings:** If you've tested something in NovelAI that's marked "unverified" in the changelog, let us know.

### How to contribute

1. **Fork** this repo and clone your fork.
2. **Create a branch** for your change:
   ```bash
   git checkout -b fix/storage-prefix-docs
   ```
3. **Make your edits.** The key files are:
   - `SKILL.md` — the agent's entry point and quick reference
   - `references/` — the in-depth documentation and types
   - `CHANGELOG.md` — note what changed and how it was verified
4. **Test your changes** by pointing your agent at your local copy. Link your clone into your skills directory (move any installed copy out of the way first):
   ```bash
   ln -s "$(pwd)" ~/.claude/skills/novel-ai-scripting
   ```
   ```powershell
   # Windows: a directory junction needs no admin rights
   New-Item -ItemType Junction -Path "$HOME\.claude\skills\novel-ai-scripting" -Target (Get-Location)
   ```
   Then ask the agent to write or fix a NovelAI script that touches your change, and check it follows the updated guidance.
5. **Open a Pull Request** with a clear description. Include:
   - What was wrong or missing
   - How you verified the fix (ideally tested in NovelAI — note this in the PR)
   - The relevant section/file changed

### Building the packages

`novel-ai-scripting.zip` and `novel-ai-scripting.skill` are built from `SKILL.md`, `CHANGELOG.md`, and `references/`, so don't edit them by hand. A GitHub Action (`.github/workflows/build-packages.yml`) rebuilds and commits them whenever those files change on `main`, attaches them to every published release, and attaches them as a downloadable artifact on pull requests. To build them locally (Python 3.10+):

```bash
python scripts/build_packages.py           # build both packages
python scripts/build_packages.py --check   # exit 1 if the committed packages are out of date
```

Builds are reproducible, so a local build and the Action's build of the same files are byte-identical.

### Guidelines

- **Accuracy over coverage.** Every code example should type-check against the bundled `NovelAI_Script_Types.d.ts`. If it hasn't been verified in NovelAI, mark it as unverified.
- **Keep `SKILL.md` lean.** It's the entry point the agent reads first. Detailed docs belong in `references/`. Link to them from `SKILL.md`.
- **Preserve the changelog.** `CHANGELOG.md` tracks every correction with its verification status. Add entries there so future readers know what was tested.
- **Don't duplicate NovelAI's official docs** word-for-word. Summarize, clarify, and correct — the value is in catching what the official docs get wrong or leave out.

---

## Links

- [NovelAI official script examples](https://github.com/NovelAI/novelai-script-examples)
- NovelAI scripting documentation](https://docs.novelai.net/en/scripting)
- Feedback & questions: [GitHub Issues](https://github.com/MidMeantime/nai-scripting-skill/issues) or the NovelAI Discord
- My other scripts: https://storyscriptvault.com/users/MidMeantime
- Like my work? [buymeacoffee.com/midmeantime](https://buymeacoffee.com/midmeantime)

## License
[MIT](LICENSE)