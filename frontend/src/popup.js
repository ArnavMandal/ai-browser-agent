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

document.getElementById('extract-btn').addEventListener('click', async () => {
  const explainLevel = document.getElementById('explain-level').value;
  const btnText = document.querySelector('.btn-text');
  const spinner = document.querySelector('.loading-spinner');

  btnText.textContent = 'Processing';
  spinner.classList.remove('hidden');

  try {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const url = tab.url;

    const response = await fetch('http://localhost:8000/process-url', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, mode: selectedType, level: parseInt(explainLevel) })
    });

    const data = await response.json();

    if (selectedType === 'picture_book') {
      await chrome.storage.local.set({ storybook_sections: data.storybook_sections });
      chrome.runtime.sendMessage({
        action: 'openStorybookWindow',
        mode: selectedType,
        payload: {
          url,
          level: parseInt(explainLevel)
        }
      });
    } else {
      chrome.runtime.sendMessage({
        action: 'openContentWindow',
        payload: {
          ...data,
          url,
          level: parseInt(explainLevel)
        },
        type: selectedType
      });
    }
  } catch (err) {
    alert('Error connecting to backend.');
    console.error(err);
  } finally {
    btnText.textContent = 'Extract & Process';
    spinner.classList.add('hidden');
  }
});
