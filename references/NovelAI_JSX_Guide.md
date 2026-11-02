# JSX UI Parts (Preact) in NovelAI Scripts

`type: 'jsx'` UI parts let a script render its own component tree with **Preact**: custom layouts, live counters, tables, SVG charts, canvas drawing, keyboard-driven widgets.

> **Opt-in only.** Use JSX only when the user explicitly asks for it. Otherwise build UI from the standard parts (see `NovelAI_UI_Component_System.md`).

**Sources:** `NovelAI_Script_Types.d.ts` (the `UIPartJSX` part) and `NovelAI_JSX_Types.d.ts` (the Preact globals, the element/attribute whitelist, event and canvas types). The JSX typings were shared in the NovelAI community, not on docs.novelai.net. The docs site only lists `api.v1.ui.part.jsx()`. Treat details the typings don't state as unverified, and test in NovelAI.

---

## 1. The Part Itself

```typescript
api.v1.ui.part.jsx({
    id: 'my-widget',                  // optional, for updateParts/removeParts
    onMount: (elem) => render(h(MyWidget, null), elem),
    captureEvents: ['keydown'],       // optional, see §6
    style: { minHeight: '120px' },    // inline styles on the host
})
```

- `onMount(elem)` is called once with the root element. Call Preact's global `render(vnode, elem)` inside it.
- The component renders inside a **shadow DOM**, isolated from the page's CSS.
- A JSX part can go anywhere a UI part can: panels, modals, windows, decoration widgets.

---

## 2. Globals Available to Scripts

These are ambient globals; there are no imports.

| Group | Globals |
| :--- | :--- |
| Preact core | `h(type, props, ...children)`, `Fragment`, `render(vnode, parent)` |
| Hooks | `useState`, `useReducer`, `useMemo`, `useRef`, `useEffect`, `useLayoutEffect`, `useCallback`, `useContext`, `useSyncExternalStore` |
| Context / portals | `createContext`, `createPortal` |
| Store (cross-tree state) | `createStore(initial)`, `useStore(store)`, `useStoreValue(store)`, `useSetStore(store)` |
| Canvas | `Path2D`, `ImageBitmap`, `createImageBitmap(dataUrlOrImageData)` |

**JSX syntax works** in scripts (tested: `<b>` and `<div><b>…</b></div>` rendered via `render(<…/>, el)` mount fine), and so does plain `h()`. Use whichever reads better.

```typescript
// h() form (always safe)
function Hello(props: { name: string }): JSX.Element {
    return h('div', { style: { padding: '8px' } }, `Hello, ${props.name}`);
}

// JSX form (equivalent)
function HelloJsx(props: { name: string }): JSX.Element {
    return <div style={{ padding: '8px' }}>Hello, {props.name}</div>;
}
```

---

## 3. State: Component Hooks vs. Stores

- **`useState` / `useReducer`** hold state local to one component, like normal Preact.
- **`createStore(initial)`** holds state shared across components *and* with the rest of the script. Any code (a hook, a regular `button` part's callback, a timer) can call `store.set(...)`, and every component using `useStore`/`useStoreValue` re-renders. This is the bridge between `api.v1` logic and the JSX tree.

```typescript
const counter = createStore(0);                          // module level

function Counter(): JSX.Element {
    const [count, setCount] = useStore(counter);         // [value, setter]
    return h('div', null,
        h('span', null, `Count: ${count} `),
        h('button', { onClick: () => setCount((c: number) => c + 1) }, '+1'),
    );
}

await api.v1.ui.update([{
    type: 'scriptPanel', id: 'jsx-demo', name: 'JSX Demo',
    content: [
        api.v1.ui.part.jsx({ id: 'counter', onMount: (elem: any) => render(h(Counter, null), elem) }),
        // a regular UI part updating the same state from outside the tree:
        api.v1.ui.part.button({ text: 'Add 10', callback: () => counter.set((c: number) => c + 10) }),
    ],
}]);
```

Stores are in memory only. Persist anything important with `api.v1.storage`/`storyStorage` and seed the store from it on load.

---

## 4. Allowed Elements and Attributes

Only whitelisted elements and attributes exist (`JSX.IntrinsicElements` in the typings). Anything else fails type-checking and should be assumed stripped at runtime.

- **Structure/text:** `div span section article aside header footer nav main p h1–h6 blockquote pre code br hr small strong em b i u s sub sup mark abbr cite kbd samp var wbr`, ruby (`ruby rt rp rb rtc`)
- **Lists/tables:** `ul ol li dl dt dd table thead tbody tfoot tr th td caption colgroup col`
- **Interactive/form:** `button details summary dialog meter progress input select option optgroup textarea label fieldset legend output datalist`
- **Media:** `img` (**`data:` URIs only**), `canvas`, `figure figcaption`, plus `address time data`
- **SVG:** `svg g defs symbol title desc path rect circle ellipse line polyline polygon text tspan textPath linearGradient radialGradient stop pattern mask clipPath marker filter` and the `fe*` filter primitives

**Not available:** `iframe`, `script`, `style`, `link`, `a`, `video`, `audio`, `object`, `embed`, `form`. Load nothing from the network.

Common attributes: `id`, `class`/`className`, `style` (object or string), `title`, `tabIndex`, `role`, `hidden`, `draggable`, `contentEditable`, ARIA (`aria-*`), `data-*`, `ref`, `key`. Form elements take their usual attributes (`value`, `checked`, `placeholder`, `disabled`, `min`/`max`/`step`, `rows`, …).

---

## 5. Styling

- Unlike regular UI parts, JSX uses **normal CSS values**, and `style` may be an object or a string. The typings don't say whether theme-token *names* (`'bg1'`) are substituted inside JSX; don't rely on that.
- For theme colors use the **`--theme-*` CSS custom properties**, which are available to JSX parts. The names follow the theme keys: `--theme-<key>`, e.g. `var(--theme-textHeadings)` (tested and confirmed), `var(--theme-bg1)`, `var(--theme-textMain)`. The keys are the ones returned by `api.v1.theme.get()` (colors: `bg0`–`bg3`, `textHeadings`, `textMain`, `textDisabled`, `textPlaceholder`, `textHighlight`, `warning`, `textPrompt`, `textUser`, `textAI`, `textEdit`, `low/mid/highIntensityColor`).
- There is no `<style>` element, so pseudo-classes and media queries aren't available. Do hover effects with state (`onMouseEnter`/`onMouseLeave` + `useState`).

---

## 6. Events

Handlers use the familiar names (`onClick`, `onInput`, `onChange`, `onKeyDown`, pointer/touch/focus/scroll events). They receive **plain snapshot objects** (`ScriptEvent`, `ScriptMouseEvent`, `ScriptKeyboardEvent`, …) with data fields like `key`, `clientX`, and `target.value`, but **no methods**: there is no `preventDefault()` or `stopPropagation()`.

- Read input values from `e.target.value` / `e.target.checked`.
- To stop keys or scroll from leaking out to NovelAI (editor hotkeys, page scroll), list them in the part's **`captureEvents`** (e.g. `['keydown', 'wheel']`). They're stopped at the shadow boundary while your handlers still receive them.
- *(Inference, not stated:)* handlers likely run in the script worker, which means a round trip. Keep per-event work light and avoid heavy work in `onMouseMove`/`onPointerMove`.

```typescript
function NameField(): JSX.Element {
    const [name, setName] = useState('');
    return h('div', null,
        h('input', { value: name, placeholder: 'Name', onInput: (e: ScriptInputEvent) => setName(String(e.target.value ?? '')) }),
        h('p', { style: { color: 'var(--theme-textDisabled)' } }, name ? `Hi, ${name}` : 'Type a name'),
    );
}
// api.v1.ui.part.jsx({ onMount: (el: any) => render(h(NameField, null), el), captureEvents: ['keydown'] })
```

---

## 7. Canvas

`<canvas>` works through a script-side wrapper. **`getContext('2d')` and `toDataURL()` return Promises**, while the drawing calls themselves are synchronous.

```typescript
function Bars(props: { values: number[] }): JSX.Element {
    const ref = useRef<ScriptCanvasElement | null>(null);
    useEffect(() => {
        (async () => {
            const ctx = await ref.current?.getContext('2d');
            if (!ctx) return;
            ctx.clearRect(0, 0, 200, 60);
            props.values.forEach((v: number, i: number) => {
                ctx.fillStyle = '#90caf9';
                ctx.fillRect(i * 22, 60 - v, 18, v);
            });
        })();
    }, [props.values]);
    return h('canvas', { ref, width: 200, height: 60 });
}
```

Images: `createImageBitmap(dataUrl)` decodes a `data:` URL (or `ImageData`) for `drawImage`. Call `bitmap.close()` when done. Network URLs are not permitted.

---

## 8. Type-Checking JSX Scripts

The JSX typings need two adjustments for `tsc`. Both are already applied in the bundled `NovelAI_JSX_Types.d.ts`: top-level `declare` modifiers, and a small shim declaring `HTMLElement` and the other element names as opaque interfaces. Don't add the DOM lib: it conflicts with the typings (`Path2D`, `ImageBitmap`) and would hide the fact that `document` doesn't exist.

```bash
cp <skill-dir>/references/NovelAI_Script_Types.d.ts ./types.d.ts
cp <skill-dir>/references/NovelAI_JSX_Types.d.ts ./jsx.d.ts
{ echo 'export {};'; cat my-script.ts; } > script.tsx
cat > tsconfig.json <<'EOF'
{ "compilerOptions": { "strict": true, "noEmit": true, "target": "ES2022", "module": "ES2022", "lib": ["ES2022"],
    "jsx": "react", "jsxFactory": "h", "jsxFragmentFactory": "Fragment" },
  "files": ["types.d.ts", "jsx.d.ts", "script.tsx"] }
EOF
tsc -p .
```

Add `NovelAI_Script_Types_Experimental.d.ts` to `files` if the script uses experimental APIs.
