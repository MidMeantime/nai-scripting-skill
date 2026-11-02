# NovelAI Text Generation - Complete Documentation

**Generated: January 2026** (updated October 2026)  
**Focus: Text Generation (Xialong / GLM-4.6 Models)**

> **Scope:** This file describes the NovelAI **editor and website** (models, context settings, samplers, Lorebook UI, Text Adventure, ATTG). It is background reference, not scripting API. For script code see `NovelAI_Scripting_API_Complete_Documentation.md` and `NovelAI_Script_Types.d.ts`. Use this file when a script has to reason about how the editor builds context or what a story setting means.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Models](#2-models)
3. [Editor](#3-editor)
4. [Story Settings](#4-story-settings)
5. [Advanced Settings](#5-advanced-settings)
6. [Slider Settings](#6-slider-settings)
7. [Sampling Guide](#7-sampling-guide)
8. [Writer's Toolbox](#8-writers-toolbox)
9. [Lorebook](#9-lorebook)
10. [Text Adventure Mode](#10-text-adventure-mode)
11. [Special Symbols (ATTG)](#11-special-symbols-attg)
12. [Phrase Repetition Penalty](#12-phrase-repetition-penalty)
13. [Special Modules](#13-special-modules)
14. [Glossary](#14-glossary)

---

## 1. Overview

NovelAI offers a robust Text Generation service with powerful tools to assist you in creating stories. The Editor is the main interface where you'll write and generate AI-assisted text.

### Basic Workflow

1. **Write** - Write directly in the Editor
2. **Generate** - Press Send button or Ctrl+Enter (⌘+Enter on Mac) to get an AI generation
3. **Edit** - Use Undo/Redo/Retry to refine outputs
4. **Refine** - Use Writer's Toolbox, Lorebook, and settings to guide the AI

### Text Color Coding

The Editor uses different colors to show the source of text (default "NovelAI Dark" theme):
- **Cream**: Initial prompt (first text before any AI generation)
- **White**: AI generated text
- **Pink**: User edits (changes made to AI text)
- **Blue**: User inputs (text written directly in Editor)

---

## 2. Models

NovelAI offers several text generation models. As of March 31, 2026, the current flagship is **Xialong**, a finetune of GLM-4.6. GLM-4.6 (Xialong's base model) and earlier models remain available.

### Xialong (Current Flagship)

Released March 31, 2026, Xialong is NovelAI's newest and most capable writing model, available to Opus subscribers.

- **Base Model**: Finetune of ZhipuAI's GLM-4.6 on NovelAI's storytelling dataset
- **Parameters**: 355 billion (Mixture of Experts architecture) — NovelAI's largest finetune to date and their first MoE finetune
- **Context Size**: 28,672 tokens (plus an 8,192-token rollover window; usable context grows between 28,672 and 36,864 tokens)
- **Released**: March 31, 2026

#### Key Features

1. **No collapsed probability space**: Unlike models trained with reinforcement learning, retries produce genuinely different outcomes, with improved name variety across stories
2. **Repetition-resistant**: Finetuned (with a flavor of RL) specifically to avoid repeating earlier story text, lorebook entries, or memory, and to avoid loops — to the point that NovelAI's presets no longer rely on Repetition Penalty with it (see Section 12)
3. **Text Adventure behavior change**: Text Adventure mode no longer prepends `>` to user input — inputs are sent as instructions. Outside dedicated Text Adventure mode, use the `{` instruct syntax instead of `>` (see Section 10)
4. **Multilingual**: Inherits GLM-4.6's strong multilingual capability (English, Japanese, Chinese, and more)

**Note (Scripting):** Scripts can use Xialong via `api.v1.generate` with the model ID `xialong-v1`, but it is Opus-only and tuned for story prose rather than instructions. Scripts should default to `glm-4-6`. Use `xialong-v1` only for prose output, and only when the user's story is already set to it. See Section 9 of the Scripting API documentation.

### GLM-4.6

GLM-4.6 is the open-source base model that Xialong is finetuned from. It remains available as a selectable model and was rolled out to all subscription tiers on March 1, 2026.

- **Parameters**: 355 billion (Mixture of Experts architecture)
- **Context Size**: 28,672 tokens
- **Rollover Window**: 8,192 tokens
- **Usable Context**: Between 28,672 and 36,864 tokens total
- **Released**: Originally GLM-4.5 (Sept 25, 2025), updated to GLM-4.6 (Oct 1, 2025)

#### Key Features

1. **Massive Context**: About 4x the context size of previous models
2. **Untuned Instruct Model**: May occasionally behave in undesirable ways, but setup minimizes this
3. **Multilingual**: Very capable in English, Japanese, and Chinese; supports many other languages
4. **Advanced Capabilities**: Agentic capabilities and strong reasoning

#### Important Notes

- ATTG formatting is not explicitly supported but the model will likely understand the general meaning
- This is an untuned model, so it may sometimes generate unexpected content
- Use the System Prompt and Prefill features to guide behavior

---

## 3. Editor

### Core Features

**Send Button**: Generate AI text (Ctrl+Enter / ⌘+Enter on Mac)

**Undo/Redo**: Navigate through edit history
- ![undo] Undo: Go back one step
- ![redo] Redo: Go forward one step

**Retry**: Regenerate the last AI output (Alt+R / ⌥+R on Mac)

**History**: View and select from multiple generation branches

### Title

Located at the top of the Editor:
- Organizational purposes only (doesn't influence AI)
- ![die] **Title Generation** button creates creative titles based on story content
- ![dot-reset] **Title Generation History** shows last 50 generated titles (session-only)

### Hypebot

Your AI companion that comments on your stories and provides suggestions:
- Can be customized in User Settings
- Comment frequency adjustable
- Can be set to comment only when clicked

### Input Box

Alternative way to add text (disabled by default):
- Can be activated in User Settings > Interface
- Not available in Editor V2

### Inline Generation

Generate text between existing paragraphs:
- Click earlier in story, press Ctrl+Shift+Enter
- Uses bidirectional model considering text in both directions
- Can be disabled in User Settings > AI Settings

### Context Menu

Right-click menu with shortcuts:
- Add selected text to Lorebook
- Generate lore entries
- Take screenshots
- Text-to-speech
- Insert special characters (em-dash, asterism, etc.)

**Tip**: Ctrl+Right Click brings up browser's default context menu (can be reversed in settings)

### Screenshot Designer

Create stylish screenshots of your story:
- Accessible via context menu after selecting text
- Customizable appearance
- Great for sharing highlights

### Token Probabilities

View how "confident" the AI is in its token selections:
- Enable in User Settings > AI Settings
- Tokens color-coded: Low-Medium-High probability
- Shows impact of generation settings
- ![brain] Brain icon to view probabilities

**Editor Token Probabilities**: See token selection directly in Editor (Editor V2 only)

### Text Formatting (Editor V2 Only)

Format text with:
- *Italic*: Ctrl+I
- **Bold**: Ctrl+B  
- Underline: Ctrl+U
- ~~Strikethrough~~: Ctrl+D

**Note**: Formatting is visual only; AI doesn't see the difference

### Highlight Speech (Editor V2 Only)

Highlight text within or outside quotation marks:
- Enable in User Settings > Interface
- Options: Normal, Inverted, or Off
- Customizable colors with Custom CSS

### Editor V2

The revamped editor with improved features:
- Automatic and manual text formatting
- Dynamic loading for better performance in long stories
- Editor toolbox with quick access to options
- Live detection of text origin
- Undo/Redo integration with history tree
- Save stories without leaving Editor
- Context menu on mobile
- Support for Editor Token Probabilities
- Easier Instruction inputs

**Converting Stories**: Use "Download Backup and Convert" in Story Settings
**Identification**: Stories using V2 show a paperclip icon in Library

---

## 4. Story Settings

The Story tab (first tab in options sidebar) contains fundamental story configuration.

### AI Model Selector

Choose from NovelAI's collection of models:
- GLM-4.6 (recommended for most use cases)
- Other models available but GLM-4.6 is the focus

**Change Default**: Access AI Settings to set default model and preset for new stories

### AI Module

**Legacy tool** for older models to focus on specific styles/genres:
- Not as relevant for GLM-4.6
- Over 60 modules available for older models
- Custom modules can be imported
- **All Modules** button shows full library with descriptions

### Config Preset

Saved generation settings:
- Model-specific default presets included
- Custom presets can be created
- **Edit Preset** button opens Config Settings tab
- Import/Export presets for sharing

**Tip**: Try switching presets if AI goes off track or starts looping

### Memory

Store information for the AI to remember:
- Broad details about setting, characters, and previous events
- Placed at top of Story Context by default
- Update regularly with important story elements
- Entirely optional

**Tip**: Memory can be used however you want - experiment to find what works best!

### Author's Note

Recent, high-impact guidance for the AI:
- Inserted very recently in context (much more recent than Memory)
- Functions like a supercharged Memory
- Use short sentences to describe desired outcomes
- Strong effect on AI output
- Update frequently for best results

### Lorebook Quick Access

Search and edit lorebook entries without opening full Lorebook:
- Quick search by entry name
- View and edit entry text
- Convenient for quick changes

### Story Options

**View Story Stats**: Technical information and experimental options

Statistics shown:
- Data Blocks (outputs, inputs, edits)
- Steps and Dead Ends
- Character count
- Most Used Words
- **Generate Additional Stats**: Word/paragraph/sentence count, top 10 words

Experimental Options:
- **Trim Story**: Removes undo/redo branches
- **Flatten Story**: Removes all history, treats current text as starting prompt
- **Reset to Prompt**: Cuts back to initial starting prompt

### Remote Storage

Toggle between local and server storage:
- Enables story access across browsers/platforms
- All stories fully encrypted
- Accessible only by your account
- **Recommended to keep enabled**

### Export Story

Multiple export formats:

**To File**: Save as .story with all branches and history

**As Scenario**: Create .scenario file with:
- Interactive popup on import
- Tags and descriptions
- User-defined placeholders for customization

**As Plaintext**: .txt file with raw story text only

**To Clipboard**: Full story file copied to clipboard

**As Image**: Create screenshot with Screenshot Designer

### Delete Story

Permanently delete story:
- **No recovery possible**
- Confirmation popup required

---

## 5. Advanced Settings

Advanced Settings tab contains options for Context, Phrase Bias, Banned Tokens, and more.

### Context

**Context** is how your story is shown to the AI when generating outputs.

**Context Bar**: Visual breakdown of context usage
- Shows token counts and percentages
- Colored by origin
- Hover for detailed information

Context limit depends on subscription tier:
- Maximum context varies by subscription
- Can be manually limited in AI Settings

**Last Context / Current Context**: Opens Context Viewer

**Edit Context Settings**: Opens Context Settings window

**Ephemeral Context**: Create time-delayed or step-based context entries

### Context Viewer

Detailed view of how Context is built:

**Context Viewer Bar**: Visual representation like main Context Bar

**Stages**: Shows Context building process
- Starts at stage 0
- Entries inserted based on Insertion Order
- Navigate with Next/Previous Stage buttons

**Main Window**: Scrollable view of entire context
- Color-coded by origin
- Shows all Memory, Author's Note, Lorebook, and story text

**Show non-activated entries**: Display inactive (but enabled) lorebook entries

**Context Viewer Information**: Detailed breakdown showing:
- Stage: When entry was inserted
- Order: Insertion Order value
- Identifier: Entry name
- Inclusion: Whether included in context
- Reason: Why included/excluded
- Key: Activation key (if applicable)
- Reserved: Reserved token count
- Tokens: Active token count
- Trim Type: How entry will be trimmed

**Included Phrase Bias Groups**: Shows active Phrase Biases from lorebook entries

### Context Settings

Four similar sections with same settings:
1. Memory Context Settings
2. Author's Note Context Settings
3. Default Lorebook Settings (see Lorebook section)
4. Story Context Settings

**Settings Available**:

- **Prefix**: Text added before entry after trimming
- **Suffix**: Text added after entry after trimming
- **Token Budget**: Maximum tokens entry may use
  - Decimals (0-1) = percentage of max context
- **Reserved Tokens**: Tokens reserved before context building
  - Entry won't reserve more than it contains
  - Decimals (0-1) = percentage of max context
- **Insertion Order**: Priority for reservation and insertion
  - Higher numbers = inserted first
  - Same order = no guarantee which goes first
- **Insertion Position**: Location in context
  - 0 = very top
  - Positive numbers = units down from top
  - Negative numbers = units up from bottom (-1 = very bottom)
- **Trim Direction**: Where to trim from when entry doesn't fit
  - "Do Not Trim" = only include if entire entry fits
- **Maximum Trim Type**: Extent of allowed trimming
- **Insertion Type**: Units for separating context entries

### Ephemeral Context Settings

Create context entries based on Story Step:

**Format**: `{+delay~duration,insertion:text}`

**Components**:
1. **Delay** (`+3` or `-3`): 
   - Steps until activation
   - `+0` = immediate
   - Add `r` after number to repeat
   
2. **Duration** (`~10`):
   - How many steps entry stays active
   
3. **Insertion** (`,+2` or `,-1`):
   - Position in context
   - `0` = top, `-1` = bottom
   
4. **Text** (`:Example`):
   - Entry content after `:`

**Example**: `{+3~10,-2:Example}`
- Activates in 3 steps
- Stays active for 10 steps
- Inserts one newline up from bottom

### System Prompt

**GLM-4.6 specific feature**:
- Initial system message to the model
- Different defaults for Storyteller vs Text Adventure mode
- Can be customized in Advanced tab

### Prefill

**GLM-4.6 specific feature**:
- Text inserted at beginning of most recent assistant message
- Helps guide AI response direction

### Phrase Bias

Increase or decrease probability of specific words/phrases:

**Format**:
- `{curly braces}` = exact text
- `[square brackets]` = token IDs
- Case-sensitive

**Groups**:
- Multiple bias groups possible
- Each group has Bias value
- ![plus] Add button creates new group
- ![trash] Delete button removes current group

**Settings**:
- **Bias Value**: Strength of bias (varies by model; use decimals for safety)
- **Enable**: Toggle bias on/off
- **When Entry Inactive**: Apply when entry is inactive instead
- **Ensure Completion After Start**: Once first token generates, complete phrase
- **Unbias When Generated**: Remove bias after phrase is generated

**Import/Export**: Share .bias files

### Banned Tokens

Completely prevent tokens/sequences from generating:
- Format same as Phrase Bias
- Case-sensitive

**Warning**: AI may work around bans with alternate spellings

### Ban Bracket Generation

Toggle to prevent `[` and `]` generation:
- Useful for generators or RPGs

### Stop Sequences

Make generation stop when character appears:
- **Min Output Length** slider: Required output length before stop sequences trigger

### Duplicate and Start as Scenario

Create duplicate story that starts like imported scenario:
- Includes Lorebook and settings
- Activates placeholders if present
- Useful for testing shareable scenarios

---

## 6. Slider Settings

Control AI generation behavior with various sliders and samplers.

### Config Preset (in Sliders)

Dropdown shows saved and imported presets:
- Defaults for each model below custom presets
- ![pen] Rename button
- **Import/Export** buttons for sharing
- **Update active Preset** popup appears when modifying settings
  - Save current preset
  - Reset changes
  - Save as new preset

### Generation Options

Three baseline settings:

**Randomness** (Temperature):
- `= 1`: Default, typical token distribution
- `< 1`: More likely tokens become likelier, less likely become rarer
  - Creates consistency but risks repetition
  - Too low = stuck in loops
- `> 1`: More equal token probabilities
  - Increases creativity but also errors
  - Helpful to use sampler to delete low-probability tokens

**Recommendation**: Keep near 1; adjust samplers instead

**Output Length**:
- Maximum characters AI can generate per output
- Minimum: 4
- Maximum: 600 (varies by subscription tier)

**Repetition Penalty**:
- Decreases probability of tokens that appeared in context
- Higher = stronger penalty
- Too high = AI runs out of choices, lower quality
- Too low = continuous repetition
- Works on tokens, not words
  - `intercom` decreases `interchange` (share `inter` token)
  - `Hello` doesn't decrease `hello` (different tokens)
- Equivalent to `e^(Presence Penalty)`

### Sampling

Samplers remove low-probability tokens while maintaining diversity.

**Recommended Main Samplers**: Unified, Min-P, or Nucleus

**Available Samplers**:

**Min-P**:
- Multiplies top token probability by slider value
- Deletes tokens below that threshold
- Example: Top probability 0.6, Min-P 0.1 → delete below 0.06
- Recommended starting value: ~0.02

**Mirostat** (Not Recommended):
- Two sliders: Tau and Learning Rate
- Attempts to maintain stochasticity at Tau value
- Learning Rate controls how quickly it adjusts
- Don't combine with other samplers

**Nucleus (Top-P)**:
- Sorts tokens by probability, adds until sum reaches slider value
- Deletes remaining low-probability tokens
- Widely benchmarked, standard for comparison
- Recommended starting value: ~0.95

**Tail-Free**:
- Deletes low-probability tokens below complex threshold
- Based on sophisticated mathematical calculation
- Recommended starting value: ~0.95

**Top-A**:
- Deletes tokens with probability < `(max token prob)^2 * A`
- Higher values = stricter, more tokens cut
- Recommended starting value: ~0.04

**Top-K**:
- Keep only K most likely tokens, delete rest
- Example: Top-K 10 keeps top 10 tokens
- Top-K 1 = same token every retry (useful for testing)

**Typical**:
- Complex sampler using entropy calculation
- Estimates "expected probability"
- Deletes tokens too high or too low vs expected
- **Unusual**: Deletes high-probability tokens
- Creates varied but lower quality output
- Recommended starting value: ~0.95

**Unified**:
- Three parameters: Linear, Quad, Conf
- Linear equivalent to 1/Randomness
- Quad shrinks low probabilities
- Conf increases Linear when top probabilities are small
- Formula: `raw value = (input log-prob) * (Linear + entropy * Conf) - (input log-prob)^2 * Quad`
- Advanced but powerful sampler

**Change Samplers**:
- Reorder samplers (applied top to bottom)
- Toggle individual samplers on/off
- Drag or use arrow buttons to arrange
- Order matters significantly

**Tip**: Start with default preset and experiment cautiously

### Repetition Penalty Settings

**Phrase Repetition Penalty**: See dedicated section

**Use Default Whitelist**: Pre-defined whitelisted tokens

**Range**:
- How many tokens from start of context get repetition penalty
- 0 (minimum) = full range (same as maximum)
- Only works when Dynamic Range disabled

**Slope**:
- Percentage of penalties applied to tokens
- Closer tokens get greater penalty
- Most recent token = doubled penalty
- Beginning of context = zero penalty
- `= 1`: Linear rise between extremes
- `< 1`: Most tokens same penalty, fewer recent/old affected differently
- `> 1`: Recent half gets ~100% penalty, older half gets minimal penalty
- Example: Slope 10 = half context 100% penalty, half zero penalty

**Dynamic Range**:
- When enabled: Penalties only apply to Story text
- Excludes Memory, Author's Note, Lorebook
- Allows AI to mention lore/descriptions more often
- Disables manual Range slider

### Alternative Repetition Penalty

**Presence**:
- Equivalent to `ln(Repetition Penalty)`
- Flat penalty if token appears at all
- Ignores appearance frequency
- Higher values extremely strong (increase of 1 = triple strength)
- **Use Repetition Penalty instead** (more user-friendly)
- High values penalize punctuation

**Frequency**:
- Stacking penalty for each token appearance
- **Dangerous**: Can quickly degrade outputs
- Keep very close to 0 if positive at all
- Small values have large effects
- High Range exacerbates problems

---

## 7. Sampling Guide

Kevin's Sampling Laboratory provides in-depth guidance on sampling.

### Preface: Edit Your Story

**Critical**: Always edit your story for correctness and quality.

- AI copies your writing level and style
- Grammar mistakes, repetition, poor style → AI copies them
- Remove errors immediately to prevent repetition cascade
- Example: Leave one repeated sentence → AI repeats more → loop forms

**Editing applies to everything**:
- Concise vs descriptive text
- Abstract metaphors vs concrete details
- Any writing style preference

**The model follows what you give it** - guide it by editing

### Sampling Basics

**Neutral Sampler**: Randomness = 1, no other samplers
- Doesn't change model outputs
- Compare other samplers to this baseline

**Quality Hierarchy**: Randomness alone < Top-K < Top-P (Nucleus)

**Why samplers help**: Lowest-probability tokens are low-quality, but model doesn't know this

**Sampler Balance**:
1. **Too much emphasis on high-probability** = simplistic and repetitive
2. **Insufficient squashing of low-probability** = bizarre text, grammar/logic errors

### Rule 1: Don't Build Large Sampler Chains

**Complex samplers break in chains**:
- Tail Free Sampling, Typical-P, Mirostat
- When they receive altered inputs, theories become invalid
- They do unpredictable things

**Other samplers**:
- Don't break, but rarely complement strengths/weaknesses
- If one is correct, the other is usually wrong

**Recommendation**: Stick to 1 sampler, or 2 maximum if confident

**Tall stacks are worse**: More samplers = improper tuning

### Rule 2: Use Closer-to-Neutral Samplers if Uncertain

**Understanding is key**: Read algorithms, view effects with Token Probabilities viewer

**Compare** Before/After probabilities to desired sampler properties (listed below)

**Documentation** summaries are optimistic (hopes and dreams, not deficiencies)

### Goals of a Sampler

1. **Cull lowest-probability tokens**
   - Very low probability = catastrophically bad
   - Balance quality vs variety
   - Quality distribution varies (different words, different stories)
   
2. **Flatten high probabilities** (optional, user preference)
   - Above ~20%: Similar output probabilities
   - Sacrifices faithfulness for word complexity
   - Example issue: `a` vs `an` - flattening improperly raises `an`
   - Benefit: Common tokens simpler than rare ones
   
3. **Similar Before → Similar After**
   - Example: All Before <5% have After = 0
   - Then Before 6% should have After ≈ 0
   
4. **Similar distributions → Similar outputs**
   - Slight Before perturbation → slight After perturbation
   
5. **No token reordering**
   - If A > B in Before, then A > B in After
   - **Exception**: Other transformations (Phrase Rep Pen, Repetition Penalty, Phrase Bias) allowed to reorder

### Numbers to Consider

View Token Probabilities (Before/After):
- Expandable to 30 tokens (from 10) in Debug Settings

**Observe**:
- **Large probabilities (>25%)**:
  - After ratio should equal Before ratio, or be closer to 1
  - After magnitude can be larger or smaller (both fine)
  
- **Middle probabilities (5-30%)**:
  - After ≥ Before
  
- **Small probabilities**:
  - Below threshold: After < Before
  - Many samplers zero below threshold

**Critical warning**: Incoherent text with Before >0.5%:
- Unicode symbols, nonsensical completions
- Indicates severe context issue
- Find and fix the cause
- All text is lower quality, even if incoherent token not chosen
- Symptom of "out of distribution" model state

### Sampler-Specific Advice

**Unified**:
- Disable Randomness (redundant with Linear)
- Set Linear 0-1 based on desired unusualness
- Lower = more unusual/creative, requires more editing
- Starting formula: `Quad = 1/3 - Linear * 4/15`, `Conf = -Quad/2`

**Advanced Unified**:
- Formula: `raw value = (input log-prob) * (Linear + entropy * Conf) - (input log-prob)^2 * Quad`
- Output = softmax(raw value)
- Negative Linear allowed but suboptimal
- If Linear or Conf negative, Quad must be positive

**Quad**: Can't make logits 0, but can make them negligible
- For true cutoff: Very high Top-P (0.999) or very low Min-P (0.0001) after Unified

**Entropy**: Natural log of number of choices
- Conf activates when token has more choices
- Theoretical range: -2*Quad to 0
- Token B (one high-prob choice) vs Token C (many low-prob choices)
  - Conf = -2*Quad: C's choices as good as B's
  - Conf = 0: C has many choices because model can't pick well
  - Practical limit: Min-P equivalent to `Conf = -0.8*Quad`
  - Keep: `-0.8*Quad < Conf < 0`

**Setting Conf precisely**:
1. Mark entropy and log-prob where quality degrades for each token
2. Linear regression: `Conf * entropy + constant ≈ marked log-prob`
3. Problem: Bad tokens often beyond 30 shown
4. Measure entropy: `entropy = (diff After log-probs) / (diff Before log-probs)` with pure Conf 1.0

**Unified goal**: Map logical sampler behavior to understandable space

**Mirostat**: Don't use
- Questionable perplexity control goal
- Subpar Top-K + Zipf method
- History tracker doesn't break repetitions
- Perplexity estimate distorted by high-confidence sequences

**Top-A**: Don't use
- Cutoff scales too much with top logit
- Replace with Min-P * 1/2 or 1/3 for strict improvement

**Tail-Free (TFS)**: Poor mathematics
- Sensitive to logit quantization
- Small low-prob changes → large second derivative changes
- If useful: Top-P better with Linear X → Top-P → Randomness X (X > 1)

**Typical**: Changes token order (violates Goal 5)
- Deletes high- AND low-probability tokens
- Insufficient information to justify high-prob deletion
- For suppressing top logits: negative Linear better

**Top-K**: Generally obsolete (oldest sampler)
- Exception: Top-K 1 for debugging

**Top-P (Nucleus)**: Standard, widely benchmarked
- Preserves distribution diversity
- All samplers compared to this

**Min-P**: Recent, easy to understand
- Top token probability imperfect certainty metric
- But works fine

---

## 8. Writer's Toolbox

Writer's Toolbox provides tools to transform text you've already written.

**Access**:
- Context menu on selected text
- ![wand] Magic wand icon beside each paragraph

### Rewrite

Rewrite passage to match existing story style:
- Useful when style has drifted
- Maintains stylistic consistency

### Transform

Infuse passage with a concept:
- Specify concept and strength
- Examples: "peanut butter", "Christmas", etc.
- Rewrite with concept imbued

### Expand

Add more detail to passage:
- Useful for exploration and inspiration
- Write bare bones → let AI add detail

### Condense

Reduce purple prose:
- Opposite of Expand
- Useful for summarizing
- Helps grasp essence of passage

### Custom

Flexible transformation tool:
- Select passage
- Tell model how to transform it
- Open-ended instructions

---

## 9. Lorebook

The Lorebook stores supplemental information about narrative elements.

**Access**: ![book] Book icon

### Overview

Repository for:
- Characters
- Locations
- Objects
- Factions
- Other narrative elements

**Context Integration**: Entries added to context when activation keys appear

**Tools**: Generate new lore entries with built-in generator

### Import/Export

- ![import] Import button: Load .json, .lorebook, or embedded .png
- ![export] Export button: Save lorebook
- ![image_down] Image embed: Embed lorebook in .png for sharing

**Tip**: NovelAI Discord has content sharing channel with lorebooks

### Additional Controls

- ![box-check] Selection: Select multiple entries for deletion or export
- ![funnel] Sort: Alphabetical or by recent
- ![search] Search: Perform search

### Entries

Main component of Lorebook:
- Activation keys trigger entry
- Entry text inserted into context when triggered

**Entry Controls**:
- ![trash] Delete entry
- ![copy] Duplicate entry

**Entry Title**: 
- Organizational only (AI doesn't see it)
- Include title in entry text or AI won't know what entry is about

**Enabled Toggle**: ![check] or ![cross]
- Determines if entry can activate
- Disabled entries never inserted

**Entry Text**: Content placed in context when activated

**Activation Keys**:
- Words/phrases that trigger entry
- Case-insensitive
- **Regex**: Keys starting/ending with `/`
  - Case-sensitive
  - Flags: i, s, m, u
  - For placeholder keys: add `$` before first `/`
- **Multiple keys**: Use `&` (e.g., `NovelAI & Anlatan`)

**Always On**: Entry always in context regardless of keys

**Hide**: ![eye-invisible] Mark entry as hidden
- Prevents viewing contents unless revealed
- Useful for scenarios shared with others
- Hidden entries excluded from context viewer

### Generator

Let AI generate lore entries:

**Generation Type**: Influence entry type
- Choose from list or custom type

**Input Text**: Prompt for generation
- Names like "Fogwood Keep" work best
- Short descriptions: "an enthusiastic merchant"
- Add tags in parentheses: "Black Skull Fleet (pirates, space)"

**Add Context (Advanced)**:
- Include Memory, Author's Note, recent story (~2500 chars)
- Include other lorebook entries
- Information used when generating

**Generation History**: Last 50 outputs (session-only, cleared on refresh)

**Change Settings**: ![link] button for Model and preset

### Placement Tab

**Warning**: For experienced users only. Only change if you understand effects.

**Search Range**: 
- Characters searched for keys
- Maximum: 10,000

**Key-Relative Insertion**:
- Insert relative to last key found
- Positive = after key
- Negative = before key
- Should have lower Insertion Order than story (default 0)
- Needs sufficient reserved tokens
- Can slow context creation with many entries

**Cascading Activation**:
- Search for keys in non-story context entries
- Search range not used for non-story entries
- Entry that caused activation not guaranteed in context

**Other Settings**: Same as Context Settings (see Advanced Settings section)
- Prefix, Suffix
- Token Budget, Reserved Tokens
- Insertion Order, Insertion Position
- Trim Direction, Maximum Trim Type
- Insertion Type

### Phrase Bias Tab

Same functionality as Advanced Settings Phrase Bias:
- Increase/decrease word/phrase probability when entry active
- Format: `{curly braces}` or `[square brackets]`
- Groups with Bias values
- Enable, When Entry Inactive, Ensure Completion, Unbias options
- Import/Export .bias files

### Categories

Organize entries into groups.

**Default Tab**: Change default placement for new entries
- Update settings for all existing entries in category

**Subcontext Tab**:
- **Create Subcontext** toggle
- Group lorebook entries in category
- Inserted using chosen settings

**Phrase Bias Tab**: Category-level phrase bias
- Activated when any entry in category is active

**GLM-4.6 Specific**:
- Only setting available: **Lorebook Entry Header**
- Text inserted above every entry in category

### Advanced Conditions (GLM-4.6 Only)

Additional activation conditions beyond keywords:

**Available Conditions**:
- **True**: Always evaluates true
- **Keyword Match**: Activate when keyword in search range
- **Lore Entry Active**: Activate when selected entry is active
- **AI Model**: Activate when using selected model
- **Story Mode**: Activate in Normal or Adventure mode
- **Random Chance**: Activate randomly (0-100%)
- **Numeric Comparison**: Compare numeric values
  - Use `currentStep`, `paragraphCount`, `characterCount` variables
  - Example use: Countdown to story event
- **String Comparison**: Compare string values
  - Use `storyText`, `memoryText`, `authorsNoteText` variables
  - Operators: equals, includes, starts with, ends with
- **AND Group**: All conditions must be true
- **OR Group**: Any condition must be true
- **NOT**: Negates following condition

**Important**: Multiple top-level conditions use OR logic

---

## 10. Text Adventure Mode

Text Adventure mode uses `>` (caret) symbols to indicate character actions.

> **Xialong note (June 2026):** With the Xialong model, Text Adventure mode no longer prepends `>` to user input — inputs are now sent to the model as instructions. The auto-formatting and shortcuts below still apply in the UI, but if you run text adventures *outside* dedicated Text Adventure mode, use the `{` instruct syntax instead of `>`. The `>`-based behavior described in this section reflects the classic/general convention and still applies to earlier models.

### Overview

- `>` symbols guide narrative direction
- Hidden from story panel (visible only in Context)
- AI interprets actions and shapes response

### Getting Started

**Option 1: Blank Prompt**
1. Create new story
2. Click Text Adventure button
3. Start writing

**Note**: More coherent with longer, properly written prompts

**Option 2: Pre-made Prompt**
1. Click View All Scenarios
2. Find `Text Adventure` tagged prompt
3. Fill placeholders and start

**Tip**: Search "text" to find Text Adventure prompts quickly

### Text Adventure Module

Dedicated module for Text Adventure style:
- Automatically activates Text Adventure UI
- Select from module dropdown
- Built specifically for this narrative style

### Two Input Modes

Text Adventure takes commands in two auto-formatted modes:

**Do Mode**:
- Adds `> You` to front of input
- State what character intends to do
- Example input: `charge the dragon`
- Result: `> You charge the dragon`

**Say Mode**:
- Modifies based on punctuation
- Full stop/no punctuation: `> You say "..."`
- Question mark: `> You ask "...?"`
- Exclamation: `> You yell "...!"`

**Direct Editing**: Click and alter text directly in editor (including non-character actions)

### Advanced Inputs

**Special Actions (Do mode)**:
- `l` → `You look around.`
- `i` → `You check your inventory.`
- `x [something]` → `You examine [something].`
- Direction commands: `n`, `w`, `s`, `e`, `nw`, `ne`, `sw`, `se`, `u`, `d`
  - Example: `n` → `you go north`
- `z` → `You wait.`

**Wildcards**:
- End with `*` or `,`: AI continues action
  - `*` deleted, `,` stays
  - Example: `grab tail*` → `You grab the tail and spin it around.`
- `!` alone:
  - Do mode: Random action
  - Say mode: Shout something
- `?` alone:
  - Do mode: Inquire about something
  - Say mode: Ask something

**Shortcuts**:
- `"` prefix: Say something (even in Do mode)
- `>` prefix: Do something (even in Say mode)
- `!` prefix: **Special** - exact input without changes
  - Hidden `>` at start only
  - Not character action/command
  - Requires proper capitalization/punctuation
  - Example: `!The dragon suddenly has a heart attack.`

### How > Works in Context

`>` actions are **player actions**, not in-character actions:
- Stating what character intends, not what happens
- AI interprets and may not follow exactly

**Tips**:
- More detail = AI follows more closely
- Less detail = AI has more freedom

---

## 11. Special Symbols (ATTG)

Special symbols used to mark parts of stories and pull specific data.

> **Model note:** The GLM-4.6 and Xialong models do not explicitly support ATTG formatting, but will most likely still understand the general meaning of an ATTG line if you provide one.

### > Arrowing

Greater-than sign `>` as right-pointing arrow:
- **Text Adventure** player commands (most common)
- Text messages
- Email quotes
- Computer output
- Usually has space before text

### *Asterisking*

Text surrounded by asterisks:
- Sound effects: `*bang*`, `*Kaboom!*`
- Vocalizations: `*ahem*`, `*sigh*`
- Speech emphasis: `"I just *love* chocolate milk."`

### <Chevronning>

Less-than and greater-than as chevrons (angled brackets):
- Telepathic dialogue
- Non-verbal dialogue (sign language, writing)
- Example: `<Be not afraid,> the creature's inner voice resonated.`

### *** Dinkusing

Three asterisks `***`:
- Scene or chapter breaks
- Line with only `***`
- AI understands skip to next section

### ⁂ Asterisming

Asterism symbol `⁂`:
- Transitions to whole new stories
- Use in line by itself
- Different characters and plot
- Useful for mini-story collections
- Access via right-click menu in Editor

### { Curly Bracing } Instructions

**{ Curly Braces }** with spaces:
- Direct instructions to AI model
- See Special Modules section
- **Kayra and Clio only**

### [ Spaced Bracketing ]

**[ Square Brackets ]** with spaces - multiple uses:

**1. ATTG**: `[ Author: ; Title: ; Tags: ; Genre: ]`
- Optional story initializer
- Keep at top (Memory first row good place)
- Author and Title least useful, can omit
- **Erato specific**: Add `[ S: X ]` for quality (1-5 stars)
  - Example: `[ Tags: London, 1820s, dragons; Genre: steampunk, drama ][ S: 4 ]`
  - Proper nouns upper case, else lower case

**2. Setting/Switching Scenes**:
- `[ London, 1821 ]`
- `[ Woodstock, 1969, 22:30 ]`
- `[ New York, 1935, Night Club ]`
- `[ Monday, 8:00 A.M. ]`
- `[ Five Minutes Later ]`
- Can use anywhere, including Author's Note

**3. Character Viewpoints**:
- `[ John ]`, `[ Batman ]`
- Won't work if AI doesn't recognize name
- Can use in Memory to track protagonist

**4. Style Tagging** (Krake, Clio, Kayra, Erato):
- `[ Style: essay, nonfiction ]`
- `[ Style: verbose ]`
- `[ Style: poetry ]`
- `[ Style: text adventure ]`
- `[ Style: chat ]`
- `[ Style: SFW ]` - more likely to stay clean
- Can insert in AN without disrupting story

**5. Knowledge Tagging** (Clio, Kayra, Erato):
- `[ Knowledge: paradoxes ]`
- `[ Knowledge: anime in 90s ]`
- Prompts model about subject
- Combine with Style:
  - `[ Knowledge: CRPGs; Style: blog post ]`
  - `[ Knowledge: supernatural; Style: podcast, transcript ]`

**6. Separating AN/Memory/LB from Context**:
- Prevents AI from copying hidden contexts verbatim
- Rare in Clio/Kayra, may not need

**7. Chapter Titles**:
- `[ An Unexpected Quest ]`
- `[ The End of Many Things ]`
- `[ Into the Wastes ]`
- `[ Time Loop (3rd Restart) ]`
- `[ Prologue ]` and `[ Epilogue ]` most consistent
- Works best following dinkus
- **Results can be unpredictable**

**Note**: Always pad with space at beginning and end

**Tip**: Beware placebo effect - better results often without brackets except above uses

### ---- Horizontal Lining

Four hyphens `----`:
- Informational text instead of storytelling
- Example:
  ```
  ----
  Elves are very proud.
  They have pointy ears.
  ***
  ```
- Resume storytelling with dinkus `***`
- Or another `----` for next info entry

**With Categories**:
```
----
Characters:
Sigurd, a strong warrior who wields a mighty sword.
Euterpe, a skilled bard who plays a tooty horn.
Goose, a handsome scholar full of valuable advice.
----
Glossary:
Infinibag: A magic pouch that can contain infinite items.
Xenoarchaeologist: A scientist that studies ancient relics.
Peach Festival: A peach-themed festival celebrating harvest.
***
```

**Additional Information with ?**:
```
----
Snake
Type: animal, reptile
Legs?: None (squamous land tetrapods are legless)
***
```

**Tips**:
- Can set context prefixes/suffixes to include `----`
- `***` only for info → storytelling transition
- Many `----` in context → AI may use it in outputs (bias against/ban if unwanted)

### ==== or ====== Horizontal Barring

**Erato**: Four equals `====`
- Forum post separator
- Username below
- Optional thread name above
- Example:
  ```
  Thread: Let's chat about AI!
  ====
  Kurumuz
  ```
- Also for email separators

**Clio and Kayra**: Six equals `======`
- Same functionality as Erato four equals
- Forum posts and emails

### Wide Spacing

Two types of wider-than-normal space characters:
- Access via Editor right-click menu

**En Space**: () character
- Text-in-text situations
- Quotes, letters, signs

**Em Space**: () character
- Poetry
- Music lyrics

**Tip**: Letter n thinner than m, so en space thinner than em space

### ─ LitRPGing

Box Drawings Light Horizontal `─`:
- Start of lines for LitRPG text
- Character stats, attributes, possessions
- Example:
  ```
  ─ You gained a level in Dragoon! You earned Class Perk: Dragon Slayer!
  ─ Dragon Slayer: attacks deal bonus damage on reptile and aquatic targets.
  ```
- Access via right-click menu

### Noting (Experimental)

**Clio and Kayra only**:
```
Notes:
-
```
- At bottom of context
- Prompts footnote-style tangents and observations
- Inconsistent, makes up things randomly
- Instruct Module recommended for proper notes

### ## Commenting Out

Use `##` at very start of line to exclude from context:
```
Dwarves are very proud.
##just like the elves lol
They have large beards.
```
AI sees:
```
Dwarves are very proud.
They have large beards.
```

**Usage**:
- Comments in Scenarios for others
- Personal notes in story
- Must be at line start (each line needs `##`)
- Space after `##` optional

### %{Placeholding}

For exported .scenario files only:

**Format**:
```
%{
placeholder_code[default]:Name:Description
another_code[default2]:Name2:Description2
}
```

**Example**:
```
%{
1name[Larry]:Your Name:Write your name.
2animal[geese]:What do you prefer?:cats/dogs
}
Once upon a time, there was a person named ${1name} who liked ${2animal}.
```

**In Scenario**: Use `${code}` where value should appear

**Can include in**: Memory, Author's Note, Lorebook (even as keywords)

**On Import**:
- User fills placeholders or uses defaults
- Setup removed from prompt (unless Keep Placeholders chosen)
- Codes don't count toward token length

**Tips**:
- Start codes with number to control fill order
- Keep codes simple and identifiable
- Placeholders filled alphabetically

---

## 12. Phrase Repetition Penalty

New repetition penalty method targeting token sequences instead of individual tokens.

> **Xialong note (June 2026):** Xialong was finetuned specifically to avoid repetition and loops, so NovelAI's default presets for Xialong no longer rely on Repetition Penalty. The settings below remain available and still apply to earlier models.

### How It Works

Penalizes recurring sentence patterns:
- First token generates normally
- Second token gets penalty
- Third token gets stronger penalty
- And so on...

**Independent**: Not affected by other repetition penalty settings
- Ignores Rep Pen Range, Rep Pen Slope
- **Can be used alongside** other repetition penalties
- All penalties affect output simultaneously

### Settings

Six intensity levels (no slider):
1. Off
2. Very Light
3. Light
4. Medium
5. Aggressive
6. Very Aggressive

---

## 13. Special Modules

Experimental modules exclusive to Clio and Kayra (not GLM-4.6).

### Instruct Module

Tell AI what to do instead of what to continue from:
- Write direct requests
- Tell AI how to continue writing
- Uses `{ curly braces }` for instructions

**Creating Instruct Block**:
1. Type `{` in Editor
2. Write instruction inside
3. No need to close braces (text in block = instruction)

**Editor V2 Required**: Instruction Blocks only work in Editor V2

**Deleting Instruct Block**:
- Backspace from block into previous line
- Backspace into empty block

**Auto-Activation**: 
- Don't need to select module
- Instructions in latest ~1000 chars → auto-activates Instruct Module

**Other Locations**:
- Memory, Author's Note: Use `{ spaced curly braces }`
- Example: `{ Make the witch do a backflip at some point. }`
- Also auto-activates if in ~1000 char range

**Lorebook**: Curly braced instructions work in entries
- Create powerful automated setups

**Note**: Instructions excluded from context when Instruct Module not in use

### Prose Augmenter

Makes AI use more descriptive and flourished writing:
- Enriches dry stories
- Simpler than Instruct (just select module)

**Warning**: Use in moderation
- Too much → overly flowery writing
- Can reduce attention to actual plot

---

## 14. Glossary

Key terms used in NovelAI Text Generation.

### AI Model

Large Language Models (LLMs):
- Learn by reading massive data using deep learning
- Understand language and predict text continuation
- Fine-tuning improves capabilities (NovelAI focuses on storytelling)

### AI Modules

Also known as Soft Prompts:
- Legacy tool for older models
- Influence behavior toward particular style/genre
- Default modules provided
- User-made Custom Modules available

### Anlas

NovelAI's premium currency:
- Received with subscription (amount depends on tier)
- Can purchase Paid Anlas without subscription
- Currently only for Image Generation

### Banned Tokens

Prevent certain token sequences from generating:
- Set in Advanced Settings Sidebar

### Config Preset

Specific set of generation settings:
- Randomness, repetition penalty, sampling methods, order
- Each model has default presets
- Custom presets can be created

### Context

Range of tokens AI sees before generating:
- Built from current story point backward
- Stops at maximum context size
- Outside context = never happened for AI
- Maximum size depends on subscription tier and model
- Memory, Author's Note, Lorebook injected per insertion settings

### Dinkus

Three asterisks `***`:
- Indicates scene or chapter break

### Phrase Bias

Increase/decrease likelihood of words/phrases:
- Negative values = reduce chances
- Positive values = increase chances
- Set in Advanced Settings or Lorebook

### Prompt

Initial written text before AI generation:
- Foundation for AI generations
- Default cream color in "NovelAI Dark" theme

### Scenario

.scenario file containing:
- Initial prompt
- Memory, Author's Note, Lorebook information
- Author's chosen AI Model and Config Preset
- May include placeholders to fill on import

### Token

Basic unit of text AI uses:
- Not individual letters
- Words or word fragments
- Arrangement and Token ID depend on Tokenizer
- Example (Pile tokenizer for Krake):
  - "The quick brown fox jumps over the goblin."
  - Tokenizes: "The| quick| brown| fox| jumps| over| the| go|bl|in."
  - Each | = token boundary

### Token Probabilities

Also known as Logits:
- Chance each token had of being selected
- Influenced by:
  - Context
  - Generation settings
  - Biasing
  - Banning
  - Modules

---

## Additional Notes

### Chat Format (summary)

The official Chat Format guide (https://docs.novelai.net/en/text/chatformat) sets up a two-character "chat style" story for the older completion models. It puts `[ Style: chat ]` after the Memory info and a `***` separator, writes an opening exchange as `your_name: ...` / `bot_name: ...` lines, adds two Phrase Bias groups (`{\nbot_name:}` at +2 with Ensure Completion After Start and Unbias When Generated, then `{\nyour_name: }` at 0 with Ensure Completion After Start, in that order), and adds a stop sequence `\nyour_name:` so the AI never writes your lines. The guide predates GLM-4.6/Xialong and was written for the older completion models.

### Best Practices

1. **Edit your outputs**: Remove errors immediately to prevent AI from copying them
2. **Update Memory/AN**: Keep important information current
3. **Use Lorebook**: Organize character and world details
4. **Experiment with settings**: Find what works for your writing style
5. **Start with defaults**: Use recommended presets before customizing
6. **Check Context Viewer**: Understand what AI sees
7. **Moderate special features**: Don't overuse Prose Augmenter or complex symbols

### Resources

- **Official Documentation**: https://docs.novelai.net
- **Type Definitions**: http://novelai.net/scripting/types/script-types.d.ts
- **Community**: NovelAI Discord server for sharing and support
- **Tokenizer**: https://novelai.net/tokenizer

---

*End of Documentation*
