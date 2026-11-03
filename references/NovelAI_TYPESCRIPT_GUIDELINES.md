# TypeScript Guidelines for NovelAI Scripting

## Critical Rules to Avoid Common Errors

### 1. Always Add Type Annotations to Function Parameters

**❌ WRONG:**
```typescript
function getLocation(id) {
    return mapData.locations[id];
}

async function updateLocation(id, updates) {
    // ...
}
```

**✅ CORRECT:**
```typescript
function getLocation(id: string) {
    return mapData.locations[id];
}

async function updateLocation(id: string, updates: any) {
    // ...
}
```

### 2. Add Type Annotations to Arrow Function Parameters

**❌ WRONG:**
```typescript
array.filter(id => id !== targetId)
array.map(item => item.name)
onChange: (value) => { /* ... */ }
```

**✅ CORRECT:**
```typescript
array.filter((id: string) => id !== targetId)
array.map((item: any) => item.name)
onChange: (value: string) => { /* ... */ }
```

### 3. Cast Object.entries() and Object.values() Loops

**❌ WRONG:**
```typescript
for (const loc of Object.values(mapData.locations)) {
    loc.connections = loc.connections.filter(id => id !== targetId);
}

for (const [id, loc] of Object.entries(mapData.locations)) {
    console.log(loc.name);
}
```

**✅ CORRECT:**
```typescript
for (const loc of Object.values(mapData.locations) as any[]) {
    loc.connections = loc.connections.filter((id: string) => id !== targetId);
}

for (const [id, loc] of Object.entries(mapData.locations) as [string, any][]) {
    console.log(loc.name);
}
```

### 4. Handle Array.shift() Undefined Return

**❌ WRONG:**
```typescript
while (queue.length > 0) {
    const currentId = queue.shift();
    const location = getLocation(currentId); // Error: string | undefined
}
```

**✅ CORRECT:**
```typescript
while (queue.length > 0) {
    const currentId = queue.shift();
    if (!currentId) continue;
    const location = getLocation(currentId);
}
```

### 5. Await Only in Async Functions

**❌ WRONG:**
```typescript
function renderView() {
    if (!(await api.v1.storage.has('key'))) {
        // ...
    }
}
```

**✅ CORRECT:**
```typescript
async function renderView(): Promise<any[]> {
    if (!(await api.v1.storage.has('key'))) {
        // ...
    }
}

// And update call sites:
content.push(...await renderView());
```

### 6. Handle Storage Get() Undefined Returns

**❌ WRONG:**
```typescript
const name = await api.v1.tempStorage.get('key');
await createLocation(name, description); // Error: string | undefined
```

**✅ CORRECT:**
```typescript
const name = await api.v1.tempStorage.get('key') as string | undefined;

if (!name || !name.trim()) {
    api.v1.ui.toast('Name is required', { type: 'error' });
    return;
}

await createLocation(name.trim(), description || '');
```

### 7. Use StorageKey Instead of Value for Text Inputs

**❌ WRONG (causes glitching/infinite loops):**
```typescript
{
    type: 'textInput',
    value: location.name,
    onChange: async (value: string) => {
        await updateLocation(location.id, { name: value });
        await saveMap();
        await updateUI(); // This reloads the form = glitch!
    }
}
```

**✅ CORRECT:**
```typescript
// Initialize storage first
const nameKey = `edit_name_${location.id}`;
if (!(await api.v1.tempStorage.has(nameKey))) {
    await api.v1.tempStorage.set(nameKey, location.name);
}

// Then bind the input to it. The "temp:" prefix is what points storageKey at tempStorage.
{
    type: 'textInput' as const,
    storageKey: `temp:${nameKey}`,
    onSubmit: async (value: string) => {
        if (value?.trim()) {
            await updateLocation(location.id, { name: value.trim() });
        }
    }
} as any
```

**⚠️ storageKey prefixes decide WHICH storage is bound.** An unprefixed `storageKey` (and an unprefixed `{{key}}` text template) reads and writes `api.v1.storage`. Use `story:key` for `api.v1.storyStorage`, `history:key` for `api.v1.historyStorage`, and `temp:key` for `api.v1.tempStorage`. The prefix is only used in the UI part; in code you call the matching API with the bare key (`api.v1.tempStorage.get(nameKey)`). A mismatch (for example, an unprefixed `storageKey` read back with `tempStorage.get`) looks like the input "not saving" or "ignoring new values".

### 8. Cast UI Parts to 'any' When Type Checking Fails

**❌ WRONG:**
```typescript
content.push({
    type: 'row',
    content: [/* ... */]
}); // Type error: complex nested types
```

**✅ CORRECT:**
```typescript
content.push({
    type: 'row' as const,
    alignment: 'center',
    content: [/* ... */] as any
} as any);
```

**Note on `row` and `column` components:** Do NOT use `spacing` as a numeric pixel value. On `row`/`column`, `spacing` is a **string** that sets how children are distributed along the main axis: `'start'`, `'center'`, `'end'`, `'space-between'`, or `'space-around'`. `alignment` sets cross-axis alignment and only accepts `'start'`, `'center'`, or `'end'`. `'left'`/`'right'` are not valid values. Both parts also accept `wrap: boolean`. To control the gap between child elements, use `margin` in the `style` property of the children:

```typescript
// ❌ WRONG - numeric spacing and 'left' alignment are not valid values
{ type: 'row' as const, spacing: 10, alignment: 'left', content: [...] }

// ✅ CORRECT - string spacing/alignment on the row, margin on children
{
    type: 'row' as const,
    spacing: 'start',
    alignment: 'center',
    content: [
        { type: 'button' as const, text: 'A', style: { margin: '2px' } } as any,
        { type: 'button' as const, text: 'B', style: { margin: '2px' } } as any
    ]
} as any
```

### 9. Declare Function Return Types

**❌ WRONG:**
```typescript
function renderView() {
    return [];
}

async function getData() {
    return await api.v1.storage.get('key');
}
```

**✅ CORRECT:**
```typescript
function renderView(): any[] {
    return [];
}

async function getData(): Promise<any> {
    return await api.v1.storage.get('key');
}
```

### 10. Never Use Browser APIs Not Available in NovelAI

**❌ FORBIDDEN:**
```typescript
confirm('Are you sure?') // Does NOT exist
alert('Hello') // Does NOT exist
prompt('Enter name') // Does NOT exist
localStorage.setItem() // Does NOT exist
setTimeout(fn, 1000) // Does NOT exist (nor clearTimeout)
fetch(url) // Arbitrary network requests are not allowed
```

**✅ USE INSTEAD:**
```typescript
// For confirmations: Use UI buttons
{
    type: 'button',
    text: 'Confirm Delete',
    callback: async () => {
        await deleteItem();
    }
}

// For storage: Use NovelAI storage APIs
await api.v1.storage.set('key', value);
await api.v1.tempStorage.set('key', value);
await api.v1.storyStorage.set('key', value);

// For delays: Use the timers API (setTimeout resolves to a timer ID)
const timerId = await api.v1.timers.setTimeout(() => { /* ... */ }, 1000);
await api.v1.timers.clearTimeout(timerId);
await api.v1.timers.sleep(500);
```

### 11. Explicitly Type Arrays When Using Const Objects with .includes()

**❌ WRONG:**
```typescript
const BIOME_TYPES = {
  FOREST: 'forest',
  PLAINS: 'plains',
  MOUNTAINS: 'mountains'
} as const;

// Later in code:
const preferredBiomes = [BIOME_TYPES.PLAINS, BIOME_TYPES.FOREST];
// ...
if (preferredBiomes.includes(cell.biomeType)) { // ERROR!
  // Argument of type 'string' is not assignable to parameter of type '"forest" | "plains"'
}
```

**✅ CORRECT:**
```typescript
const BIOME_TYPES = {
  FOREST: 'forest',
  PLAINS: 'plains',
  MOUNTAINS: 'mountains'
} as const;

// Explicitly type as string[] to allow .includes() with string values
const preferredBiomes: string[] = [BIOME_TYPES.PLAINS, BIOME_TYPES.FOREST];
// ...
if (preferredBiomes.includes(cell.biomeType)) { // Works!
  // ...
}
```

**Why this happens:**
- `as const` makes the object deeply readonly with literal types
- Arrays from const objects become `readonly ['plains', 'forest']` type
- `.includes()` expects the exact literal type, not a general `string`
- Typing as `string[]` widens the type and allows any string in `.includes()`

### 12. Always Use `ui.update()` for UI Panels — Never `ui.register()`

**❌ WRONG (UI disappears on script disable/re-enable or story copy):**
```typescript
// Using register() for initial UI creation
await api.v1.ui.register([{
    type: 'sidebarPanel',
    id: 'my-panel',
    name: 'My Script',
    content: mainContent
}]);

// Then using update() for subsequent changes
await api.v1.ui.update([{
    type: 'sidebarPanel',
    id: 'my-panel',
    name: 'My Script',
    content: newContent
}]);
```

**✅ CORRECT (UI survives disable/re-enable and story copy):**
```typescript
// Use update() for BOTH initial creation AND subsequent changes
// update() creates the panel if it doesn't exist, and updates it if it does
await api.v1.ui.update([{
    type: 'sidebarPanel',
    id: 'my-panel',
    name: 'My Script',
    content: mainContent
}]);
```

**Why this matters:**
- `api.v1.ui.register()` silently fails when re-registering an existing panel ID
- When a user disables and re-enables a script, or copies a story, the script reinitializes but the panel ID may still be tracked from the previous session
- `register()` fails on the second call → the sidebar panel never appears → the script UI vanishes completely
- `api.v1.ui.update()` works as both create-if-missing AND update-if-exists, making it resilient to script reloads, disable/re-enable cycles, and story copies
- **This applies to ALL UI extension types**: `sidebarPanel`, `scriptPanel`, `lorebookPanel`, etc.

**Correct initialization pattern:**
```typescript
// In your onScriptsLoaded hook or initialization function:
api.v1.hooks.register('onScriptsLoaded', async () => {
    const content = await renderMainUI();
    
    // Use update(), NOT register()
    await api.v1.ui.update([{
        type: 'sidebarPanel',
        id: 'my-script-panel',
        name: 'My Script',
        content: content
    }]);
});

// Your updateUI function also uses update() — same call, consistent behavior
async function updateUI(): Promise<void> {
    const content = await renderMainUI();
    await api.v1.ui.update([{
        type: 'sidebarPanel',
        id: 'my-script-panel',
        name: 'My Script',
        content: content
    }]);
}
```

**Note:** `api.v1.hooks.register()` for hooks is fine and correct — this rule only applies to `api.v1.ui.register()` for UI extensions.

### 13. Read Button-Driven Input Values From the Storage the Input Is Bound To

Per the docs, an input with a `storageKey` saves its value to storage automatically whenever the user changes it, and updates itself when that stored value changes elsewhere. A separate "Create"/"Save" button can read the current value straight from storage at click time, without the user pressing Enter. NovelAI's own Find & Replace example does exactly this with an unprefixed key and `api.v1.storage.get()`.

The common bug is reading from the wrong storage. An unprefixed `storageKey: 'name'` writes to `api.v1.storage`, so `api.v1.tempStorage.get('name')` comes back empty or stale. Match the prefix to the API (see pitfall 7):

```typescript
{ type: 'textInput' as const, storageKey: 'temp:form-name' } as any
// ...in the button callback:
const name = await api.v1.tempStorage.get('form-name') as string | undefined;
```

If you deliberately don't use a `storageKey`, mirror the value yourself with `onChange` (e.g. `onChange: (v: string) => api.v1.tempStorage.set('form-name', v)`).

### 14. Create/Edit Forms: Pre-fill Through the Bound Key, or Use initialValue

When one form serves both "create new" and "edit existing", you can either:
- **Keep `storageKey`** and set the bound key before showing the form (`await api.v1.tempStorage.set('form-name', existing.name)` for `storageKey: 'temp:form-name'`, or clear it for "create"). The input follows the stored value.
- **Or skip `storageKey`**: pass `initialValue` for display and use `onChange` to write every keystroke to tempStorage. The edit button's callback calls `clearFormStorage()`, then `tempStorage.set()` for each field with the existing data, then `updateUI()`. The re-rendered form reads those values and passes them as `initialValue`.

If a `storageKey` input seems to "cache the old value and ignore new `tempStorage.set()` calls", check the prefix first. An unprefixed key is bound to `api.v1.storage`, not tempStorage.

### 15. Validate Modal Content Props, and Use the Promise + safeResolve Pattern

`api.v1.ui.modal.open` (and `window.open`) **return a Promise**: always `await` them before using `.close()`, `.update()`, or `.closed`. Modal content accepts any UI parts (`UIPart[]`). NovelAI's own demo scenario puts bare `button`s, `textInput`s, `text`, `row`s, and `box`es directly in modal `content`.

The error `ui.modal.open: options.content[N] does not match any of the allowed types` means part N (or something nested in it) failed schema validation. Usually a property has an invalid value or name. Check for:
- `alignment: 'left'` / `'right'` on a `row`/`column` (valid: `'start'`, `'center'`, `'end'`)
- a numeric `spacing` (valid: `'start'`, `'center'`, `'end'`, `'space-between'`, `'space-around'`)
- `size` other than `'small'`, `'medium'`, `'large'`, `'full'`
- misspelled props (e.g. `disableWhileCallbackRunning` instead of `disabledWhileCallbackRunning`) or props that part doesn't have

Compare each part against its `UIPart*` type in `NovelAI_Script_Types.d.ts`.

**Simple modal (bare buttons are fine):**
```typescript
const modal = await api.v1.ui.modal.open({
    title: 'Confirm',
    size: 'small',
    content: [
        { type: 'text' as const, text: 'Are you sure?' } as any,
        { type: 'button' as const, text: 'Yes', callback: async () => { await modal.close(); } } as any,
        { type: 'button' as const, text: 'No', callback: async () => { await modal.close(); } } as any
    ]
});
```

**Confirmation dialog that returns the user's choice: use the Promise + safeResolve pattern:**
```typescript
async function showConfirmation(): Promise<boolean> {
    return new Promise(async (resolve) => {
        let resolved = false;
        function safeResolve(value: boolean): void {
            if (!resolved) { resolved = true; resolve(value); }
        }

        const modal = await api.v1.ui.modal.open({
            title: 'Confirm',
            size: 'small',
            content: [
                {
                    type: 'text',
                    text: '**Are you sure?**',
                    markdown: true,
                    style: { marginBottom: '4px' }
                },
                {
                    type: 'box',
                    content: [{
                        type: 'text',
                        text: 'This action cannot be undone.',
                        style: { fontSize: '12px' }
                    }]
                },
                {
                    type: 'row' as const,
                    alignment: 'center',
                    content: [
                        {
                            type: 'button' as const,
                            text: 'Yes',
                            style: { margin: '4px' },
                            callback: async () => { safeResolve(true); await modal.close(); }
                        } as any,
                        {
                            type: 'button' as const,
                            text: 'No',
                            style: { margin: '4px' },
                            callback: async () => { safeResolve(false); await modal.close(); }
                        } as any
                    ]
                } as any
            ]
        });

        // Catches X button and "Disable This Script" closures
        modal.closed.then(() => { safeResolve(false); });
    });
}
```

**Key points:**
- **`row`** is a convenient way to lay button groups out horizontally; `box` gives grouped content a bordered background
- Always use the **Promise + `safeResolve` + `modal.closed.then()`** pattern so the calling code doesn't hang when the user closes the modal via X button or "Disable This Script"
- **⚠️ CRITICAL — Resolve BEFORE close:** Always call `safeResolve()` **before** `await modal.close()` in button callbacks. `await modal.close()` triggers the `modal.closed.then()` handler synchronously, which calls `safeResolve(false)` — if the button hasn't resolved yet, the fallback wins and the button appears to do nothing. Correct order: `safeResolve(value); await modal.close();`

**❌ WRONG — close before resolve (buttons silently do nothing):**
```typescript
callback: async () => { await modal.close(); safeResolve(true); }
// modal.close() fires modal.closed.then() → safeResolve(false) wins
// safeResolve(true) is ignored because resolved is already true
```

**✅ CORRECT — resolve before close:**
```typescript
callback: async () => { safeResolve(true); await modal.close(); }
// safeResolve(true) sets resolved = true with the correct value
// modal.closed.then() → safeResolve(false) is safely ignored
```

### 16. Always Compile with `tsc --strict` Before Delivering the Script

**MANDATORY**: Before presenting the final script file, always set up a local compilation check and verify zero errors.

**Setup (do this once per chat):** compile against the bundled official type definitions. Don't hand-write a stub, since a stub hides real mistakes like misspelled props or invalid enum values.
```bash
mkdir -p nai-check && cd nai-check
cp <skill-dir>/references/NovelAI_Script_Types.d.ts ./types.d.ts
{ echo 'export {};'; cat <path-to>/my-script.ts; } > ./script.ts   # check copy only; the /*--- ---*/ header is a comment, so it's fine
cat > tsconfig.json <<'EOF'
{ "compilerOptions": { "strict": true, "noEmit": true, "target": "ES2022", "module": "ES2022", "lib": ["ES2022"] },
  "files": ["types.d.ts", "script.ts"] }
EOF
tsc -p .    # install with `npm i -g typescript` if missing
```
The `export {};` line and the `ES2022` module/target settings let tsc accept top-level `await` (errors TS1375/TS1378 otherwise). Add the line only to the check copy, not the delivered script. The `as any` casts recommended elsewhere skip checking on those objects. For a stricter pass, temporarily drop the casts on UI parts to catch invalid props. Scripts using `jsx` parts or experimental APIs also need `NovelAI_JSX_Types.d.ts` / `NovelAI_Script_Types_Experimental.d.ts` and the JSX compiler options. See §8 of `NovelAI_JSX_Guide.md`.

**The output must be 0 lines / 0 errors.** If there are errors, fix them all before delivering.

**Why:** The NovelAI script editor runs TypeScript compilation and will reject scripts with type errors. The user cannot fix these themselves.

### 17. Don't Let Edits Swallow Adjacent Code

When inserting code with a find-and-replace edit, make sure the replacement restores any line you matched after the insertion point (e.g. the next function's header), and re-check a few lines around each edit.

### 18. Look Up Property Names, Don't Guess

Before using properties of a NovelAI API type, check `NovelAI_Script_Types.d.ts` (e.g. `grep -n "type UIPartButton" -A15`). For your own interfaces, grep their definitions and existing usage. Guessed names compile silently under `as any` and then do nothing at runtime.

### 19. Never Re-render the Panel From an Input's onChange

Calling `updateUI()` / `render()` (anything that ends in a full `api.v1.ui.update()`) inside an input's `onChange` rebuilds the whole panel while the user is still using that input. This applies to **every** part with an `onChange`: `textInput`, `multilineTextInput`, `numberInput`, `sliderInput`, `checkboxInput`, and `codeEditor` (and `onInput`/`onChange` handlers inside a `jsx` part that trigger a script-side re-render). The rebuild:

- **loses focus** in the input being typed in, so the next keystrokes go nowhere;
- **drops or duplicates keystrokes** while the rebuild is in flight;
- **resets anything that was open**: dropdowns inside a `jsx` part, collapsible sections without a `storageKey`, and scroll position;
- **breaks callbacks** on continuous inputs: sliders and number inputs fire `onChange` on every step of a drag. The first event rebuilds the panel and assigns new callback IDs, and the next event calls the **old** ID, which produces `UI callback "__callback_NNNN" not found` on every later event.

**❌ WRONG — re-rendering from onChange:**
```typescript
api.v1.ui.part.sliderInput({
    storageKey: 'my-slider',
    min: 1, max: 10, step: 1,
    onChange: async (value: number) => {
        await api.v1.storage.set('threshold', value);
        await updateUI(); // CRASH — destroys callbacks mid-drag
    },
});

api.v1.ui.part.textInput({
    storageKey: 'temp:draft-title',
    onChange: async (_value: string) => {
        await updateUI(); // loses focus after every keystroke
    },
});
```

**✅ CORRECT — persist only, and refresh just the part that shows the value:**
```typescript
api.v1.ui.part.sliderInput({
    storageKey: 'my-slider',
    min: 1, max: 10, step: 1,
    onChange: async (value: number) => {
        await api.v1.storage.set('threshold', value);
        await api.v1.ui.updateParts([{ type: 'text', id: 'threshold-label', text: `Threshold: ${value}` }]);
    },
});

// Or skip the handler entirely: a template re-renders on its own when the key changes.
api.v1.ui.part.text({ text: 'Draft: {{temp:draft-title}}' });
```

**Re-render as little as possible.** Pick the cheapest refresh that covers the change:

| Change | Refresh with |
| :--- | :--- |
| A stored value shown as text | Nothing: a `{{temp:…}}` / `{{story:…}}` / `{{key}}` template re-renders by itself |
| One part's text, style, or disabled state | `api.v1.ui.updateParts([{ type, id, ... }])` on a part with a stable `id` |
| Structure (items added or removed, view switched) | A full `render()` / `api.v1.ui.update()`, from a button `callback` or an input's `onSubmit` (each fires once) |

Any button that acts on an input's value should read it fresh from storage at click time (not from a variable captured at render time), since the input may have changed without a rebuild. Note that `numberInput`'s `onChange`/`onSubmit` receive the value as a **string** (`sliderInput` passes a number, `checkboxInput` a boolean).

### 20. Use Only Valid Enum Values on Layout Parts (Modal Validator)

Modal content is validated against the UI part schemas, and the validator recurses into nested content. A single invalid value anywhere fails the whole part with `does not match any of the allowed types`. The classic trigger is `alignment: 'left'`, which is not a valid value.

**❌ WRONG — `'left'` is not a valid alignment (fails in modal):**
```typescript
content.push({
  type: 'row' as const, alignment: 'left', content: [
    { type: 'text' as const, text: '■', style: { color: '#E6194B' } } as any,
    { type: 'text' as const, text: 'Kingdom Name' } as any
  ]
} as any);
```

**✅ CORRECT — valid alignment value.** Nothing in the docs or types forbids text-only rows. If one still fails after fixing the values, fall back to a single `text` element (e.g. `'■ Kingdom Name'`).
```typescript
content.push({
  type: 'row' as const, alignment: 'center', spacing: 'start', content: [
    { type: 'text' as const, text: '■', style: { color: '#E6194B', marginRight: '4px' } } as any,
    { type: 'text' as const, text: 'Kingdom Name' } as any
  ]
} as any);
```

**Rule of thumb:** `alignment` ∈ `'start' | 'center' | 'end'`; `spacing` ∈ `'start' | 'center' | 'end' | 'space-between' | 'space-around'`. When in doubt, check the `UIPart*` type in `NovelAI_Script_Types.d.ts`.

### 21. Never Embed NovelAI Import-Format Signatures in Strings (Paste Killer)

NovelAI's script editor sniffs pasted clipboard text for content that looks like
NovelAI's own JSON import formats. If the pasted text contains a lorebook-entry
signature — specifically the word keys immediately followed by a quote and a
colon, i.e. the JSON field name of a lorebook entry's activation keys — the
ENTIRE paste is silently swallowed: nothing is inserted, no error is shown.
The clipboard is fine (the same copy pastes into any plain textarea); it is the
editor's paste handler diverting the text into an import path that then fails.

A single occurrence is enough: one prompt template containing a JSON example
with that field name makes the whole compiled script (and every excerpt
containing that line) unpasteable, however large it is. Renaming the field
fixes it immediately.

Rules:
- NEVER write a JSON example, template, or documentation string whose text
  contains the lorebook keys field signature (the word keys directly followed
  by ": ) — in prompts, comments, placeholders, ANYWHERE in the compiled
  output. Use a different field name such as activation_keys and adapt the
  parser (dot-access like parsed.keys in CODE is safe; only the quoted JSON
  form is dangerous).
- Treat other NovelAI import-format signatures with the same suspicion when
  embedding JSON-looking text: field combinations resembling lorebook entries,
  scenarios, or presets may trip the same sniffer. Prefer renamed fields or
  inline prose-wrapped examples.
- This applies to COMMENTS too: an explanatory comment quoting the forbidden
  form re-poisons the build (this happened during the fix itself).
- Diagnostic signature if it ever recurs: paste "does nothing" in the script
  editor while the identical clipboard pastes fine into a plain textarea;
  bisect the text — the trigger is a substring, not size, encoding, or emoji.

### 22. Use Style Presets, Theme Tokens, and Factory Functions for All UI Styling

Never write one-off inline style objects scattered across the script. Define style presets and factory functions **once at the top** of the script and reference them everywhere. For the full scalable version (namespaced IDs, token maps, typed `api.v1.ui.part.*` factories with variants, storage-bound `field()` helpers, render/refresh strategy, reusable dialogs), see **`NovelAI_UI_Component_System.md`**.

#### Style Presets (Object Constants)

```typescript
// ✅ CORRECT — define once at top of script
const CARD_STYLE: Record<string, string> = {
    backgroundColor: 'bg1',
    border: '1px solid',         // width + style only
    borderColor: 'bg2',          // color always on its own (tokens don't apply inside the shorthand)
    borderRadius: '6px',
    padding: '12px',
    margin: '6px 0',
};

const DANGER_STYLE: Record<string, string> = {
    ...CARD_STYLE,     // spread base, then override
    borderColor: 'warning',
};

// Apply later via spread:
{ type: 'container' as const, style: { ...CARD_STYLE, padding: '4px' }, content: [...] } as any
```

#### CSS Rules

- **Borders:** a theme token inside the `border` shorthand doesn't apply its color, so `border: '1px solid bg2'` doesn't work. Write `border: '1px solid'` (or `borderWidth` + `borderStyle`) and put the color in its own `borderColor`, after the shorthand.
- **4px / 8px grid:** every size, spacing, and radius value is a multiple of 4 or 8 pixels (`4px`, `8px`, `12px`, `16px`, `24px`…), or one of the small half-steps `1px`, `2px`, and `6px` for borders, tight gaps, and small radii. Rem equivalents work too (`2px = 0.125rem`, `4px = 0.25rem`, `6px = 0.375rem`, `8px = 0.5rem`, `12px = 0.75rem`, `16px = 1rem`, `24px = 1.5rem`). Values like `5px` or `10px` are off the grid. Pick px or rem for a script and don't mix them.
- **Restyleable from one place:** every element comes from a factory or gets a named preset and a namespaced `id`. Standard UI parts have no `class`/`className` prop (only `jsx` parts do), so a preset name is the "class".

```typescript
// ❌ WRONG — theme token inside the shorthand: the color doesn't apply
const badPanel: Record<string, string> = { border: '1px solid bg2', padding: '12px', borderRadius: '6px' };

// ✅ CORRECT — color on its own
const panel: Record<string, string> = { border: '1px solid', borderColor: 'bg2', padding: '12px', borderRadius: '6px' };
```

#### Theme Tokens (Never Hardcode Hex Colors)

Instead of hardcoding hex colors, plug theme token strings directly as values into UIPart `style` properties. At runtime NovelAI replaces each token with the user's actual theme value, written as an inline literal (e.g. `'bg1'` becomes an `rgb(...)` code in the element's inline style).

> **⚠️ Tokens are not CSS variables.** The scripting environment only exposes the bare token strings (`'bg1'`, `'bg2'`, `'bg3'`, ...). There are no `--theme-*` custom properties for scripts or page-level custom CSS to reference, so don't write `var(--theme-bg1)`. Because the substitution is a literal inline value, custom CSS elsewhere on the site can't read or reuse it either. If a script needs the raw color/font values (e.g. to lighten a color), call `api.v1.theme.get()`. *(Only exception: the official type definitions say JSX UI parts (`type: 'jsx'`) have `--theme-*` custom properties available inside them. Regular UI parts and page CSS don't.)*

| Token / Key | Role |
| :--- | :--- |
| `'bg0'` | Deepest / outermost background |
| `'bg1'` | Default panel background |
| `'bg2'` | Raised surface / border / button background |
| `'bg3'` | Highlighted / selected surface |
| `'textHeadings'` | High-contrast headings |
| `'textMain'` | Default body text |
| `'textDisabled'` | Disabled / muted text |
| `'textPlaceholder'` | Input placeholder text |
| `'textHighlight'` | Search / highlight color |
| `'warning'` | Warning / alert state |
| `'textPrompt'`, `'textUser'`, `'textAI'`, `'textEdit'` | Story text colors |
| `'lowIntensityColor'`, `'midIntensityColor'`, `'highIntensityColor'` | Low/mid/high probability colors |
| `'default'` | Body font family (use in `fontFamily`) |
| `'headings'` | Heading font family (use in `fontFamily`) |
| `'code'` | Monospace code font family |
| `'field'` | Form / input field font family |

> **⚠️ Warning on `'primary'`**: NovelAI does **NOT** have a `'primary'` or `'error'` theme token. Using `color: 'primary'` produces invalid CSS. For active/highlighted surfaces use `'bg3'`, for high-contrast accents use `'textHeadings'`, or supply explicit hex/rgba color strings (e.g. `'#90caf9'`).

```typescript
// ❌ WRONG — hardcoded color breaks in light themes, 'primary' is invalid CSS
{ style: { backgroundColor: '#1a1a2e', color: 'primary' } }

// ✅ CORRECT — theme tokens adapt automatically
{ style: { backgroundColor: 'bg1', color: 'textHeadings' } }
```

#### Factory Functions (The NovelAI Equivalent of cloneNode)

**Never use `document.createElement`, `cloneNode`, or DOM APIs** — they do not exist in the Web Worker. Instead, write typed factory functions that return pre-styled UI Part objects:

```typescript
// ✅ CORRECT — factory function defined once, used everywhere
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

// Usage:
makeButton('Save', handleSave);
makeButton('Delete', handleDelete, { backgroundColor: 'warning' });
makeCard('Options', [/* children */]);
```

---

## NovelAI-Specific Best Practices

### Storage Types
- `api.v1.storage` - Script-level storage (account or story based on script type)
- `api.v1.storyStorage` - Always stores in current story
- `api.v1.tempStorage` - Session-only, cleared on story close
- `api.v1.historyStorage` - History-aware (reverts with undo/redo)

### UI Input Best Practices
1. **Always use `storageKey`** (or `initialValue`) for text inputs, NOT `value` (there is no `value` prop)
2. Use `onSubmit` (or a button) for anything that re-renders the panel, NOT `onChange` (see pitfall 19)
3. Initialize storage before showing inputs with storageKey
4. Clear form storage before opening create/edit forms
5. Prefix `storageKey` to match the storage you read in code: none → `storage`, `story:` → `storyStorage`, `history:` → `historyStorage`, `temp:` → `tempStorage`

### Storage Key Patterns
```typescript
// UI part side: the prefix selects the storage
{ type: 'textInput' as const, storageKey: 'temp:draft-title' } as any
{ type: 'text' as const, text: 'Saved: {{story:saved-title}}' } as any

// Code side: call the matching API with the bare key
const draft = await api.v1.tempStorage.get('draft-title');
await api.v1.storyStorage.set('saved-title', draft);

// Defaults without an extra has() round trip
const count = await api.v1.storage.getOrDefault('runCount', 0);
```

### Async Function Patterns
```typescript
// Always declare return types for async functions
async function updateUI(): Promise<void> { }
async function getData(): Promise<any> { }
async function renderView(): Promise<any[]> { }
```

## Quick Checklist Before Submitting Code

- [ ] All function parameters have type annotations
- [ ] All arrow function parameters in callbacks have types
- [ ] `Object.entries()` and `Object.values()` are cast to `[string, any][]` or `any[]`
- [ ] `Array.shift()` results are checked for undefined
- [ ] Functions with `await` are declared `async`
- [ ] Storage `.get()` results are cast to proper types with `| undefined`
- [ ] Text inputs use `storageKey` + `onSubmit`, not `value` + `onChange`
- [ ] Every `storageKey` / `{{key}}` prefix (`temp:`, `story:`, `history:`, or none) matches the storage API the code reads
- [ ] No use of `confirm()`, `alert()`, `prompt()`, global `setTimeout`, or browser storage APIs
- [ ] No DOM APIs (`document`, `window`, `cloneNode`) — use factory functions instead
- [ ] Style objects defined as `Record<string, string>` constants at the top of the script
- [ ] Theme tokens (`'bg1'`, `'textHeadings'`, `'warning'`, etc.) used instead of hardcoded hex colors
- [ ] Reusable elements built with factory functions, not duplicated inline style blocks
- [ ] Border colors are set with `borderColor`, never inside the `border` shorthand
- [ ] Every size, spacing, and radius is on the 4px/8px grid (multiples of 4 or 8, or the `1px`/`2px`/`6px` half-steps), all in px or all in rem
- [ ] Complex UI parts are cast with `as const` and `as any` where needed
- [ ] Storage is initialized before using `storageKey` in inputs
- [ ] Arrays used with `.includes()` on string values are typed as `string[]`
- [ ] UI panels use `api.v1.ui.update()` — never `api.v1.ui.register()` for UI extensions
- [ ] `row`/`column` `spacing` is a string (`'start'`/`'center'`/`'end'`/`'space-between'`/`'space-around'`), never a number; `alignment` is `'start'`/`'center'`/`'end'` (never `'left'`/`'right'`)
- [ ] Buttons use `disabledWhileCallbackRunning` (not `disableWhileCallbackRunning`)
- [ ] No input `onChange` (text, multiline, number, slider, checkbox, code editor) re-renders the whole panel; small refreshes use `updateParts` or `{{templates}}`
- [ ] `api.v1.ui.modal.open()` / `window.open()` are awaited before using the returned handle
- [ ] No string anywhere contains the lorebook keys JSON field signature (word keys + quote + colon) — it makes the compiled script unpasteable into the editor

## Common Error Messages and Fixes

| Error Message | Fix |
|---------------|-----|
| `Parameter 'x' implicitly has an 'any' type` | Add type: `(x: string)` or `(x: any)` |
| `'loc' is of type 'unknown'` | Cast: `as any[]` or `as [string, any][]` |
| `Type 'undefined' is not assignable to type 'string'` | Add null check or cast: `as string \| undefined` |
| `'await' expressions are only allowed within async functions` | Make function `async` and add return type |
| `Object literal may only specify known properties` | Cast to `as any` |
| `Argument of type X is not assignable to parameter of type Y` | Cast UI parts with `as const` and `as any` |
| `Argument of type 'string' is not assignable to parameter of type '"x" \| "y"'` | Type array as `string[]` instead of inferring from const object |
| UI panel disappears after disable/re-enable or story copy | Replace all `api.v1.ui.register()` with `api.v1.ui.update()` |
| `UI callback "__callback_NNNN" not found` during slider/input interaction | Remove `updateUI()` from the widget's `onChange` handler — it destroys callbacks mid-interaction (pitfall 19) |
| Text input loses focus or drops keystrokes while typing | The input's `onChange` re-renders the panel. Persist only, and use `updateParts`/`{{templates}}` for live values (pitfall 19) |
| `ui.modal.open: options.content[N] does not match any of the allowed types` | Part N (or a nested child) has an invalid value or prop name, typically `alignment: 'left'`/`'right'`, numeric `spacing`, a bad `size`, or a misspelled prop. Check it against the `UIPart*` type; see pitfalls 15 and 20. |
| Input "doesn't save" / button reads an empty value / input ignores `tempStorage.set()` | `storageKey` prefix doesn't match the API you read with (unprefixed = `api.v1.storage`; use `temp:` for tempStorage). See pitfall 7. |
| `modal.close is not a function` / handle is a Promise | `await api.v1.ui.modal.open(...)` (same for `window.open`). |
| Pasting the compiled script into the editor silently does nothing | The text contains a NovelAI import-format signature (lorebook keys field). Rename the field (e.g. activation_keys); see pitfall 21. |

---

**Summary**: When coding NovelAI scripts, be explicit with types everywhere, cast liberally with `as any` for UI parts, use `storageKey` for inputs with the right storage prefix (`temp:`/`story:`/`history:`), never use browser APIs not in the NovelAI API, always use `api.v1.ui.update()` (not `register()`) for UI panels, only use the documented string values for row/column `spacing` and `alignment`, never re-render the panel from any input's `onChange` handler, and `await` modal/window handles.
