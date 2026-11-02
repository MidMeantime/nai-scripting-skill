/*---
compatibilityVersion: naiscript-1.0
id: 5638ab87-061a-4103-aa9e-57df03da91aa
name: New User Script
createdAt: 1774853052273
updatedAt: 1789373883304
version: 1.0.0
author: Unknown
memoryLimit: 8
config:
  - name: config_1
    prettyName: New Config
    type: string
    default: default value
    description: single line string config
  - name: config_2
    prettyName: New Config
    type: string
    default: |-
      default 

      value
    description: multiline string config
    multiline: true
  - name: config_3
    prettyName: New Config
    type: number
    default: 50
    description: number option with minimum value (optional) maximum value (optional) and disallowed decimals (optional)
    max: "999"
    min: "0"
    decimal: false
  - name: config_4
    prettyName: New Config
    type: boolean
    default: false
    description: boolean option
  - name: config_5
    prettyName: New Config
    type: select
    options:
      - label: Label 1
        value: Value 1
      - label: Label 2
        value: Value 2
      - label: Label 3
        value: Value 3
    description: select option. default value is the first option presented
---*/
// Read config values declared in the header above (fall back in case a value is unset)
async function readConfig(): Promise<{ label: string; limit: number; enabled: boolean; mode: string }> {
    return {
        label: ((await api.v1.config.get('config_1')) as string | undefined) ?? 'default value',
        limit: ((await api.v1.config.get('config_3')) as number | undefined) ?? 50,
        enabled: ((await api.v1.config.get('config_4')) as boolean | undefined) ?? false,
        mode: ((await api.v1.config.get('config_5')) as string | undefined) ?? 'Value 1',
    };
}

// Minimal panel so this example is self-contained
async function renderPanel(): Promise<void> {
    const cfg = await readConfig();
    await api.v1.ui.update([{
        type: 'scriptPanel',
        id: 'config-example-panel',
        name: 'Config Example',
        content: [
            { type: 'text', markdown: true, text: `**${cfg.label}** (mode: ${cfg.mode}, limit: ${cfg.limit}, enabled: ${cfg.enabled})` },
            // "temp:" prefix binds this text to api.v1.tempStorage
            { type: 'text', text: '{{temp:oldest_story_context}}' },
        ],
    }]);
}

// initialize the script
api.v1.hooks.register('onScriptsLoaded', async () => {
    // init storage key
    const existing: string | undefined = await api.v1.tempStorage.get('oldest_story_context') as string | undefined;
    if (!existing) {
        await api.v1.tempStorage.set('oldest_story_context', 'click the button to find the oldest story paragraph.');
    }

    await renderPanel();
});
