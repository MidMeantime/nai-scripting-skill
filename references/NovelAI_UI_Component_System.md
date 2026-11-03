# Reusable, Scalable UI in NovelAI Scripts

NovelAI scripts can't touch the DOM. There's no `document.createElement`, `cloneNode`, `<style>` injection, or `:root` CSS variables, because scripts run in a Web Worker. UI is a tree of plain **UI Part objects** handed to `api.v1.ui.update()` / `modal.open()` / `window.open()`. The browser habits of style presets, element templates, and CSS variables all still apply, but they map onto plain objects:

| Browser habit | NovelAI equivalent |
| :--- | :--- |
| `Partial<CSSStyleDeclaration>` + `Object.assign` | `Record<string, string>` style presets merged with object spread |
| CSS variables (`--accent`) | **Theme tokens** as values (`'bg1'`, `'textHeadings'`, …) plus your own TypeScript constants for spacing/radii |
| `<template>` / `cloneNode(true)` | **Factory functions** that return UI parts (built on `api.v1.ui.part.*`) |
| CSS classes | Named presets (`S.card`, `S.muted`) and component variants |
| Re-rendering a DOM subtree | `api.v1.ui.update()` for whole extensions, `api.v1.ui.updateParts()` for parts with a stable `id`, `{{temp:key}}` templates for live values |

The layers below build on each other. Taken in order, every code block in this file forms one script that type-checks under `tsc --strict` against `NovelAI_Script_Types.d.ts`.

---

## 1. Namespace and Tokens

Pick one short namespace and derive every ID and storage key from it. Two scripts that both use `'panel'` or `'name'` would otherwise collide. Theme tokens go in a `COLOR` map so components never hardcode hex values. Spacing and radii are ordinary constants, which is the role CSS variables would play on a normal page.

```typescript
const NS = 'myscript';

/** Namespaced ID for UI parts and extensions: id('status') -> 'myscript.status' */
const id = (name: string): string => `${NS}.${name}`;

/** Spacing and radii. Pick px or rem for a script and don't mix them. */
const SPACE = { xs: '2px', sm: '4px', md: '8px', lg: '12px', xl: '16px' } as const;
const RADIUS = { sm: '4px', md: '6px', lg: '12px' } as const;

/** Semantic names for NovelAI theme tokens (replaced with the user's theme at render time). */
const COLOR = {
    canvas: 'bg0',
    surface: 'bg1',
    raised: 'bg2',
    selected: 'bg3',
    heading: 'textHeadings',
    body: 'textMain',
    muted: 'textDisabled',
    highlight: 'textHighlight',
    danger: 'warning',
} as const;

const FONT = { body: 'default', heading: 'headings', mono: 'code', field: 'field' } as const;
```

> Use only real token names (see the token table in `SKILL.md`). `primary`, `error`, `textHeading`, and `textDescription` are **not** tokens. Invalid values produce invalid CSS that the browser silently drops.
>
> **Borders:** a theme token inside the `border` shorthand doesn't apply its color (`border: '1px solid bg2'` doesn't work). Set the width and style with `border: '1px solid'` (or `borderWidth` + `borderStyle`, as the presets below do), and always put the color in its own `borderColor`. That also lets variants override just the color.

---

## 2. Style Presets

Presets are the "classes". Build specific ones from general ones with spread, and keep each one small and single-purpose so they combine well.

```typescript
type Style = Record<string, string>;

const S: Record<string, Style> = {
    card: {
        backgroundColor: COLOR.surface,
        borderStyle: 'solid', borderWidth: '1px', borderColor: COLOR.raised,
        borderRadius: RADIUS.md,
        padding: SPACE.lg,
        margin: `${SPACE.sm} 0`,
    },
    heading: { color: COLOR.heading, fontFamily: FONT.heading, margin: `0 0 ${SPACE.md} 0` },
    body: { color: COLOR.body },
    muted: { color: COLOR.muted, fontSize: '12px' },
    mono: { fontFamily: FONT.mono, fontSize: '12px' },
    gapRight: { marginRight: SPACE.sm },
};

S.cardDanger = { ...S.card, borderColor: COLOR.danger };
S.cardSelected = { ...S.card, backgroundColor: COLOR.selected };

/** Merge any number of presets/overrides; later ones win (like stacking CSS classes). */
const sx = (...styles: (Style | undefined | false)[]): Style =>
    Object.assign({}, ...styles.filter(Boolean));
```

Inline styles can't do `:hover`, media queries, or `url(...)` (URLs are stripped), so presets cover static looks only.

---

## 3. Component Factories

Factories are the `cloneNode` replacement. Build them on `api.v1.ui.part.*`: those helpers add the `type` field and return correctly typed parts, so you don't need `as const` / `as any` casts. Give each factory **one options object** (`opts`) so new options don't break existing call sites, and use **variants** instead of copy-pasted overrides.

```typescript
type ButtonVariant = 'default' | 'danger' | 'subtle';
type ButtonOpts = { id?: string; icon?: IconId; variant?: ButtonVariant; disabled?: boolean; style?: Style };

const BUTTON_VARIANTS: Record<ButtonVariant, Style> = {
    default: { backgroundColor: COLOR.raised, color: COLOR.heading },
    danger: { backgroundColor: COLOR.danger, color: COLOR.heading },
    subtle: { backgroundColor: 'transparent', color: COLOR.body },
};

function button(text: string, onClick: () => void | Promise<void>, opts: ButtonOpts = {}): UIPartButton {
    return api.v1.ui.part.button({
        id: opts.id,
        text,
        iconId: opts.icon,
        disabled: opts.disabled,
        disabledWhileCallbackRunning: true,   // note the "d"
        callback: onClick,
        style: sx({ margin: SPACE.sm, padding: `${SPACE.sm} ${SPACE.lg}`, borderRadius: RADIUS.sm },
                  BUTTON_VARIANTS[opts.variant ?? 'default'], opts.style),
    });
}

function heading(text: string, level: 2 | 3 | 4 = 3): UIPartText {
    return api.v1.ui.part.text({ text: `${'#'.repeat(level)} ${text}`, markdown: true, style: S.heading });
}

function text(value: string, opts: { id?: string; muted?: boolean; markdown?: boolean; style?: Style } = {}): UIPartText {
    return api.v1.ui.part.text({
        id: opts.id, text: value, markdown: opts.markdown,
        style: sx(opts.muted ? S.muted : S.body, opts.style),
    });
}

function card(title: string | null, children: UIPart[], opts: { id?: string; variant?: 'default' | 'danger' | 'selected' } = {}): UIPartContainer {
    const base = opts.variant === 'danger' ? S.cardDanger : opts.variant === 'selected' ? S.cardSelected : S.card;
    return api.v1.ui.part.container({
        id: opts.id,
        style: base,
        content: title ? [heading(title), ...children] : children,
    });
}

/** Horizontal group. spacing/alignment take the documented string values only. */
function hstack(children: UIPart[], opts: { spacing?: UIPartRow['spacing']; align?: UIPartRow['alignment']; wrap?: boolean } = {}): UIPartRow {
    return api.v1.ui.part.row({ spacing: opts.spacing ?? 'start', alignment: opts.align ?? 'center', wrap: opts.wrap, content: children });
}

function vstack(children: UIPart[], opts: { spacing?: UIPartColumn['spacing']; align?: UIPartColumn['alignment'] } = {}): UIPartColumn {
    return api.v1.ui.part.column({ spacing: opts.spacing ?? 'start', alignment: opts.align ?? 'start', content: children });
}

/** Collapsible group that remembers its open/closed state per story. */
function section(title: string, children: UIPart[], opts: { startCollapsed?: boolean; icon?: IconId } = {}): UIPartCollapsibleSection {
    return api.v1.ui.part.collapsibleSection({
        title,
        iconId: opts.icon,
        initialCollapsed: opts.startCollapsed,
        storageKey: `story:${id('collapsed.' + title)}`,
        content: children,
    });
}
```

**Composition over configuration:** keep factories small and nest them. Avoid one giant `makeWidget(...)` with twenty flags.

---

## 4. Bound Fields (Storage Keys Without Prefix Bugs)

The most common bug is binding an input to one storage and reading another. An unprefixed `storageKey` means `api.v1.storage`, while `temp:`, `story:`, and `history:` select the others. A small helper owns the key, the prefix, and the accessors together, so they can't drift apart:

```typescript
type Scope = 'script' | 'story' | 'history' | 'temp';
const PREFIX: Record<Scope, string> = { script: '', story: 'story:', history: 'history:', temp: 'temp:' };
const STORE = {
    script: api.v1.storage, story: api.v1.storyStorage, history: api.v1.historyStorage, temp: api.v1.tempStorage,
};

/** One field = one key. `bind` goes in storageKey / {{templates}}; get/set/clear go in code. */
function field<T>(name: string, scope: Scope = 'temp', fallback?: T) {
    const key = id(name);
    return {
        bind: `${PREFIX[scope]}${key}`,
        template: `{{${PREFIX[scope]}${key}}}`,
        get: async (): Promise<T | undefined> => (await STORE[scope].getOrDefault(key, fallback)) as T | undefined,
        set: (value: T): Promise<void> => STORE[scope].set(key, value),
        clear: (): Promise<void> => STORE[scope].remove(key),
    };
}

// Declare every field once, at the top:
const F = {
    title: field<string>('form.title', 'temp', ''),
    notes: field<string>('form.notes', 'temp', ''),
    savedTitle: field<string>('saved.title', 'story'),
    runs: field<number>('runs', 'script', 0),
};

function textField(f: { bind: string }, label: string, opts: { multiline?: boolean; placeholder?: string } = {}): UIPart {
    return opts.multiline
        ? api.v1.ui.part.multilineTextInput({ label, storageKey: f.bind, placeholder: opts.placeholder })
        : api.v1.ui.part.textInput({ label, storageKey: f.bind, placeholder: opts.placeholder });
}
```

Inputs with a `storageKey` save as the user types, and they update when the stored value changes. Buttons can read `await F.title.get()` at click time, and pre-filling a form is just `await F.title.set(existing)`.

---

## 5. One Render Function, Targeted Refreshes

Keep a single `render()` that builds the whole extension from storage. Use stable, namespaced IDs, and pick the cheapest refresh:

| Change | Refresh with |
| :--- | :--- |
| A value shown as text | Nothing: a `{{temp:…}}` / `{{story:…}}` template re-renders by itself |
| One part's text/style/disabled state | `api.v1.ui.updateParts([{ type, id, ... }])` |
| Structure (items added or removed, view switched) | `render()` → `api.v1.ui.update([...])` |

Never call `render()` from any input's `onChange` (text, multiline, number, slider, checkbox, code editor). It loses focus, drops keystrokes, resets anything open, and breaks slider callbacks (see guidelines pitfall 19).

```typescript
const PANEL = { id: id('panel'), name: 'My Script', icon: 'feather' as IconId };
const STATUS_ID = id('status');

async function setStatus(message: string): Promise<void> {
    await api.v1.ui.updateParts([{ type: 'text', id: STATUS_ID, text: message }]);
}

async function render(): Promise<void> {
    const saved = await F.savedTitle.get();
    // ui.update() requires `id` to be a definite string, so re-state it after the helper's optional id
    await api.v1.ui.update([{
        ...api.v1.ui.extension.sidebarPanel({
            name: PANEL.name,
            iconId: PANEL.icon,
            content: [
                card('New Entry', [
                    textField(F.title, 'Title', { placeholder: 'Untitled' }),
                    textField(F.notes, 'Notes', { multiline: true }),
                    hstack([
                        button('Save', onSave, { icon: 'save' }),
                        button('Clear', onClear, { variant: 'subtle' }),
                    ], { spacing: 'end' }),
                ]),
                card('Saved', [
                    text(saved ? `Last saved: **${saved}**` : '_Nothing saved yet_', { markdown: true }),
                    text(`Runs: ${F.runs.template}`, { muted: true }),
                ]),
                text('', { id: STATUS_ID, muted: true }),
            ],
        }),
        id: PANEL.id,
    }]);
}

async function onSave(): Promise<void> {
    const title = ((await F.title.get()) ?? '').trim();
    if (!title) { await setStatus('Title is required.'); return; }
    await F.savedTitle.set(title);
    await F.runs.set(((await F.runs.get()) ?? 0) + 1);
    await render();                 // structure changed (the "Saved" card text)
    await setStatus('Saved.');
}

async function onClear(): Promise<void> {
    await F.title.clear();
    await F.notes.clear();          // bound inputs empty themselves
    await setStatus('Cleared.');
}
```

`updateParts` is ignored for a part that hasn't mounted yet, such as right after it was created. In that case, wait for the next user action or re-render instead.

---

## 6. Reusable Dialogs

Wrap common modal flows once and reuse them everywhere. Always `await modal.open()`, resolve the result before closing, and treat the X / "Disable This Script?" close as "cancel":

```typescript
async function confirm(title: string, message: string, opts: { confirmText?: string; danger?: boolean } = {}): Promise<boolean> {
    return new Promise<boolean>(async (resolve) => {
        let done = false;
        const finish = (value: boolean): void => { if (!done) { done = true; resolve(value); } };
        const modal = await api.v1.ui.modal.open({
            title,
            size: 'small',
            content: [
                text(message, { markdown: true }),
                hstack([
                    button('Cancel', async () => { finish(false); await modal.close(); }, { variant: 'subtle' }),
                    button(opts.confirmText ?? 'OK', async () => { finish(true); await modal.close(); },
                           { variant: opts.danger ? 'danger' : 'default' }),
                ], { spacing: 'end' }),
            ],
        });
        modal.closed.then(() => finish(false));
    });
}

async function notify(message: string, type: 'info' | 'success' | 'warning' | 'error' = 'info'): Promise<void> {
    await api.v1.ui.toast(message, { id: id('toast'), type });   // same id = updates instead of stacking
}
```

---

## 7. Wiring It Up

```typescript
api.v1.hooks.register('onScriptsLoaded', async () => {
    try {
        await render();
    } catch (err: any) {
        api.v1.error('render failed', err);
        await notify('My Script failed to load its panel.', 'error');
    }
});
```

---

## Scaling Checklist

- [ ] One `NS`; every part/extension ID goes through `id()`, and every storage key through `field()`
- [ ] Colors only from `COLOR` (real theme tokens); spacing/radii only from `SPACE` / `RADIUS`
- [ ] Border colors always in `borderColor`, never inside the `border` shorthand
- [ ] Every size, spacing, and radius on the 4px/8px grid (multiples of 4 or 8, or the `1px`/`2px`/`6px` half-steps), all in px or all in rem
- [ ] Every element comes from a factory or has its own named preset and `id()` (standard parts have no `class` prop)
- [ ] Presets in `S`, combined with `sx()`; no one-off style objects in render code
- [ ] Components built on `api.v1.ui.part.*` with an options object and variants
- [ ] One `render()`; small changes go through `updateParts` or `{{templates}}`, never a full re-render from `onChange`
- [ ] Shared flows (`confirm`, `notify`) written once
- [ ] As the script grows, keep this order in the file: tokens → presets → components → fields → views/render → actions → hooks
- [ ] If the user asks for JSX (opt-in only), wrap the `jsx` part in its own factory and share state with the rest of the script through `createStore()` (see `NovelAI_JSX_Guide.md`). Inside JSX, use `var(--theme-*)` instead of token names.
