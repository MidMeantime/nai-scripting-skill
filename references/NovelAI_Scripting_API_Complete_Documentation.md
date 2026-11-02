# NovelAI Scripting API - Complete Documentation

**Generated: January 2026** (updated October 2026, checked against docs.novelai.net and the official `script-types.d.ts`)

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [API Reference](#2-api-reference)
3. [Hooks](#3-hooks)
4. [Storage API](#4-storage-api)
5. [UI Extensions](#5-ui-extensions)
6. [UI Parts](#6-ui-parts)
7. [Modals and Windows](#7-modals-and-windows)
8. [Document API](#8-document-api)
9. [Generation API](#9-generation-api)
10. [Context Building](#10-context-building)
11. [Story Settings API](#11-story-settings-api)
12. [Lorebook API](#12-lorebook-api)
13. [Text-to-Speech API](#13-text-to-speech-api)
14. [Utilities API](#14-utilities-api)
15. [Messaging API](#15-messaging-api)
16. [Permissions API](#16-permissions-api)
17. [Decorations API](#17-decorations-api)
18. [Experimental API](#18-experimental-api)

---

## 1. Introduction

### NovelAI Scripting API Documentation

Welcome to the NovelAI Scripting API documentation. Scripts allow you to extend NovelAI's functionality with custom UI components, generation hooks, and document manipulation capabilities. They are written in TypeScript, a superset of JavaScript.

### Getting Started

The User Scripts modal can be found in the goose menu in the left sidebar, or, when a story is selected, the advanced tab of the right sidebar. Alt+X will also open the modal.

This modal is where you will can import, create, and modify scripts. There are two levels of scripts, account and story. Account scripts are saved to the account and will be loaded when any story is selected. Story scripts are saved to the story file and will be loaded only when that story is loaded.

### Architecture

Scripts are run executed in an isolated JavaScript interpreter in a Web Worker and can interact with NovelAI only through a set of predefined API methods. As scripts are run in a Web Worker, they don't block the UI thread and won't interrupt the main page while running. Because of this most API functions are asynchronous and return promises.

### What You Can't Do

For security and privacy reasons scripts don't have free reign over the page. There are several things they cannot do. Scripts are not allowed to make arbitrary network requests, access most user account information, directly access the DOM, or alter parts of the page not designated for scripts.

### Scripts Are Transient

Scripts can be unloaded at any time, such as when the user disables them, switches stories, or closes the User Scripts modal. Because of this scripts should avoid maintaining important state in memory. Instead they should use the Storage API to persist important data.

### Emergency Disable

If a rogue script has made the website unusable to the point where that script cannot be disabled through the User Scripts modal, you can disable all scripts by adding `?noscript=true` to the end of the URL and reloading the page. This will prevent any scripts from loading, allowing you to access the User Scripts modal and disable or remove the problematic script.

### Unhandled Promise Rejections

For various technical reasons, unhandled rejected promises in scripts will not show any error message in the UI or console. To avoid silent failures, make sure to properly handle errors in your scripts using `.catch` on promises or awaiting them in a try/catch block.

### Example Scripts

Here's a few example scripts to get you started:

* **Scripting Demo Scenario** - A scenario containing an example script demonstrating various scripting features
* **Smart Summarizer** - Adds a right click option to summarize selected text in the editor
* **Bookmarks** - A script that lets you create "bookmarks" in a story
* **Find & Replace** - A script that adds a Find & Replace panel to the UI
* **Retry Harder** - A script that provides an alternative retry button with special prompting

More example scripts can be found in the novelai-script-examples repository on GitHub.

### Type Definitions

An m.ts file containing type definitions for the scripting API can be found at http://novelai.net/scripting/types/script-types.d.ts. This file can be used to provide type information and autocompletion in editors that support it.

---

## 2. API Reference

The API Reference provides comprehensive documentation of all available API functions and namespaces. The NovelAI Scripting API is versioned, with v1 being the current stable version accessed via `api.v1`.

### Core API Structure

```
api.v1
├── an (Author's Note API)
├── buildContext()
├── clipboard
├── commentBot
├── config
├── createCancellationSignal()
├── createRolloverHelper()
├── document
├── editor
├── error()
├── file
├── generate()
├── generateWithStory()
├── generationParameters
├── historyStorage
├── hooks
├── log()
├── logprobs
├── lorebook
├── maxTokens()
├── memory
├── messaging
├── permissions
├── prefill
├── random
├── rolloverTokens()
├── script
├── storage
├── story (id(), title.get/set, description.get/set)
├── storyStorage
├── systemPrompt
├── tempStorage
├── theme
├── timers
├── tokenizer
├── ts
├── tts
├── ui
└── uuid()
```

### Key Namespaces

#### api.v1.an (Author's Note)
- `get()` - Get current author's note text
- `set(text)` - Set author's note text (requires storyEdit permission)

#### api.v1.clipboard
- `writeText(text)` - Write text to clipboard (requires clipboardWrite permission)

#### api.v1.commentBot
- `get()` - Get current comment bot configuration
- `update(data)` - Update comment bot configuration

#### api.v1.config
- `get(key)` - Get a configuration value by key

#### api.v1.file
- `prompt(options)` - Prompt user to select a file (requires fileInput permission)
- `save(filename, content)` - Prompt user to save a file (requires fileDownload permission)

#### api.v1.memory
- `get()` - Get current memory text
- `set(text)` - Set memory text (requires storyEdit permission)

#### api.v1.prefill
- `get()` - Get current prefill text
- `getDefault()` - Get the default prefill for the current story mode
- `set(text)` - Set prefill text; empty string or undefined restores the default (requires storyEdit permission)

#### api.v1.systemPrompt
- `get()` - Get current system prompt
- `getDefault()` - Get the default system prompt for the current model and story mode
- `set(text)` - Set system prompt; empty string or undefined restores the default (requires storyEdit permission)

#### api.v1.story
- `id()` - Get the current story ID
- `title.get()` / `title.set(title)` - Read or change the story title
- `description.get()` / `description.set(description)` - Read or change the story description

#### api.v1.theme
- `get()` - Get the active theme: `{ name, fonts: { default, code, field, headings }, colors: { bg0…bg3, textHeadings, textMain, … } }`. Values are user-defined and can be in any CSS format.

#### api.v1.script (Script Info & Token Budget)
Static, read-only information about the running script, plus helpers for the script generation rate limits (see Section 9):
- `id` - The script's ID
- `name` - The script's name
- `author` - The script's author
- `description` - The script's description
- `version` - The version of the running script
- `memoryLimit` - The script's memory limit, in bytes
- *(The token-budget helpers below are synchronous: they return numbers directly, except the `waitFor…` ones, which return Promises.)*
- `getAllowedInput()` - Number of input tokens currently available
- `getAllowedOutput()` - Number of output tokens currently available
- `getTimeUntilAllowedInput(minTokens)` - Time (ms) until at least `minTokens` input tokens are available
- `getTimeUntilAllowedOutput(minTokens)` - Time (ms) until at least `minTokens` output tokens are available
- `waitForAllowedInput(minTokens)` - Promise that resolves when at least `minTokens` input tokens are available
- `waitForAllowedOutput(minTokens)` - Promise that resolves when at least `minTokens` output tokens are available
- `countUncachedInputTokens(messages)` - Count how many input tokens in a `Message[]` prompt would count against the input limit, accounting for caching

### Utility Functions

#### Logging
```javascript
api.v1.log(...messages)  // Log messages to console
api.v1.error(...messages)  // Log error messages
```

#### UUIDs
```javascript
api.v1.uuid()  // Generate a new UUID
```

#### Model Information
```javascript
api.v1.maxTokens(model)  // Get max tokens for model
api.v1.rolloverTokens(model)  // Get rollover tokens for model
```

#### Larry
```javascript
// Show Larry with a question and optional response buttons.
// With no options, Yes/No buttons are shown (Yes triggers normal Larry generation).
api.v1.ui.larry.help({
  question: "What would you like to do?",
  options: [
    { text: "Generate more", callback: () => api.v1.editor.generate() },
    { text: "Cancel", callback: () => {} }
  ]
})
```

---

## 3. Hooks

Hooks allow your scripts to respond to events in the generation pipeline, enabling you to modify context, alter responses, and control generation behavior. All the hooks receive their parameters as a single object.

### Available Hooks

#### onGenerationRequested
The first hook that triggers when a user generates text. The generation has not yet happened and context has not yet been built. This hook could be used to prevent generation and take full control over the generation flow or to prepare things for later hooks.

#### onBeforeContextBuild
Happens just before context is built. Provides an opportunity to temporarily modify or disable context objects like Lorebook entries, Memory, etc. The `dryRun` parameter indicates if this is for actual generation or just for viewing.

#### onContextBuilt
Happens whenever context is built. You can return a modified array of messages to alter the context that will be used for generation. Only happens when generating with models that use the OpenAI-like completions endpoint.

#### onResponse
Happens when response data is received for a generation request. You can return modified text to alter what will be placed in the editor. You can also provide altered token ids and logprobs.

If streaming is enabled, there will be multiple onResponse calls for each generation. The final onResponse will have the `final` param set to true.

You can set `seenData` on the return object to hold part or all of a response from being sent up the chain.

#### onGenerationEnd
Triggers after a generation has successfully completed or been cancelled. When this hook is called, the generation is fully finished, the editor is unlocked, and generation is no longer blocked.

#### onScriptsLoaded
Triggers once after all scripts have been loaded and initialized. This is a good place to perform any setup that would fail if done at the top level of the script, such as calling buildContext.

#### onLorebookEntrySelected
Triggers whenever a Lorebook entry or category is selected in the Lorebook. The hook is provided the id of the selected entry or category.

#### onTextAdventureInput
Triggers whenever input is submitted via the Text Adventure input box. Return `{ inputText }` to replace the input (an empty string adds nothing), `mode` to change it (`'action' | 'dialogue' | 'story'`), or `stopGeneration: true` to prevent generation. Newlines in `inputText` are replaced with spaces.

#### onHistoryNavigated
Triggers whenever the user or a script navigates the document history through undo/redo/retry/jump to history node. It receives `{ nodeId: number, previousNodeId: number, direction: 'forward' | 'backward' | 'both', distance, cause: 'undo' | 'redo' | 'retry' | 'jump' }`. It does not fire when a new node is created by ordinary editing or generation.

#### onDocumentConvertedToText
Triggers whenever a document is converted to text format, generally for the purposes of generation context building. You can return modified sections to alter the text.

### Hook Registration

```javascript
api.v1.hooks.register('onGenerationRequested', async (params) => {
  // Your hook logic here
  return {
    stopGeneration: false,  // Optional: prevent generation
    stopFurtherScripts: false  // Optional: prevent other scripts
  };
});
```

### Hook Execution Order

Scripts execute their hooks in the same order as they are listed in the User Scripts modal. All account scripts are executed in order, then all story scripts.

### Controlling Hook Propagation

- `stopFurtherScripts`: Set to true to prevent a hook from being called for any scripts after this one
- `stopGeneration`: For `onGenerationRequested`, `onContextBuilt`, and `onResponse` (and `onTextAdventureInput`), set to true to immediately prevent or cancel a generation. No further hooks fire for any script.

Each script can have only one callback per hook. Registering the same hook again replaces the previous callback. `api.v1.hooks.unregister(name)` and `api.v1.hooks.isRegistered(name)` are also available.

---

## 4. Storage API

The Storage API provides persistent data storage for scripts at both the story and account level. Each script gets its own storage separate from other scripts. Data is stored as key-value pairs.

### Storage Types

#### api.v1.storage
Standard storage for scripts. Stores data with the script. Where data is stored depends on whether the script is an account or story script. Account scripts are limited to 4 MB per script.

#### api.v1.storyStorage
Always stores data in the current story regardless of script type. Note that for story scripts this is separate from `api.v1.storage`.

#### api.v1.historyStorage
Functions like storyStorage but is aware of document history. When a value is set, it's set at a specific point in the document history. If the document is undone to before that history node, values will revert.

Values live on **generation nodes** only (history nodes created by a generation). `set()` writes to the closest generation node at or above the current node. If no generation node is an ancestor yet, it writes to the story root. `get`/`has`/`list` search upward through ancestor generation nodes and return the closest match. `remove()` only clears the value on the targeted node, so an ancestor's value can show through afterward. The optional `nodeId` argument must be a real node, and for `set`/`setIfAbsent`/`remove` it must be a generation node; otherwise the call throws.

#### api.v1.tempStorage
Temporary storage that persists only for the current session and is cleared when the story is closed. Use this for displaying temporary UI state using storage keys in UI Parts.

### Basic Operations

All storage APIs share the same basic structure:

```javascript
// Set a value
await api.v1.storage.set('key', value);

// Get a value
let value = await api.v1.storage.get('key');

// Get with default
let value = await api.v1.storage.getOrDefault('key', defaultValue);

// Check if key exists
let exists = await api.v1.storage.has('key');

// Remove a value
await api.v1.storage.remove('key');

// List all keys
let keys = await api.v1.storage.list();

// Set if absent
let wasSet = await api.v1.storage.setIfAbsent('key', value);
```

### History-Aware Storage

History storage automatically updates when document history changes:

```javascript
// At history point A
await api.v1.historyStorage.set('turn-count', 1);

// User generates text, moving to point B
await api.v1.historyStorage.set('turn-count', 2);

// User undoes back to point A
let count = await api.v1.historyStorage.get('turn-count');  // Returns 1
```

### Limitations of History Storage

- Only handles cases where undo/redo are used
- Manual document edits won't automatically revert values
- Only marks history points when a generation occurs

### Temporary Storage with UI Parts

```javascript
// Set a temporary value
await api.v1.tempStorage.set('example-string', 'Hello, world!');

// Register a UI Part that displays the temporary value
await api.v1.ui.register([{
  type: 'scriptPanel',
  name: 'Temporary Storage Example',
  content: [{
    type: 'text',
    text: '{{temp:example-string}}'
  }]
}]);

// Update the value (UI will reflect the change)
await api.v1.tempStorage.set('example-string', 'Updated text!');
```

### Storage Keys in UI Parts

Inputs with a `storageKey` and `{{key}}` templates in `text` parts bind to storage by prefix:

| Prefix | Storage |
| :--- | :--- |
| *(none)* | `api.v1.storage` |
| `story:` | `api.v1.storyStorage` |
| `history:` | `api.v1.historyStorage` |
| `temp:` | `api.v1.tempStorage` |

In code, use the bare key with the matching API (e.g. `storageKey: 'temp:draft'` ↔ `api.v1.tempStorage.get('draft')`).

### Data Types

Stored data is immediately serialized as JSON, so anything not serializable will be lost or altered. Only JSON-serializable data can be stored. `historyStorage` methods also accept an optional trailing `nodeId` to read or write at a specific history node.

---

## 5. UI Extensions

UI Extensions allow you to add custom interface elements to NovelAI. These extensions can appear in various locations and provide interactive controls for your scripts.

### Extension Types

#### Context Menu Buttons
Appear in the context menu when right-clicking in the editor. The callback receives `{ selection }` (a `DocumentSelection`). It does **not** receive the selected text, so use `api.v1.document.textFromSelection(selection)` to get it.

```javascript
api.v1.ui.register([{
  type: 'contextMenuButton',
  text: 'Example Button',
  callback: async ({ selection }) => {
    const text = await api.v1.document.textFromSelection(selection);
    api.v1.log('Selected text:', text);
  }
}]);
```

#### Toolbar Buttons
Appear in a new toolbar above the normal editor toolbar.

```javascript
api.v1.ui.register([{
  type: 'toolbarButton',
  text: 'Example Button',
  callback: () => {
    api.v1.log('Example toolbar button clicked.');
  }
}]);
```

#### Toolbox Options
Add options to the Writer's Toolbox. The callback runs when the user clicks "Adjust" with the tool selected, and receives `{ selection, text }`. Return the modified text.

```javascript
api.v1.ui.register([{
  type: 'toolboxOption',
  name: 'Custom Tool',
  content: [{
    type: 'textInput',
    storageKey: 'tool-input',
  }],
  callback: ({ text }) => {
    api.v1.log('Custom tool executed.');
    return { text: text + ' New text.' };
  }
}]);
```

#### Script Panels
Collapsible panels added between the document and the controls. Only one can be open at a time; `api.v1.ui.openPanel(id)` / `api.v1.ui.closePanel()` control it.

```javascript
api.v1.ui.register([{
  type: 'scriptPanel',
  name: 'Example Panel',
  content: [
    {
      type: 'text',
      text: 'This is an example script panel.'
    },
    {
      type: 'button',
      text: 'Click Me',
      callback: () => {
        api.v1.log('Button in script panel clicked.');
      }
    }
  ]
}]);
```

#### Sidebar Panels
Added to the right sidebar when a story is open to a new "…" tab.

```javascript
api.v1.ui.register([{
  type: 'sidebarPanel',
  name: 'Example Sidebar',
  content: [
    {
      type: 'text',
      text: 'This is an example sidebar panel.'
    }
  ]
}]);
```

#### Lorebook Panels
Appear in the "Script" tab of Lorebook entries and categories.

```javascript
api.v1.hooks.register('onLorebookEntrySelected', async ({ entryId, categoryId }) => {
  api.v1.ui.update([{
    type: "lorebookPanel",
    id: 'lore-info-panel',
    name: 'Lore Info',  // required by the type
    content: [{
      type: 'text',
      text: `ID: ${entryId ?? categoryId}`
    }]
  }]);
});
```

### Updating and Removing Extensions

```javascript
// Update an extension (requires ID)
await api.v1.ui.update([{
  type: 'scriptPanel',
  id: 'my-panel',
  content: [/* updated content */]
}]);

// Remove extensions (takes an array of IDs)
await api.v1.ui.remove(['my-panel']);

// Update or remove individual UI parts (by part id) inside panels, modals, and windows
await api.v1.ui.updateParts([{ type: 'text', id: 'status-text', text: 'Done!' }]);
// (updateParts is ignored if the part hasn't mounted yet, e.g. called right after creating it)
await api.v1.ui.removeParts(['status-text']);
```

`api.v1.ui.update()` can also create an extension that doesn't exist yet, as long as it has an `id`. Each extension type also has a helper that fills in `type` for you: `api.v1.ui.extension.scriptPanel({...})`, `.sidebarPanel`, `.lorebookPanel`, `.toolbarButton`, `.contextMenuButton`, `.toolboxOption`. UI parts have the same kind of helper: `api.v1.ui.part.button({...})`, `.text`, `.row`, etc. Panels, toolbar buttons, and toolbox options accept an `iconId` (see `IconId` in the type definitions).

---

## 6. UI Parts

UI Parts are the building blocks for creating user interfaces in your scripts. They can be used in UI Extensions, Modals, and Windows.

### Layout Components

#### Row
Arranges child components horizontally (a flex row).

```javascript
{
  type: 'row',
  spacing: 'space-between',  // Optional: 'start' | 'center' | 'end' | 'space-between' | 'space-around' (NOT a number)
  alignment: 'center',  // Optional vertical alignment: 'start' | 'center' | 'end'
  wrap: false,  // Optional: allow items to wrap
  content: [
    { type: 'text', text: 'First Item' },
    { type: 'text', text: 'Second Item' }
  ]
}
```

#### Column
Arranges child components vertically.

```javascript
{
  type: 'column',
  spacing: 'start',  // Optional: 'start' | 'center' | 'end' | 'space-between' | 'space-around' (NOT a number)
  alignment: 'start',  // Optional horizontal alignment: 'start' | 'center' | 'end' (NOT 'left'/'right')
  content: [
    { type: 'text', text: 'First Item' },
    { type: 'text', text: 'Second Item' }
  ]
}
```

#### Box
Places child components in a bordered box with background color.

```javascript
{
  type: 'box',
  content: [
    { type: 'text', text: 'This is inside a box.' }
  ]
}
```

#### Container
A simple wrapper for applying custom styles.

```javascript
{
  type: 'container',
  style: {
    border: '1px solid #ff0000',
    padding: '10px'
  },
  content: [
    { type: 'text', text: 'Custom-styled container.' }
  ]
}
```

### Input Components

All inputs accept `storageKey` (two-way binding: typing saves to storage automatically, and changing the stored value updates the input; see the prefix table in Section 4), `initialValue`, `label`, `disabled`, and `id`. Text and number inputs also take `placeholder`.

#### Text Input
Single-line text input. `onSubmit` fires on Enter.

```javascript
{
  type: 'textInput',
  storageKey: 'user-value',
  placeholder: 'Enter text...',
  onChange: (value) => {
    api.v1.log('User changed input to: ' + value);
  },
  onSubmit: (value) => {
    api.v1.log('User submitted: ' + value);
  }
}
```

#### Multiline Text Input
Multiple-line text input area. `onSubmit` fires on Ctrl+Enter. There is no `rows` prop, so set the height through `style`.

```javascript
{
  type: 'multilineTextInput',
  storageKey: 'user-multiline-value',
  placeholder: 'Enter text...',
  style: { minHeight: '100px' },
  onChange: (value) => { /* ... */ },
  onSubmit: (value) => { /* ... */ }
}
```

#### Number Input
Numeric input field. It has no `min`/`max`/`step` props (use `sliderInput` for a bounded range), and `onChange`/`onSubmit` receive the value as a **string**.

```javascript
{
  type: 'numberInput',
  storageKey: 'user-number',
  onChange: (value) => { const n = Number(value); /* ... */ },
  onSubmit: (value) => { /* ... */ }
}
```

#### Slider Input
Slider for numeric values (with direct value editing). `min` and `max` are required. Optional: `step`, `preventDecimal`, `uncapMin`/`uncapMax`, `prefix`/`suffix`, `changeDelay`, `defaultValue`.

```javascript
{
  type: 'sliderInput',
  storageKey: 'slider-value',
  min: 0,
  max: 100,
  step: 1,
  onChange: (value) => { /* value is a number */ }
}
```

#### Checkbox Input
Boolean checkbox.

```javascript
{
  type: 'checkboxInput',
  storageKey: 'user-checkbox',
  label: 'Enable feature',
  onChange: (value) => {
    api.v1.log('Checkbox is now: ' + value);
  }
}
```

### Display Components

#### Text
Display text with optional markdown formatting.

```javascript
{
  type: 'text',
  text: '# Heading\nThis is **bold** and this is *italic*.',
  markdown: true,
  noTemplate: false  // Set to true to disable {{key}} substitution
}
```

Text within `{{curly braces}}` will be treated as storage keys and replaced with stored values (unprefixed = `api.v1.storage`). Use `{{history:key}}`, `{{story:key}}`, or `{{temp:key}}` for specific storage types. URLs in markdown do not become clickable links.

#### Image
Display an image (Data URLs only).

```javascript
{
  type: 'image',
  src: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...',
  alt: 'Example Image',
  height: 200,
  width: 200
}
```

#### Button
Clickable button.

```javascript
{
  type: 'button',
  text: 'Click Me',
  iconId: 'play',  // Optional icon (see IconId)
  disabled: false,
  disabledWhileCallbackRunning: true,  // note the "d": the type defines `disabledWhileCallbackRunning`
  callback: () => {
    api.v1.log('Button was clicked!');
  }
}
```

#### Code Editor
Monaco code editor with syntax highlighting. `id` is **required** for this part.

```javascript
{
  type: 'codeEditor',
  id: 'my-code-editor',
  storageKey: 'code-content',
  language: 'javascript',  // 'typescript' | 'javascript' | 'json' | 'markdown' | 'html' | 'css' | 'plaintext'
  height: 300,  // px number or CSS string
  onChange: (value) => { /* ... */ }
}
```

#### Collapsible Section
Expandable/collapsible section.

```javascript
{
  type: 'collapsibleSection',
  title: 'Advanced Options',
  initialCollapsed: true,  // Optional
  storageKey: 'section-collapsed',  // Persists the collapsed state
  content: [
    { type: 'text', text: 'Hidden content' }
  ]
}
```

#### JSX (Preact)
*Opt-in only: use JSX only when the user explicitly asks for it.* Both JSX syntax and `h()` work.

A custom component rendered with Preact (`type: 'jsx'`, or `api.v1.ui.part.jsx({...})`), inside a shadow DOM. `onMount(elem)` receives the root element. Render into it with the global `render(h(MyComponent, null), elem)`. Preact globals (`h`, `render`, hooks, `createStore`) are ambient, so there are no imports. Only whitelisted elements and attributes are allowed: no `iframe`/`script`/`style`/`a`, and `img` takes `data:` URIs only. Event handlers get plain snapshot objects without `preventDefault()`, so use `captureEvents` (e.g. `['keydown', 'wheel']`) to stop events at the shadow boundary. Theme colors come from the `--theme-*` CSS custom properties.

```javascript
const counter = createStore(0);
function Counter() {
  const [n, setN] = useStore(counter);
  return h('button', { onClick: () => setN((c) => c + 1) }, `Clicked ${n}`);
}
{
  type: 'jsx',
  id: 'my-widget',
  onMount: (elem) => render(h(Counter, null), elem),
  captureEvents: ['keydown'],
  style: { minHeight: '40px' }
}
```

**Full details:** the whitelist, stores vs. hooks, events, canvas, and type-checking are in **`NovelAI_JSX_Guide.md`**, with typings in `NovelAI_JSX_Types.d.ts`.

### Styling

Most UI Parts support the `style` property with CSS properties in camelCase. These are inline styles, so pseudo-classes (`:hover`) and media queries are not possible, and URLs are stripped from style values.

```javascript
{
  type: 'text',
  text: 'Styled text',
  style: {
    backgroundColor: 'bg1',      // theme token — adapts to active theme
    color: 'textHeadings',        // theme token
    padding: '10px',
    borderRadius: '5px'
  }
}
```

#### Theme Tokens

Use these string values directly in any `style` property instead of hardcoded hex colors. NovelAI automatically replaces them with the user's active theme values at render time:

| Token | Role |
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

> **⚠️ Note on `'primary'`**: NovelAI does **NOT** have a `'primary'` or `'error'` theme token. Using `color: 'primary'` or `backgroundColor: 'primary'` produces invalid CSS. For active/highlighted surfaces use `'bg3'`, for high-contrast accents use `'textHeadings'`, or supply explicit hex/rgba color strings (e.g. `'#90caf9'`).

#### Style Presets and Factory Functions

To avoid duplicating inline style blocks throughout the script, define style constants and factory functions once at the top:

```typescript
// ── Style presets ──────────────────────────────────────────────
const CARD_STYLE: Record<string, string> = {
    backgroundColor: 'bg1',
    border: '1px solid bg2',
    borderRadius: '6px',
    padding: '10px',
    margin: '6px 0',
};

const DANGER_STYLE: Record<string, string> = { ...CARD_STYLE, borderColor: 'warning' };

// ── Factory functions ──────────────────────────────────────────
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

// ── Usage ──────────────────────────────────────────────────────
makeButton('Save', handleSave);
makeButton('Delete', handleDelete, { backgroundColor: 'warning' });

{
  type: 'container' as const,
  style: CARD_STYLE,
  content: [/* children */]
} as any
```

> **Important:** `row`/`column` `spacing` is a string justification value (`'start'`, `'center'`, `'end'`, `'space-between'`, `'space-around'`), **not** a pixel number. To set the gap between children, put `margin` on the child elements.



## 7. Modals and Windows

Modals and Windows provide a way to create custom dialog boxes and floating windows in NovelAI.

Modals are centered and block the rest of the UI until closed. Windows float, can be moved, and let the user keep using the page. Both `open()` calls return a **Promise** resolving to a handle `{ update(options), close(), isClosed(), closed }`, so `await` them before using the handle.

### Creating a Modal

```javascript
let modal = await api.v1.ui.modal.open({
  title: 'Example Modal',
  content: [
    {
      type: 'text',
      text: 'This is an example modal.'
    },
    {
      type: 'button',
      text: 'Close',
      callback: () => modal.close()
    }
  ],
  size: 'small'  // 'small' | 'medium' | 'large' | 'full'. Other options: hasMinimumHeight, fillWidth, id
});

// Wait for modal to close
await modal.closed;
api.v1.log('Modal was closed');
```

### Creating a Window

```javascript
let wndw = await api.v1.ui.window.open({
  title: 'Example Window',
  content: [
    {
      type: 'text',
      text: 'This is an example window.'
    }
  ],
  defaultHeight: 300,
  defaultWidth: 400,
  defaultX: 100,  // Optional position
  defaultY: 100,
  resizable: true  // Optional; also minWidth/minHeight/maxWidth/maxHeight
});

// Update window content
await wndw.update({
  content: [
    { type: 'text', text: 'Updated content!' }
  ]
});

// Close programmatically
await wndw.close();

// Wait for window to close (resolves however it was closed)
await wndw.closed;
```

### Disable This Script Button

All modals and windows created by scripts have a "Disable This Script?" button (bottom right of modals, title bar of windows). Clicking it immediately disables the script that created the modal or window, and closes that modal or window along with any others the script opened.

---

## 8. Document API

The Document API provides methods for reading and manipulating the story document.

### Understanding Document Structure

#### Sections
The document is divided into sections, which represent paragraphs. Each section has:

```javascript
{
  text: string,
  origin: [{ position: number, length: number, data: string }],
  formatting: [{ position: number, length: number, data: string }],
  source: string | undefined
}
```

- `origin[].data`: `'user' | 'ai' | 'edit' | 'prompt' | 'script'` (`append()` uses `'script'`)
- `formatting[].data`: `'bold' | 'italic' | 'underline' | 'strikethrough' | 'inline_code'`
- `source`: `'story' | 'action' | 'dialogue' | 'instruction'` (used for text adventure inputs and instructions)

Section IDs are large numeric IDs, **not** indexes. Use `sectionIds()` or `scan()` to get them.

#### Selections
Document selections represent a range of text:

```javascript
{
  from: { sectionId: number, offset: number },
  to: { sectionId: number, offset: number },
  anchor: { sectionId: number, offset: number },
  head: { sectionId: number, offset: number }
}
```

### Reading Document Content

#### Scanning the Document

```javascript
// Resolves to [{ sectionId, section, index }, ...]; the callback is optional.
// An optional second argument { from?: sectionId, to?: sectionId } limits the range.
let allSections = await api.v1.document.scan((sectionId, section, index) => {
  api.v1.log(`Section ${index} (ID: ${sectionId}): ${section.text}`);
});
```

#### Getting Section IDs

```javascript
let sectionIds = await api.v1.document.sectionIds();
api.v1.log(`The document has ${sectionIds.length} sections.`);
```

#### Getting Text from Selection

```javascript
let selectionText = await api.v1.document.textFromSelection({
  from: selection.from,
  to: selection.to
});
```

### Modifying Document Content

All modification methods require the `documentEdit` permission.

#### Appending Text

```javascript
// Simple append
await api.v1.document.append('This text will be added to the end.');

// Append paragraph with formatting
await api.v1.document.appendParagraph({
  text: 'This is a new paragraph.',
  origin: [{ position: 0, length: 4, data: 'user' }],
  formatting: [{ position: 10, length: 4, data: 'bold' }]
});

// Append multiple paragraphs
await api.v1.document.appendParagraphs([
  { text: 'First paragraph' },
  { text: 'Second paragraph' }
]);
```

#### Inserting Text

```javascript
// Insert after a specific section (0 = start of document)
await api.v1.document.insertParagraphAfter(0, {
  text: 'This paragraph was inserted at the start.'
});

// Insert multiple paragraphs
await api.v1.document.insertParagraphsAfter(sectionId, [
  { text: 'First inserted paragraph' },
  { text: 'Second inserted paragraph' }
]);
```

#### Updating Paragraphs

```javascript
// Update single paragraph
await api.v1.document.updateParagraph(sectionId, {
  text: 'Updated text'
});

// Update multiple paragraphs
await api.v1.document.updateParagraphs([
  { sectionId: id1, section: { text: 'Updated 1' } },
  { sectionId: id2, section: { text: 'Updated 2' } }
]);
```

#### Deleting Paragraphs

```javascript
// Delete single paragraph
await api.v1.document.removeParagraph(sectionId);

// Delete multiple paragraphs
await api.v1.document.removeParagraphs([id1, id2, id3]);
```

### Document History

```javascript
// Undo
await api.v1.document.history.undo();

// Redo (optionally to a specific child node: redo(nodeId))
await api.v1.document.history.redo();

// Jump to specific history node
await api.v1.document.history.jump(nodeId);

// Get current node ID
let currentNode = await api.v1.document.history.currentNodeId();

// Get previous node ID
let previousNode = await api.v1.document.history.previousNodeId();

// Get most recent generation node
let lastGen = await api.v1.document.history.mostRecentGenerationNodeId();

// Get node state
let state = await api.v1.document.history.nodeState(nodeId);
```

---

## 9. Generation API

Scripts can generate text using the `api.v1.generate` function. Currently only supports chat-style generation with models that use the OpenAI-like completions endpoint.

### Model Identifiers

Two model strings are currently valid for chat-style generation:

- `"glm-4-6"`: the GLM 4.6 base model, available on all tiers. **Use this by default.** It follows instructions very well, which suits most script work: summaries, extraction, classification, JSON/structured output, rewrites to spec, and lorebook or memory generation.
- `"xialong-v1"`: **Xialong**, NovelAI's storytelling finetune of GLM 4.6 (released March 31, 2026). It uses the same message format but is tuned for **story prose generation, not instruction-following**, so use it only when the script's output is story continuation or prose. It is **Opus-only**, and requests fail for non-Opus users. Suggested starting sampling: `temperature: 0.85, top_p: 0.95, top_k: 250, min_p: 0.0`.

Both have 28,672 tokens of context plus an 8,192-token rollover window. Query these at runtime with `await api.v1.maxTokens(model)` / `await api.v1.rolloverTokens(model)` rather than hardcoding them.

**Choosing a model:** hardcode `glm-4-6` for instruction-style tasks. For prose tasks, use `xialong-v1` only if the user's story is already set to it. That setting proves the user has Opus, and it respects their choice. Never upgrade `glm-4-6` to `xialong-v1` on your own.

```javascript
// Instruction-style task: always the base model
const summary = await api.v1.generate(messages, { model: 'glm-4-6', max_tokens: 200 });

// Prose task: follow the story's model only if it's Xialong (implies Opus), else the base model
const { model: storyModel } = await api.v1.generationParameters.get();
const proseModel = storyModel === 'xialong-v1' ? 'xialong-v1' : 'glm-4-6';

let response = await api.v1.generate(messages, {
  model: proseModel,
  max_tokens: 250,
  temperature: 0.85,
  top_p: 0.95,
  top_k: 250,
  min_p: 0.0
});
```

### Basic Generation

```javascript
let response = await api.v1.generate(
  [
    { role: 'system', content: 'You are a helpful assistant.' },
    { role: 'user', content: 'Where am I?' }
  ],
  {
    model: 'glm-4-6',
    temperature: 0.8,
    max_tokens: 100
  }
);

api.v1.log('Generated text: ' + response.choices[0].text);
```

### Generation Parameters

Available parameters:
- `model` (string, required)
- `temperature` (number)
- `max_tokens` (number)
- `top_p` (number)
- `top_k` (number)
- `frequency_penalty` (number)
- `presence_penalty` (number)
- `min_p` (number)
- `stop` (array of strings)
- `logit_bias` (`Record<number, number>`, keyed by token ID)
- `enable_thinking` (boolean)

The response is `{ choices: GenerationChoice[] }` (currently always one choice). Each choice has `text`, `index`, `token_ids`, and optionally `finish_reason`, `logprobs`, and reasoning fields (`isReasoning`, `parsedReasoning`, `parsedContent`). Messages are `{ role: 'system' | 'user' | 'assistant', content?: string, reasoning?: string }`.

### Streaming Generation

All `api.v1.generate` requests stream by default. Pass a callback as the third argument to receive chunks as they arrive.

```javascript
await api.v1.generate(
  [{ role: 'user', content: 'Tell me a story...' }],
  { model: 'glm-4-6' },
  (choices, final) => {
    for (let choice of choices) {
      api.v1.log('Received: ' + choice.text);
    }
    if (final) {
      api.v1.log('Generation complete.');
    }
  }
);
```

### Blocking and Background Generation

```javascript
// Background generation (allows user interaction)
let response = await api.v1.generate(
  messages,
  params,
  callback,
  'background'  // or 'blocking' (default)
);
```

### Cancellation

```javascript
let signal = await api.v1.createCancellationSignal();

// Start generation
let promise = api.v1.generate(
  messages,
  params,
  callback,
  'background',
  signal
);

// Cancel after 5 seconds (the global setTimeout is not available in scripts)
await api.v1.timers.setTimeout(() => { signal.cancel(); }, 5000);

// Cancellation may not be immediate, but the generation stops as soon as possible.
// signal.cancelled tells you whether it was cancelled; signal.dispose() frees it.
```

### Generation with Story Context

```javascript
// Messages are appended after the built story context. Signature:
// generateWithStory(messages, params, options?, callback?, behaviour?, signal?)
// Note the extra `options` argument (contextLimitReduction, position, suppressScriptHooks)
// before the callback. The positions differ from generate().
let response = await api.v1.generateWithStory(
  [{ role: 'user', content: 'Summarize what happened.' }],
  { model: 'glm-4-6', max_tokens: 150 }
);
```

### Editor Generation

```javascript
// Trigger generation as if user clicked "Send" (resolves when generation starts)
if (!(await api.v1.editor.isBlocked())) {
  await api.v1.editor.generate();
}
```

### Generation Limit

Scripts have several limits on how frequently and how much they can generate. These limits are shown in the script diagnostics tab in the UI for debugging.

- **Editor generations** (`api.v1.editor.generate`): only three calls are allowed without user interaction in between. After three, further calls are rejected until the user generates manually or interacts with UI created by the script.
- **Output tokens** (`api.v1.generate`): currently 2,048 output tokens every 4 minutes, per script. Used tokens are placed in a "bucket" and returned once 4 minutes have passed *and* the user has interacted with the script's UI or generated manually.
- **Input tokens** (`api.v1.generate`): currently double the maximum allowed context size for the model and current subscription tier, every 6 minutes. Only new (uncached) input tokens count. Tokens are treated as cached when they match the start of a previous prompt, measured to a resolution of 64 tokens — so reusing the start of prior prompts (e.g. via rollover logic) helps stay within the limit. Returned after 6 minutes and user interaction.

Use the `api.v1.script` token-budget helpers (`getAllowedInput`/`getAllowedOutput`, `getTimeUntilAllowedInput`/`getTimeUntilAllowedOutput`, `waitForAllowedInput`/`waitForAllowedOutput`, `countUncachedInputTokens`) to work within these limits, and `api.v1.createRolloverHelper` to manage a sliding context window.

---

## 10. Context Building

The `buildContext` method generates the same kind of context that would be used for a standard editor generation.

### Basic Usage

```javascript
let context = await api.v1.buildContext();

for (let message of context) {
  api.v1.log(`Role: ${message.role}`);
  api.v1.log(`Content: ${message.content}`);
}
```

### Advanced Options

```javascript
let context = await api.v1.buildContext({
  contextLimitReduction: 100,  // Reduce context by 100 tokens
  position: { sectionId: 123, offset: 50 },  // Build as if generating here
  suppressScriptHooks: 'all',  // 'self' or 'all' (skips onContextBuilt hooks)
  forGeneration: false  // true if the context will be used for a generation (affects caching and other scripts)
});
```

### Safe Usage

Don't call `buildContext` during script initialization. Use the `onScriptsLoaded` hook instead:

```javascript
api.v1.hooks.register('onScriptsLoaded', async () => {
  let context = await api.v1.buildContext();
  api.v1.log(`Context has ${context.length} messages`);
});
```

---

## 11. Story Settings API

Access and modify story settings related to text generation.

### Memory

```javascript
// Get memory
let memory = await api.v1.memory.get();

// Set memory (requires storyEdit permission)
await api.v1.memory.set('Character: Maria - A brave knight...');
```

### Author's Note

```javascript
// Get author's note
let an = await api.v1.an.get();

// Set author's note (requires storyEdit permission)
await api.v1.an.set('[Style: descriptive and atmospheric]');
```

### System Prompt

```javascript
// Get system prompt
let prompt = await api.v1.systemPrompt.get();

// Set system prompt (requires storyEdit permission)
await api.v1.systemPrompt.set('Write good please.');
// Empty string uses default system prompt
await api.v1.systemPrompt.set('');
```

### Prefill

```javascript
// Get prefill
let prefill = await api.v1.prefill.get();

// Set prefill (requires storyEdit permission)
await api.v1.prefill.set('Here\'s a list of:');
```

### Generation Parameters

```javascript
// Get parameters
let params = await api.v1.generationParameters.get();
api.v1.log(`Temperature: ${params.temperature}`);

// Update parameters (requires storyEdit permission). Only the provided fields change.
await api.v1.generationParameters.update({
  temperature: 0.7,
  max_tokens: 150,
  top_p: 0.9,
  top_k: 50
});
```

Note: a story's settings can have individual samplers disabled. A disabled sampler's value is ignored during generation, and updating its value does **not** enable it.

---

## 12. Lorebook API

Manage Lorebook entries and categories programmatically. Create/update/remove calls require the `lorebookEdit` permission. Creating an entry or category whose ID already exists throws an error. `createEntry` and `createCategory` both resolve to the new ID string.

**Entry fields** (`LorebookEntry`): `id`, `displayName?`, `category?`, `text?`, `keys?: string[]`, `hidden?`, `enabled?`, `forceActivation?`, `advancedConditions?: LorebookCondition[]` (types `and`, `or`, `not`, `true`, `key`, `lore`, `model`, `storymode`, `random`, `equation`, `string`; see the type definitions). For `random`, `chance` is a percentage from 0 to 100, not 0 to 1.
**Category fields** (`LorebookCategory`): `id`, `name?`, `enabled?`, `settings?: { entryHeader?: string }`.

### Reading Lorebook Content

```javascript
// Get all entries
let allEntries = await api.v1.lorebook.entries();

// Get entries in a category
let categoryEntries = await api.v1.lorebook.entries(categoryId);

// Get specific entry
let entry = await api.v1.lorebook.entry('entry-id');

// Get all categories
let allCategories = await api.v1.lorebook.categories();

// Get specific category
let category = await api.v1.lorebook.category('category-id');
```

### Creating Lorebook Content

```javascript
// Create entry (requires lorebookEdit permission)
let entryId = await api.v1.lorebook.createEntry({
  id: api.v1.uuid(),  // Optional, generated if not provided
  text: 'Galena, the Witch of the Tower...',
  displayName: 'Galena',
  keys: ['Galena', 'witch', 'tower'],
  enabled: true,
  category: categoryId  // Optional
});

// Create category (requires lorebookEdit permission)
let categoryId = await api.v1.lorebook.createCategory({
  id: api.v1.uuid(),  // Optional
  name: 'Characters',
  enabled: true
});
```

### Updating Lorebook Content

```javascript
// Update entry (requires lorebookEdit permission)
await api.v1.lorebook.updateEntry('entry-id', {
  text: 'Updated entry text',
  enabled: false
});

// Update category (requires lorebookEdit permission)
await api.v1.lorebook.updateCategory('category-id', {
  name: 'Updated Category Name'
});
```

### Deleting Lorebook Content

```javascript
// Delete entry (requires lorebookEdit permission)
await api.v1.lorebook.removeEntry('entry-id');

// Delete category (requires lorebookEdit permission)
// Note: Deleting a category doesn't delete its entries; they become uncategorized
await api.v1.lorebook.removeCategory('category-id');
```

### Working with Entry Selection

```javascript
api.v1.hooks.register('onLorebookEntrySelected', async ({ entryId, categoryId }) => {
  if (entryId) {
    let entry = await api.v1.lorebook.entry(entryId);
    api.v1.log(`Selected entry: ${entry?.displayName}`);
  } else if (categoryId) {
    let category = await api.v1.lorebook.category(categoryId);
    api.v1.log(`Selected category: ${category?.name}`);
  }
});
```

---

## 13. Text-to-Speech API

Control NovelAI's Text-to-Speech system.

### Speaking and Queuing

```javascript
// Speak immediately (interrupts current speech)
await api.v1.tts.speak('Hello! This will be spoken aloud.');

// Queue text (plays after current speech)
await api.v1.tts.queue('This will play next.');
await api.v1.tts.queue('Then this will play.');

// Both accept an optional { seed } (voice seed) as the second argument
await api.v1.tts.speak('Different voice.', { seed: 'my-narrator-seed' });
```

`speak()` interrupts current speech **and clears the queue**. Both calls resolve once the speech is queued for generation, which may be before it starts playing.

### Playback Control

```javascript
// Pause playback
await api.v1.tts.pause();

// Resume playback
await api.v1.tts.resume();

// Toggle pause/resume
await api.v1.tts.togglePause();

// Stop all playback and clear queue
await api.v1.tts.stop();
```

---

## 14. Utilities API

Helper functions for common tasks.

### Random Number Generation

```javascript
// Random boolean (optional probability of true, default 0.5)
let coinFlip = api.v1.random.bool();
let rare = api.v1.random.bool(0.1);

// Random integer (inclusive)
let diceRoll = api.v1.random.int(1, 6);
let percentage = api.v1.random.int(0, 99);

// Random float (min inclusive, max exclusive)
let temperature = api.v1.random.float(0.5, 1.5);

// Dice roll notation
let result = api.v1.random.roll('3d6');
api.v1.log(`Rolled: ${result.total}`);  // also result.rolls[] and result.breakdown (human-readable)

let attackRoll = api.v1.random.roll('2d20+5');
let damageRoll = api.v1.random.roll('2d6+1d4+3');
```

### Text Tokenization

```javascript
// Encode text to tokens
let text = 'When did we get here?';
let tokens = await api.v1.tokenizer.encode(text, 'glm-4-6');
api.v1.log(`Token count: ${tokens.length}`);

// Decode tokens to text
let tokens = [49955, 13];
let text = await api.v1.tokenizer.decode(tokens, 'glm-4-6');
```

### Timers and Delays

The global `setTimeout`/`clearTimeout` are **not** available in scripts; use these instead.

```javascript
// Set timeout: resolves to a timer ID, so await it
let timeoutId = await api.v1.timers.setTimeout(() => {
  api.v1.log('This runs after 2 seconds');
}, 2000);

// Clear timeout
await api.v1.timers.clearTimeout(timeoutId);

// Sleep (pause execution)
async function delayedAction() {
  api.v1.log('Starting...');
  await api.v1.timers.sleep(3000);  // Wait 3 seconds
  api.v1.log('3 seconds later...');
}
```

### UUID Generation

```javascript
let uniqueId = api.v1.uuid();
api.v1.log(`Generated UUID: ${uniqueId}`);
```

### File Operations

```javascript
// Prompt for file selection (requires fileInput permission)
let file = await api.v1.file.prompt({
  multiple: false,
  accept: '.txt,.json',
  readAs: 'text'  // 'text', 'dataURL', or 'arrayBuffer'
});

if (file) {
  api.v1.log(`File content: ${file}`);
}

// Multiple files
let files = await api.v1.file.prompt({ multiple: true });

// Save file (requires fileDownload permission). Only string content is supported.
let data = JSON.stringify({ name: 'My Data', value: 42 }, null, 2);
await api.v1.file.save('data.json', data);
```

`file.prompt()` resolves to the content (a `string`, or an `ArrayBuffer` for `readAs: 'arrayBuffer'`), an array of them with `multiple: true`, or `undefined` if the user cancels. It also accepts an `encoding` option for text. These are browser file dialogs: scripts have no direct file-system access and can't choose where saved files go.

### Clipboard Access

```javascript
// Copy to clipboard (requires clipboardWrite permission)
await api.v1.clipboard.writeText('This text is now on the clipboard!');
api.v1.ui.toast('Text copied to clipboard');
```

### Rollover Helper

The Rollover Helper manages a sliding window of items within a token budget, useful for maintaining conversation history or context. When the window's total exceeds `maxTokens + rolloverTokens`, the oldest items are trimmed until it fits within `maxTokens` again. Trimming in jumps like this keeps the start of the prompt stable between calls, so more input tokens count as cached (see Generation Limit).

```javascript
// Create (synchronous; no await). All three config fields are required.
const helper = api.v1.createRolloverHelper({
  maxTokens: 2000,
  rolloverTokens: 500,
  model: 'glm-4-6'   // tokenizer used for items without a `tokens` count
});

// Add items (async). Strings or objects with a `content` string; extra fields are kept.
await helper.add({ role: 'user', content: 'First message', tokens: 10 });
await helper.add({ role: 'assistant', content: 'Second message' });  // auto-tokenized
await helper.add(['a plain string', { role: 'user', content: 'batch item' }]);

// read(): returns ALL items in the current window (each with a `tokens` field)
// and advances the window start if trimming was needed. It does not consume items.
const messages = helper.read();

// peek(): same items as read() but without moving the window start
const preview = helper.peek();

// getAll(): every stored item, including ones already trimmed out of the window
const everything = helper.getAll();

// Window size (synchronous)
const count = helper.count();
const totalTokens = helper.totalTokens();

// remove(n): remove the LAST (newest) n entries, e.g. to undo the latest exchange
helper.remove(2);

// clear(): remove everything and reset
helper.clear();

// compact(): free memory held by items already trimmed out of the window
helper.compact();

// getConfig(): returns { maxTokens, rolloverTokens, model }
```

Only `add()` returns a Promise; the other methods are synchronous.

---

## 15. Messaging API

Enable communication between different scripts running in the same story. Message data must be serializable (no functions or circular references).

### Sending Messages

```javascript
// Send to specific script (optional third argument: channel name)
await api.v1.messaging.send('target-script-id', {
  type: 'greeting',
  text: 'Hello from another script!'
}, 'greetings');

// Broadcast to all other listening scripts (the sender doesn't receive it)
await api.v1.messaging.broadcast({
  type: 'notification',
  event: 'generation-complete',
  timestamp: Date.now()
});
```

### Receiving Messages

```javascript
// Register message handler: resolves to a subscription index, so await it
let unsubId = await api.v1.messaging.onMessage((message) => {
  // message: { fromScriptId, toScriptId?, channel?, data, timestamp }
  api.v1.log(`From ${message.fromScriptId}: ${JSON.stringify(message.data)}`);
  
  if (message.data.type === 'greeting') {
    api.v1.log(`Greeting: ${message.data.text}`);
  }
}, { channel: 'greetings' });  // optional filter: { channel?, fromScriptId? }

// Unsubscribe
await api.v1.messaging.unsubscribe(unsubId);
```

### Getting Script ID

```javascript
api.v1.log(`My script ID: ${api.v1.script.id}`);
```

Hard-coding other scripts' IDs isn't recommended because they may change. Use broadcasts to discover other scripts.

---

## 16. Permissions API

Manage script permissions.

### Available Permissions

- `documentEdit` - Modify document content
- `storyEdit` - Modify story settings
- `lorebookEdit` - Modify lorebook
- `editorDecorations` - Add decorations to editor
- `clipboardWrite` - Write to clipboard
- `fileInput` - Read files from user
- `fileDownload` - Save files to user's system
- `presetEdit` - New in the current type definitions; neither the docs nor the types say which methods require it yet

### Checking Permissions

```javascript
let canEdit = await api.v1.permissions.has('documentEdit');

if (canEdit) {
  api.v1.log('Can edit document');
} else {
  api.v1.log('Cannot edit document');
}
```

### Requesting Permissions

The user sees a dialog to allow or deny. `request()` resolves to `true` if granted, including when the permission was already granted. Both `has()` and `request()` accept a single permission or an array, and `request()` takes an optional explanation message as its second argument.

```javascript
let granted = await api.v1.permissions.request('storyEdit', 'Needed to update Memory with the summary.');

if (granted) {
  api.v1.log('Permission granted!');
  // Proceed with action
} else {
  api.v1.log('Permission denied');
  api.v1.ui.toast('Permission required', { type: 'error' });
}
```

### Listing Permissions

```javascript
let grantedPermissions = await api.v1.permissions.list();
api.v1.log(`Granted: ${grantedPermissions.join(', ')}`);
```

---

## 17. Decorations API

Add visual decorations to the document editor.

### Rules

Apply styles to text matching a regular expression.

```javascript
api.v1.editor.decorations.registerRules([
  {
    id: "alice-highlight",
    type: "inline",
    match: /\bAlice\b/gi,
    style: { backgroundColor: "rgba(255, 255, 0, 0.3)" }
  },
  {
    id: "important-paragraphs",
    type: "node",
    match: /^IMPORTANT:/,
    style: { borderLeft: "4px solid red", paddingLeft: "10px" }
  }
]);

// Update rules
api.v1.editor.decorations.updateRules([
  { id: "alice-highlight", style: { backgroundColor: "rgba(0, 255, 0, 0.3)" } }
]);

// Remove rules
api.v1.editor.decorations.removeRules(["alice-highlight"]);

// Get all rules
let rules = await api.v1.editor.decorations.getRules();

// Remove all of this script's rules
api.v1.editor.decorations.clearRules();
```

`match` can be a RegExp or a string pattern (with optional `flags`, e.g. `"gi"`). `scope: { sectionIds: [...] }` limits a rule to specific paragraphs. Creating rules, markers, or widgets requires the `editorDecorations` permission. (The Decorations docs page calls this `api.v1.decorations`, but the actual namespace is `api.v1.editor.decorations`.)

### Markers

Apply styles to specific positions.

```javascript
// Inline marker (highlight text range)
let marker = await api.v1.editor.decorations.createMarker({
  type: "inline",
  from: { sectionId: 123, offset: 0 },
  to: { sectionId: 123, offset: 10 },
  style: { backgroundColor: "rgba(255, 0, 0, 0.2)" }
});

// Node marker (style entire paragraph)
let nodeMarker = await api.v1.editor.decorations.createMarker({
  type: "node",
  sectionId: 456,
  style: { backgroundColor: "rgba(0, 0, 255, 0.1)" }
});

// Update marker
await marker.update({ style: { backgroundColor: "yellow" } });

// Dispose marker
await marker.dispose();

// Create multiple markers
let markers = await api.v1.editor.decorations.createMarkers([
  { type: "inline", from: {...}, to: {...}, style: {...} },
  { type: "node", sectionId: 789, style: {...} }
]);

// Get marker info
let info = await api.v1.editor.decorations.getMarker(marker.id);

// Clear all markers
api.v1.editor.decorations.clearMarkers();
```

### Widgets

Embed custom UI components in the document.

```javascript
// Inline widget (within a paragraph)
let widget = await api.v1.editor.decorations.createWidget({
  type: "inline",
  position: { sectionId: 123, offset: 5 },
  content: [
    api.v1.ui.part.button({
      text: "Button",
      callback: () => api.v1.log("Widget clicked!")
    })
  ]
});

// Node widget (between paragraphs)
let nodeWidget = await api.v1.editor.decorations.createWidget({
  type: "node",
  sectionId: 456,
  side: "after",  // "before" or "after"
  content: [
    api.v1.ui.part.box({
      content: [
        api.v1.ui.part.text({ text: "Widget content" }),
        api.v1.ui.part.button({ text: "Click", callback: () => {} })
      ]
    })
  ]
});

// Update widget
await widget.update({
  content: [api.v1.ui.part.text({ text: "Updated!" })]
});

// Dispose widget
await widget.dispose();

// Create multiple widgets
let widgets = await api.v1.editor.decorations.createWidgets([
  { type: "inline", position: {...}, content: [...] },
  { type: "node", sectionId: 789, side: "after", content: [...] }
]);

// Clear all widgets
api.v1.editor.decorations.clearWidgets();

// Clear everything
api.v1.editor.decorations.clearAll();
```

### Widget and Marker Events

```javascript
let marker = await api.v1.editor.decorations.createMarker({
  type: "inline",
  from: { sectionId: 123, offset: 0 },
  to: { sectionId: 123, offset: 10 },
  style: { backgroundColor: "yellow" },
  onChange: (event) => {
    // { type: 'change', info } when edits move it, or
    // { type: 'dispose', reason: 'collapsed' | 'sectionRemoved' } when it's auto-removed
    api.v1.log('Marker event:', event);
  }
});
```

Widgets accept the same kind of `onChange` callback, plus `side: 'before' | 'after'` and `display: 'block' | 'inline' | 'inline-block'`. `getMarkers()` and `getWidgets()` list everything this script has created.

---

## 18. Experimental API

These are declared in `NovelAI_Script_Types_Experimental.d.ts` and gated behind the **`experimentalScriptingApi` user setting**. They are not part of the public API and may change or be removed without notice. Only use them when the user has said they enabled the setting, and feature-detect so the script still works without them. (The functions are presumably absent when the setting is off; this hasn't been confirmed.)

```javascript
const hasBlock = typeof api.v1.editor.block === 'function';
const hasTransaction = typeof api.v1.document.transaction === 'function';
```

### `api.v1.editor.block(blocked, generating?, onCancel?)`

Locks the editor while a script works. The user can't edit, and other scripts can't change the document or generate. The blocking script itself is unaffected.
- `generating: true` shows the Send button's generation animation, along with a cancel button.
- `onCancel` runs when the user presses cancel. The block is **not** released automatically, so call `block(false)` yourself.
- Only one script can hold a block, and blocking while another script does throws. A script's block is released automatically when it unloads.

```javascript
await api.v1.editor.block(true, true, async () => {
  cancelled = true;                       // user pressed cancel
  await api.v1.editor.block(false);
});
try {
  // ... document edits / generation ...
} finally {
  await api.v1.editor.block(false);       // always release
}
```

### `api.v1.document.transaction(callback)`

Groups every document edit made inside the (optionally async) callback into **one undo step**. Without it, each `append`/`updateParagraph`/etc. is its own history step.

```javascript
await api.v1.document.transaction(async () => {
  await api.v1.generate(messages, params, (choices) => {
    api.v1.document.append(choices[0].text);   // streamed appends → a single undo step
  });
});
```

---

## Appendix: Complete Example Script

Here's a complete example script demonstrating various API features:

```javascript
// Script metadata
const SCRIPT_NAME = "Example Script";
const SCRIPT_VERSION = "1.0.0";

// Initialize on load
(async () => {
  api.v1.log(`${SCRIPT_NAME} v${SCRIPT_VERSION} loaded`);
  
  // Request permissions
  await api.v1.permissions.request('documentEdit');
  await api.v1.permissions.request('storyEdit');
  
  // Register hooks
  api.v1.hooks.register('onScriptsLoaded', async () => {
    api.v1.log('All scripts loaded!');
    await setupUI();
  });
  
  api.v1.hooks.register('onGenerationEnd', async () => {
    api.v1.log('Generation completed');
  });
  
  // Setup UI (update() with ids creates-or-updates; see TypeScript Guidelines pitfall 12)
  async function setupUI() {
    await api.v1.ui.update([
      {
        type: 'sidebarPanel',
        id: 'example-panel',
        name: 'Example Panel',
        content: [
          {
            type: 'text',
            markdown: true,
            text: '# Example Script\nThis is a demonstration.'
          },
          {
            type: 'textInput',
            storageKey: 'user-input',  // unprefixed → api.v1.storage
            placeholder: 'Enter text...'
          },
          {
            type: 'button',
            text: 'Generate Summary',
            callback: async () => {
              let input = await api.v1.storage.get('user-input');
              await generateSummary(input);
            }
          }
        ]
      },
      {
        type: 'contextMenuButton',
        id: 'summarize-selection',
        text: 'Summarize Selection',
        callback: async ({ selection }) => {
          // The callback only receives the selection; read its text explicitly
          const text = await api.v1.document.textFromSelection(selection);
          await generateSummary(text);
        }
      }
    ]);
  }
  
  // Generate summary function
  async function generateSummary(text) {
    if (!text) {
      api.v1.ui.toast('No text provided', { type: 'error' });
      return;
    }
    
    try {
      let response = await api.v1.generate(
        [
          { role: 'system', content: 'Provide brief summaries.' },
          { role: 'user', content: `Summarize: ${text}` }
        ],
        {
          model: 'glm-4-6',
          max_tokens: 100
        }
      );
      
      let summary = response.choices[0].text;
      await api.v1.document.append(`\n\nSummary: ${summary}`);
      api.v1.ui.toast('Summary added!', { type: 'success' });
    } catch (error) {
      api.v1.error('Generation failed:', error);
      api.v1.ui.toast('Generation failed', { type: 'error' });
    }
  }
})();
```

---

## Additional Resources

- **Type Definitions**: http://novelai.net/scripting/types/script-types.d.ts
- **Example Scripts**: https://github.com/novelai/novelai-script-examples
- **NovelAI Documentation**: https://docs.novelai.net

---

*End of Documentation*
