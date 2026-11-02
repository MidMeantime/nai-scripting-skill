---
name: novel-ai-scripting
description: >-
  Comprehensive guide and reference for NovelAI User Scripts, TypeScript scripting rules,
  API v1 reference, UI extensions, generation hooks, and text generation configuration.
  Use when writing, debugging, refactoring, or reviewing NovelAI scripts, Lorebook integration,
  context building, or NovelAI TypeScript code.
---

# NovelAI Scripting & TypeScript Skill Guide

This skill provides comprehensive instructions, API references, typing rules, and architectural guidelines for developing **NovelAI User Scripts** and interacting with the NovelAI text generation engine.

---

## 1. Quick Reference & Documentation Files

All in-depth documentation and types are located in the `references/` directory:

- [TypeScript Guidelines](./references/NovelAI_TYPESCRIPT_GUIDELINES.md) — Critical rules to avoid runtime crashes in the Web Worker interpreter, typing patterns, event handling, and casting.
- [Scripting API Complete Documentation](./references/NovelAI_Scripting_API_Complete_Documentation.md) — Full reference for all `api.v1` namespaces (Storage, UI, Document, Hooks, Generation, Lorebook, TTS, etc.).
- [Text Generation Documentation](./references/NovelAI_Text_Generation_Documentation.md) — Background on the NovelAI **editor and website features** (models, context settings, samplers, lorebook UI, ATTG, Text Adventure). Rarely needed for script code; consult it when a script has to reason about how the editor builds context or what a setting means.
- [Script Types Definition (`.d.ts`)](./references/NovelAI_Script_Types.d.ts) — The official TypeScript definitions (from `https://novelai.net/scripting/types/script-types.d.ts`). **This is the source of truth for property names and allowed values.** When it disagrees with prose docs, trust the types.
- [JSX Guide](./references/NovelAI_JSX_Guide.md) + [JSX Types](./references/NovelAI_JSX_Types.d.ts) — Preact-based `jsx` UI parts for custom visuals (tables, SVG/canvas charts, live widgets): globals (`h`, `render`, hooks, `createStore`), the element/attribute whitelist, events, canvas, and how to type-check. **Opt-in only: use JSX only when the user explicitly asks for it.** Otherwise build UI from standard parts, even for complex layouts, and at most mention that JSX could help.
- [Experimental Types](./references/NovelAI_Script_Types_Experimental.d.ts) — `api.v1.editor.block()` and `api.v1.document.transaction()`, gated behind the user's `experimentalScriptingApi` setting (see Section 18 of the API docs). Don't use these unless the user says they've enabled it.
- [UI Component System](./references/NovelAI_UI_Component_System.md) — How to build reusable, scalable UI: tokens, style presets, typed component factories, storage-bound fields, render/refresh strategy, reusable dialogs. **Use this as the default structure for any script with UI.**
- [Script Header & Config Example](./references/script_config_examples.ts) — The `/*--- ... ---*/` script header with every config option type (string, multiline string, number, boolean, select).
- Official examples: https://github.com/NovelAI/novelai-script-examples. The *Scripting Demo* scenario and scripts like *Find & Replace*, *Notes*, and *Smart Summarizer* show real-world patterns.

---

## 2. Core Architecture & Runtime Environment

1. **Isolated Web Worker Execution**:
   - Scripts run inside an isolated JavaScript interpreter within a Web Worker.
   - Scripts **cannot** access arbitrary DOM elements or make raw network requests.
   - All interactions with NovelAI occur via the versioned `api.v1` asynchronous interface.
   - The global `setTimeout`/`clearTimeout` are **not** available. Use `await api.v1.timers.setTimeout(...)`, `api.v1.timers.clearTimeout(...)`, and `api.v1.timers.sleep(ms)`.
2. **Scripts Are Transient**:
   - Scripts can be reloaded or unloaded when stories switch, when the User Scripts modal closes, or when toggled.
   - **Never store persistent state in global memory variables.** Always persist state using `api.v1.storage`.
3. **Silent Promise Rejections**:
   - Unhandled rejected promises in the worker do **not** print to the console or UI.
   - **Always** wrap asynchronous calls with `try/catch` or attach `.catch((err) => ...)` handlers.
4. **Emergency Recovery**:
   - If a script causes instability, append `?noscript=true` to the NovelAI URL to disable script execution on load.

---

## 3. Critical TypeScript Guidelines for NovelAI Scripts

The Web Worker interpreter requires clean, strictly annotated TypeScript to avoid compile/runtime errors:

### A. Explicit Parameter Annotations
Always type all parameters in standard functions and arrow callbacks:
```typescript
// ❌ WRONG
function processEntry(id, data) { ... }
items.filter(item => item.active);

// ✅ CORRECT
function processEntry(id: string, data: any): void { ... }
items.filter((item: any) => item.active);
```

### B. Object Iteration Casting
`Object.entries()` and `Object.values()` must be explicitly cast:
```typescript
// ✅ CORRECT
for (const [key, value] of Object.entries(myObj) as [string, any][]) { ... }
for (const val of Object.values(myObj) as any[]) { ... }
```

### C. Undefined Checks on Array Shifts
`Array.prototype.shift()` returns `T | undefined`:
```typescript
// ✅ CORRECT
const item = queue.shift();
if (!item) return;
```

### D. Await Only in Async Contexts
UI builder and helper functions that invoke asynchronous API methods must be `async`:
```typescript
// ✅ CORRECT
async function loadUserData(): Promise<void> {
    const hasData = await api.v1.storage.has('userData');
    if (hasData) {
        const data = await api.v1.storage.get('userData');
    }
}
```

---

## 4. Key API Namespaces (`api.v1`)

| Namespace / Method | Purpose |
| :--- | :--- |
| `api.v1.storage` | Persistent key-value storage: `get`, `getOrDefault`, `set`, `setIfAbsent`, `has`, `remove`, `list` (also `storyStorage`, `historyStorage`, `tempStorage`). |
| `api.v1.hooks` | Register event lifecycle hooks (`onGenerationRequested`, `onBeforeContextBuild`, `onContextBuilt`, `onResponse`, `onGenerationEnd`, `onScriptsLoaded`, `onLorebookEntrySelected`, `onTextAdventureInput`, `onHistoryNavigated`, `onDocumentConvertedToText`). One callback per hook per script; registering again replaces it. |
| `api.v1.ui` | Create UI extensions (`scriptPanel`, `sidebarPanel`, `lorebookPanel`, `toolbarButton`, `contextMenuButton`, `toolboxOption`), modals, windows, toasts; `updateParts()` to change individual parts by `id`. |
| `api.v1.document` | Read and edit the story document by section (paragraph) ID: `scan()`, `sectionIds()`, `textFromSelection()`, `append()`, `appendParagraph(s)()`, `insertParagraph(s)After()`, `updateParagraph(s)()`, `removeParagraph(s)()`, plus `document.history`. |
| `api.v1.editor` | `generate()`, `isBlocked()`, `selection.get()`, and `editor.decorations` (highlights, markers, widgets). |
| `api.v1.memory` / `systemPrompt` / `prefill` | Get or set the story's Memory, System Prompt, and Prefill (setting requires `storyEdit`). |
| `api.v1.generate()` | Execute direct text generation with custom parameters and context. |
| `api.v1.generateWithStory()` | Run generation using the current story context and settings. |
| `api.v1.lorebook` | Query, update, create, or delete Lorebook entries and categories. |
| `api.v1.an` | Get or set the Author's Note text. |
| `api.v1.buildContext()` | Access and inspect context assembly before it is sent to the AI. |
| `api.v1.config` | `await api.v1.config.get('name')` reads a user-configurable value declared in the script header (see below). |
| `api.v1.permissions` | `has()` / `request()` / `list()`. Request `documentEdit`, `storyEdit`, `lorebookEdit`, `editorDecorations`, `clipboardWrite`, `fileInput`, `fileDownload` (and `presetEdit`) before using the gated APIs. |

### Script Header & Config

Every `.naiscript` starts with a YAML header in a `/*--- ... ---*/` comment (`compatibilityVersion: naiscript-1.0`, `id`, `name`, `version`, `author`, `description`, `memoryLimit`, optional `config`). `config` entries (`name`, `prettyName`, `type`, `default`, `description`) appear in the User Scripts modal's Config tab, so users can change them without editing code. Types are `string` (optionally `multiline: true`), `number` (optional `min`/`max`/`decimal`), `boolean`, and `select` (`options: [{ label, value }]`; defaults to the first option). See [script_config_examples.ts](./references/script_config_examples.ts). Read values at runtime with a fallback:

```typescript
const openOnCreate: boolean = (await api.v1.config.get('open_on_create')) ?? true;
```

---

## 5. Standard Script Boilerplate

When creating a new NovelAI script, follow this structure:

```typescript
(async () => {
    try {
        const STORAGE_KEY = "my_custom_script_data";

        // 1. Initialize persistent state
        const state = await api.v1.storage.getOrDefault(STORAGE_KEY, { enabled: true, count: 0 });
        await api.v1.storage.setIfAbsent(STORAGE_KEY, state);

        // 2. Register lifecycle hooks
        // onGenerationRequested runs before context is built; it can only stop generation or prepare state.
        api.v1.hooks.register('onGenerationRequested', async (params: any) => {
            if (!state.enabled) return;
            // Prepare state for later hooks here, or return { stopGeneration: true } to block it
        });

        // To modify what the model sees, use onBeforeContextBuild (memory, lorebook, AN...)
        // or onContextBuilt (return { messages } with the edited message array).
        api.v1.hooks.register('onContextBuilt', async (params: any) => {
            if (!state.enabled || params.dryRun) return;
            return { messages: params.messages };
        });

        // 3. Register UI — always use update(), NOT register()
        api.v1.hooks.register('onScriptsLoaded', async () => {
            await api.v1.ui.update([{
                type: 'sidebarPanel' as const,
                id: 'my-script-panel',
                name: 'Custom Tool',
                content: [
                    { type: 'text' as const, text: `Status: ${state.enabled ? 'Active' : 'Disabled'}` } as any
                ]
            }]);
        });

    } catch (err: any) {
        api.v1.error("Script Initialization Error:", err);
    }
})();
```

---

## 6. Styling, Theme Tokens & Factory Functions

NovelAI scripts run in an isolated Web Worker with **no access to the DOM**. Never use `document.createElement`, `document.head`, `cloneNode`, or any browser API that touches the page directly. All UI is built from declarative **UI Part objects** passed to `api.v1.ui.update()`.

> **Default architecture for any script with UI: follow [NovelAI_UI_Component_System.md](./references/NovelAI_UI_Component_System.md).** It has a reusable, scalable layering that type-checks against the official types:
> 1. Namespace and tokens: `NS` + `id()`, `COLOR` theme-token map, `SPACE`/`RADIUS` constants
> 2. Style presets combined with `sx()`
> 3. Component factories built on `api.v1.ui.part.*` with options objects and variants
> 4. `field()` bindings that keep `storageKey` prefixes and storage APIs in sync
> 5. One `render()`, with `updateParts`/`{{templates}}` for small refreshes
> 6. Reusable `confirm()`/`notify()` dialogs
>
> The snippets below are the minimal version of the same idea. If the user asks for JSX, see [NovelAI_JSX_Guide.md](./references/NovelAI_JSX_Guide.md). JSX styles use normal CSS and `var(--theme-*)`, not token names. Don't switch to JSX on your own initiative.

### Style Object Presets

Define typed style objects at the top of your script and spread them onto UI parts:

```typescript
const CARD_STYLE: Record<string, string> = {
    backgroundColor: 'bg1',      // theme token
    border: '1px solid bg2',     // theme token
    borderRadius: '6px',
    padding: '10px',
    margin: '6px 0',
};

const DANGER_STYLE: Record<string, string> = {
    ...CARD_STYLE,
    borderColor: 'warning',
};

// Apply via spread in a UI Part:
{ type: 'container' as const, style: CARD_STYLE, content: [...] } as any
```

### Theme Tokens

Instead of hardcoding hex colors, use NovelAI theme token strings directly as values in `style` objects. At render time each token is replaced with the user's active theme value as a literal inline value (e.g. `'bg1'` becomes an `rgb(...)` code). These are **not** CSS variables: there are no `--theme-*` custom properties to use with `var()`, and custom CSS elsewhere on the site can't reference them. For raw theme values inside a script, use `api.v1.theme.get()`. (Exception: per the official types, JSX UI parts get `--theme-*` custom properties inside their own shadow DOM.)

| Token | Role |
| :--- | :--- |
| `'bg0'` | Deepest / outermost background |
| `'bg1'` | Default panel background |
| `'bg2'` | Raised surface / border / button background |
| `'bg3'` | Highlighted / selected surface |
| `'textHeadings'` | High-contrast headings and title text |
| `'textMain'` | Default body text |
| `'textDisabled'` | Disabled / muted text |
| `'textPlaceholder'` | Input placeholder text |
| `'textHighlight'` | Search / highlight color |
| `'warning'` | Warning / alert state |
| `'textPrompt'`, `'textUser'`, `'textAI'`, `'textEdit'` | Story text colors |
| `'lowIntensityColor'`, `'midIntensityColor'`, `'highIntensityColor'` | Low/mid/high probability colors (as used by token probabilities) |
| `'default'` | Body font family (use in `fontFamily`) |
| `'headings'` | Headings font family (use in `fontFamily`) |
| `'code'` | Monospace code font family |
| `'field'` | Form / input field font family |

> **⚠️ Note on `'primary'`**: NovelAI does **NOT** have a `'primary'` or `'error'` theme token. Using `color: 'primary'` produces invalid CSS that browsers ignore. For active/highlighted surfaces use `'bg3'`, for high-contrast accents use `'textHeadings'`, or supply explicit hex/rgba color strings (e.g. `'#90caf9'`).

### Factory Functions (Replaces cloneNode / Templates)

Write factory functions at the top of your script that return pre-styled, pre-configured UI Part objects. This avoids repeating inline style objects throughout the script.

```typescript
// Reusable styled button factory
function makeButton(
    text: string,
    onClick: () => Promise<void> | void,
    overrideStyle: Record<string, string> = {}
): any {
    return {
        type: 'button' as const,
        text,
        disabledWhileCallbackRunning: true,
        callback: onClick,
        style: {
            backgroundColor: 'bg2',
            color: 'textHeadings',
            margin: '4px',
            padding: '6px 12px',
            borderRadius: '4px',
            ...overrideStyle,
        }
    } as any;
}

// Reusable card container factory
function makeCard(title: string, children: any[]): any {
    return {
        type: 'container' as const,
        style: CARD_STYLE,
        content: [
            { type: 'text' as const, text: `### ${title}`, markdown: true } as any,
            ...children
        ]
    } as any;
}

// Usage further down in the script:
await api.v1.ui.update([{
    type: 'sidebarPanel' as const,
    id: 'my-panel',
    name: 'Tools',
    content: [
        makeCard('Actions', [
            {
                type: 'row' as const,
                alignment: 'center',
                content: [
                    makeButton('Save', async () => { /* ... */ }),
                    makeButton('Reset', async () => { /* ... */ }, { backgroundColor: 'warning' })
                ]
            } as any
        ])
    ]
}]);
```

> **Key rules:**
> - `row`/`column` `spacing` is a **string** (flex justification: `'start'`, `'center'`, `'end'`, `'space-between'`, `'space-around'`), never a pixel number. `alignment` only accepts `'start'`, `'center'`, or `'end'` (not `'left'`/`'right'`). For gaps between children, use `margin` on the children.
> - The button prop is `disabledWhileCallbackRunning` (with a "d"). The misspelling `disableWhileCallbackRunning` is silently ignored when cast `as any`.
> - Style values are inline styles only: no pseudo-classes (`:hover`) or media queries, and URLs are stripped from style values.
> - Always cast UI Part objects with `type: '...' as const` and `as any` to avoid the worker compiler's union-type errors.
> - Never use `api.v1.ui.register()` for panels — always use `api.v1.ui.update()` (creates-or-updates, survives disable/re-enable cycles).

---

## 7. Model Context & Token Limits (2026 Reference)

| Model | Script model ID | Architecture / Family | Context Size | Rollover Window | Total Max Context |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Xialong** (Opus only) | `xialong-v1` | GLM-4.6 storytelling finetune (355B MoE) | 28,672 tokens | 8,192 tokens | 36,864 tokens |
| **GLM-4.6** (all tiers) | `glm-4-6` | Base instruct MoE (355B) | 28,672 tokens | 8,192 tokens | 36,864 tokens |
| **Kayra** | — (not scriptable) | 13B Finetune | 8,192 tokens | — | 8,192 tokens |
| **Erato** | — (not scriptable) | Llama-3-70B Finetune | 8,192 tokens | — | 8,192 tokens |

*Note for API Generation:* **Default to `glm-4-6`.** It follows instructions very well and works on every tier, so it is the right choice for summaries, extraction, structured/JSON output, and other instruction-style tasks. `xialong-v1` is meant for story prose, not instruction-following, and it is **Opus-only**. Use it for prose output only when the user's story is already set to it (`(await api.v1.generationParameters.get()).model === 'xialong-v1'`), and never upgrade to it on your own. Script generation (and the `onContextBuilt`/`onResponse` hooks) only works with models on the OpenAI-like completions endpoint, so Kayra and Erato cannot be used from `api.v1.generate`. Query limits at runtime with `await api.v1.maxTokens(model)` and `await api.v1.rolloverTokens(model)` instead of hardcoding them.
