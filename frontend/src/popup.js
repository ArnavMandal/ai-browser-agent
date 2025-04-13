document.addEventListener('DOMContentLoaded', () => {
  const commandInput = document.getElementById('command');
  const executeButton = document.getElementById('execute');
  const responseDiv = document.getElementById('response');

  executeButton.addEventListener('click', async () => {
    const command = commandInput.value.trim();
    if (!command) return;

    try {
      // Send the command to the background script
      const response = await chrome.runtime.sendMessage({
        type: 'EXECUTE_COMMAND',
        command: command
      });

      // Display the response
      responseDiv.textContent = response.message || 'Command executed successfully';
    } catch (error) {
      responseDiv.textContent = `Error: ${error.message}`;
    }
  });

  // Allow Enter key to trigger the execute button
  commandInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      executeButton.click();
    }
  });
}); 