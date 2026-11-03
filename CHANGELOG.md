# novel-ai-scripting: Changelog

Releases use semantic versioning (`1.0.0`, `1.1.0`, …). "v1" and "v2" below refer to the community docs this skill grew out of: release `1.0.0` is the v2 revision of those docs.

## 1.1.0

### Corrections

- **Border colors don't work inside the `border` shorthand.** 1.0.0 said `border: '1px solid bg2'` was tested and worked. It doesn't apply the token's color. Every example now uses `border: '1px solid'` (or `borderWidth` + `borderStyle`) with the color in its own `borderColor`, and the claim is removed from "Verified in NovelAI" below.

### New Rules

- **Re-rendering (guidelines pitfall 19, rewritten):** never re-render the whole panel from any input's `onChange`. It now covers text, multiline, number, slider, checkbox, and code editor inputs (it used to focus on sliders and number inputs), lists the symptoms (lost focus, dropped keystrokes, reset dropdowns and sections, broken slider callbacks), and adds a "re-render as little as possible" table: templates, then `updateParts()`, then a full `ui.update()` only for structural changes. Also added to the `SKILL.md` key rules.
- **CSS rules** (new subsection in `SKILL.md` §6 and guidelines pitfall 22, plus the component system checklist): border colors in `borderColor` only; every size, spacing, and radius on the 4px/8px grid (multiples of 4 or 8, plus `1px`/`2px`/`6px` half-steps), in px or the equivalent rem values but not mixed; every element comes from a factory or has a named preset and namespaced `id` (standard parts have no `class` prop).
- **Input size checks** (new "Check the Input Size Before Every Generation" in the API docs, and `SKILL.md` §8): measure the prompt with the tokenizer against `maxTokens(model)` minus `max_tokens`, trim on purpose or stop, check the rate-limit budget, and measure early in generation-heavy scripts. Includes a type-checked `fitDocument()`/`summarize()` example.
- **Lorebook entries** (API docs Lorebook section, and `SKILL.md` §8): always set `keys` and `forceActivation` explicitly when creating an entry, so it can't end up silently never activating.

### Build

- **Packages are built automatically.** `scripts/build_packages.py` builds `novel-ai-scripting.zip` (files at the root) and `novel-ai-scripting.skill` (files inside `novel-ai-scripting/`) reproducibly. The `Build skill packages` GitHub Action rebuilds and commits them on pushes to `main`, attaches them to published releases, and uploads them as an artifact on pull requests.

### Example Fixes

- Style examples keep their sizes except for off-grid values: `10px` became `12px` (paddings, the component system's `RADIUS.lg`, a decoration example), and two `5px` values became `4px`. Borders changed as described under Corrections. Font sizes in the component system and pitfall 15 use `12px` instead of `em`, so no example mixes units.
- Pitfall 19's examples use `api.v1.ui.part.*` and type-check.
- Removed two leftovers from a specific project (a script-specific storage key prefix and a version reference in pitfall 21).

## 1.0.0 (2026-10-23): v2, compared with v1

**v1** is the original four-file release from the community thread:
- `NovelAI_TYPESCRIPT_GUIDELINES.md`
- `NovelAI_Scripting_API_Complete_Documentation.md`
- `NovelAI_Text_Generation_Documentation.md`
- `NovelAI_Script_Types.d.ts`

It had no `SKILL.md`. Every comparison below is against those four files.

v2 was checked against all 17 pages of docs.novelai.net/en/scripting, the official `script-types.d.ts`, NovelAI's example repo (github.com/NovelAI/novelai-script-examples), and tests run in NovelAI. Every code example in the skill type-checks under `tsc --strict` against the bundled types.

### At a Glance

| File | v1 → v2 |
| :--- | :--- |
| `SKILL.md` | **New**. Entry point: architecture, TypeScript rules, API map, script header/config, styling and theme tokens, model table, links to every reference |
| `CHANGELOG.md` | **New.** This file |
| `references/NovelAI_TYPESCRIPT_GUIDELINES.md` | 688 → 806 lines (+202 / −84). Pitfalls 7, 8, 10, 13–20 revised; pitfall 22 added |
| `references/NovelAI_Scripting_API_Complete_Documentation.md` | 1761 → 2013 lines (+365 / −113). Many API corrections, a full styling/theme-token section, and Section 18 (Experimental) |
| `references/NovelAI_Script_Types.d.ts` | Replaced with the current official file (+125 / −34) |
| `references/NovelAI_Text_Generation_Documentation.md` | Small changes: scope label, Xialong scripting note, chat-format summary |
| `references/script_config_examples.ts` | **New** (not in v1). Script header with every config option type, plus `api.v1.config.get()` |
| `references/NovelAI_UI_Component_System.md` | **New.** Reusable, scalable UI architecture |
| `references/NovelAI_JSX_Guide.md` | **New.** JSX/Preact parts (opt-in) |
| `references/NovelAI_JSX_Types.d.ts` | **New.** Community-shared JSX typings, made ready for tsc |
| `references/NovelAI_Script_Types_Experimental.d.ts` | **New.** `editor.block()`, `document.transaction()` |

---

### Breaking Corrections (v1 Guidance That Produced Broken Scripts)

- **Storage key prefixes.** An unprefixed `storageKey` / `{{key}}` binds to `api.v1.storage`. Use `temp:`, `story:`, or `history:` for the other storages. v1's pitfall 7 bound inputs with bare keys and then read them back from `tempStorage`. That caused the "input doesn't save" and "ignores `tempStorage.set()`" symptoms.
- **Inputs save as the user types.** v1's pitfall 13 said `storageKey` only saves on Enter. The docs and NovelAI's Find & Replace example say otherwise, and an in-NovelAI test confirmed it.
- **Modal content.** v1's pitfalls 15 and 20 said bare buttons and text-only rows are rejected in modals. They aren't: the official demo uses bare buttons, and a text-only row was tested in NovelAI and works. The real cause of `does not match any of the allowed types` was invalid values such as `alignment: 'left'`, which v1's own example used.
- **`row`/`column` props.** v1 used `spacing: 10` and `alignment: 'left'`. `spacing` takes a string (`'start' | 'center' | 'end' | 'space-between' | 'space-around'`), and `alignment` is `'start' | 'center' | 'end'`.
- **`disabledWhileCallbackRunning`.** v1's button example spelled it `disableWhileCallbackRunning`, which does nothing.
- **Theme token `'textHeading'`** in v1's styling example doesn't exist. The real token is `'textHeadings'`.
- **Missing `await`s.** `ui.modal.open()`, `ui.window.open()`, `timers.setTimeout()`, and `messaging.onMessage()` all return Promises. v1's examples used them without `await`.
- **No global `setTimeout`** in scripts. v1's cancellation example used it; v2 uses `api.v1.timers.setTimeout`.
- **`ui.remove()` takes an array** of IDs, not a single string.
- **Context menu callbacks receive only `{ selection }`.** v1's appendix read a nonexistent `text` argument; v2 uses `document.textFromSelection(selection)`.
- **Rollover helper rewritten.** v1's config used `{ tokenizer, maxTokens }`. The real config is `{ maxTokens, rolloverTokens, model }`, and creation is synchronous. `read()` returns the window without consuming it, `remove(n)` drops the **newest** n items, and `compact()` frees trimmed items. Only `add()` is async.
- **Model choice.** `glm-4-6` is the default for instruction-style work. `xialong-v1` is Opus-only and meant for prose, so use it only when the story is already set to it. v1's example upgraded `glm-4-6` stories to Xialong, which breaks for non-Opus users.
- **Fields that don't exist.** v1's examples used `rows` on `multilineTextInput` and `min`/`max`/`step` on `numberInput`. Neither is in the types.

### `SKILL.md` (new!)

- Runtime rules: Web Worker, no DOM, no global `setTimeout`, transient scripts, silent promise rejections, `?noscript=true`.
- TypeScript rules for the script compiler.
- An `api.v1` map with the real hook and document method names, plus editor, memory/system prompt/prefill, config, and permissions.
- Standard boilerplate: `getOrDefault`/`setIfAbsent`, an `onContextBuilt` example, and `ui.update()` with IDs.
- Script header and config docs.
- Styling: presets, theme tokens substituted as inline values (with the JSX `--theme-*` exception), invalid-token warnings, factory functions, and key rules (row/column values, `disabledWhileCallbackRunning`, inline-style limits).
- A model table with script model IDs, the Opus-only note, and Kayra/Erato marked as not scriptable.
- Links to every reference. It names the types file as the source of truth and the component system as the default for UI, and makes **JSX opt-in** so Claude only uses it when you ask.

### `NovelAI_TYPESCRIPT_GUIDELINES.md`

- **7:** `temp:` prefix fix, plus a prefix explainer.
- **8:** `spacing`/`alignment` values corrected (string spacing; start/center/end).
- **10:** `setTimeout` and `fetch` added to the forbidden list, with the timers API shown.
- **13:** rewritten. Inputs save automatically; read the storage they're bound to.
- **14:** rewritten. Pre-fill through the bound key, or use `initialValue`.
- **15:** rewritten. Modals accept any parts, the validation error means invalid props, and modals must be awaited. v1's Promise + safeResolve pattern is kept.
- **16:** compile against the bundled official types instead of a hand-written stub. This needs ES2022 module/target for top-level `await` (tested). JSX/experimental note added.
- **17, 18:** trimmed to two lines each. They were generic editing advice.
- **19:** `updateParts` and `{{temp:}}` alternatives added, plus a note that `numberInput` passes a string.
- **20:** rewritten as "use valid enum values on layout parts."
- **21 (paste-killer):** unchanged.
- **22:** **new.** Style presets, a full theme-token table (including the `'primary'`/`'error'` warning and the not-CSS-variables note), and factory functions, with a pointer to the component system.
- Checklist and error table: storage prefixes, enum values, the button prop name, awaited modals, and new error rows (prefix mismatch, un-awaited modal).

### `NovelAI_Scripting_API_Complete_Documentation.md`

- **Namespaces:** added `story`, `theme`, `prefill/systemPrompt.getDefault()`, the note that token-budget helpers are synchronous, `hooks.unregister`/`isRegistered`, `ui.openPanel`/`closePanel`/`updateParts`/`removeParts`, the `ui.extension.*` / `ui.part.*` helpers, and `iconId`.
- **Hooks:** `stopGeneration` scope, the `onTextAdventureInput` return shape, and `onHistoryNavigated` params (numeric IDs).
- **Storage:** a prefix table, `historyStorage` generation-node rules, and the `nodeId` argument.
- **UI parts:**
  - Corrected: row/column values, multiline input (no `rows`), number input (no min/max, string values), slider options, `codeEditor` requires `id`, collapsible `initialCollapsed`, button prop name and `iconId`.
  - Modals and windows: modal sizes (incl. `full`) and options, window options, and the "Disable This Script?" behavior.
  - New sections: JSX (opt-in).
- **Styling:** v1 had a single sentence about theme keys. v2 adds the full token table, the `'primary'`/`'error'` warning, inline-style limits (no `:hover`, media queries, or URLs), style presets, and a factory example.
- **Document:** origin/formatting/source enums, a note that section IDs aren't indexes, and the `scan` range.
- **Generation:** model guidance; `logit_bias`, `enable_thinking`, and the response/message shapes; streaming by default; the `generateWithStory` argument order; `editor.isBlocked()`; `buildContext` `forGeneration`; the disabled-sampler note.
- **Lorebook:** entry and category fields, `random` chance from 0 to 100, and duplicate-ID errors.
- **TTS:** the `seed` option, and the fact that `speak()` clears the queue.
- **Utilities:** `random.bool(chance)`, the `roll` breakdown, and `file.prompt` return and encoding notes.
- **Messaging:** channels, filters, and the fact that broadcasts skip the sender.
- **Permissions:** arrays, the message argument, and `presetEdit`.
- **Decorations:** `clearRules`, `scope`, string patterns, event shapes, widget `display`, and a note that the docs page calls the namespace `api.v1.decorations`, while it's really `api.v1.editor.decorations`.
- **Appendix example:** now uses `update()` with IDs, the correct context menu callback, and an awaited setup.
- **New Section 18, Experimental API:** `editor.block()` and `document.transaction()`, gated behind `experimentalScriptingApi`.

### `NovelAI_Script_Types.d.ts`

Replaced with the current official file. The main changes since v1:
- the **`theme` namespace / `theme.get()`** (absent in v1)
- the `UIPartJSX` part with `ui.part.jsx()`
- the `UIPartRegistry` union
- the `presetEdit` permission
- `xialong-v1` mentioned as a model ID
- `historyStorage` generation-node semantics
- lorebook `random` chance from 0 to 100
- `onHistoryNavigated` hook name and numeric IDs
- the disabled-sampler note on `generationParameters.update`

### `NovelAI_Text_Generation_Documentation.md`

- Scope note: this file is editor/website reference, not the scripting API.
- The Xialong scripting note now matches the model guidance (`xialong-v1`, Opus-only, prose). v1 said there was no Xialong ID for scripts.
- v1's "Chat Format: not accessible" note was replaced with a summary of the official guide.

### Other New Files

- **`script_config_examples.ts`:** a script header covering every config type (string, multiline, number, boolean, select), plus a self-contained `readConfig()`/`renderPanel()` example.
- **`NovelAI_UI_Component_System.md`:** namespace and `id()`; `COLOR`/`SPACE`/`RADIUS` tokens; presets combined with `sx()`; `api.v1.ui.part.*` factories with options and variants; `field()` storage bindings; a single `render()` with targeted refreshes; reusable `confirm()`/`notify()`.
- **`NovelAI_JSX_Guide.md`:** mounting, globals, hooks vs. `createStore`, the element whitelist, styling with `var(--theme-<key>)` (confirmed), event snapshots and `captureEvents`, canvas, and type-checking. JSX syntax is confirmed working.
- **`NovelAI_JSX_Types.d.ts`:** the community-shared typings, with `declare` modifiers and a small element-name shim added so tsc accepts them. No change in meaning.
- **`NovelAI_Script_Types_Experimental.d.ts`:** unchanged from the shared file.

### Verified in NovelAI During This Revision

- Inputs bound with `temp:` save without pressing Enter.
- A text-only `row` with a valid `alignment` opens in a modal.
- JSX syntax (`<b>`, `<div><b>…</b></div>`) mounts in a `jsx` part.
- `var(--theme-textHeadings)` applies the heading color inside JSX.
- `xialong-v1` is a valid model ID and is Opus-only.

### Still Unverified

- Whether experimental functions are `undefined` when `experimentalScriptingApi` is off. The feature-detection advice assumes so.
- JSX event handlers probably make a round trip through the worker. This is inferred, not documented.
- `presetEdit` permission: no documented API requires it yet.
