# VS Code Extension Testing Guide

## Testing the sayHello Command

### 1. Load the Extension in VS Code

1. Open VS Code
2. Open this repository folder in VS Code
3. Press F5 to launch the Extension Development Host
   - Or use "Run > Start Debugging" from the menu
   - This will open a new VS Code window with the extension loaded

### 2. Test the Command

In the Extension Development Host window:

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) to open the Command Palette
2. Type "Say Hello"
3. Select "Say Hello" from the list
4. An information message "Hello World!" should appear in the bottom right corner

### 3. Expected Results

✓ Extension activates without errors
✓ "Say Hello" command appears in Command Palette
✓ Executing the command displays "Hello World!" message

## Extension Structure

- `extension.cjs` - Main extension entry point with activate() and deactivate() functions
- `package.json` - Extension configuration with:
  - `activationEvents`: Defines when extension activates
  - `contributes.commands`: Registers the "Say Hello" command
  - `main`: Points to extension.cjs

## Implementation Details

The command registration (from `extension.cjs`):

```javascript
vscode.commands.registerCommand('extension.sayHello', () => {
  vscode.window.showInformationMessage('Hello World!');
});
```

This matches the required implementation from the problem statement.
