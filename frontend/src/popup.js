let selectedType = 'simplify';

document.getElementById('explain-level').addEventListener('input', (e) => {
  document.getElementById('level-value').textContent = e.target.value;
});

document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    selectedType = btn.dataset.type;
    document.querySelector('.btn-text').textContent = 'Extract & Process';
  });
});

document.getElementById('extract-btn').addEventListener('click', async () => {
  const explainLevel = parseInt(document.getElementById('explain-level').value);
  const btnText = document.querySelector('.btn-text');
  const spinner = document.querySelector('.loading-spinner');
  const resultElement = document.getElementById('result'); // Add this for simplify output
  resultElement.innerText = ''; // Clear previous result

  btnText.textContent = 'Processing';
  spinner.classList.remove('hidden');

  try {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const url = tab?.url;

    if (!url || !selectedType || isNaN(explainLevel)) {
      alert("Missing required input fields.");
      console.error("Invalid request:", { url, selectedType, explainLevel });
      return;
    }

    const body = {
      url,
      mode: selectedType,
      level: explainLevel
    };

    console.log("Sending to backend:", body);

    const response = await fetch('http://localhost:8000/process-url', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(`Server error: ${response.status} ${JSON.stringify(errorData)}`);
    }

    const data = await response.json();

    if (selectedType === 'simplify') {
      // ✅ Show result directly inside the popup
      resultElement.innerText = data.simplified || data.raw || "No content available";
    } else if (selectedType === 'picture_book') {
      await chrome.storage.local.set({ storybook_sections: data.storybook_sections });
      chrome.runtime.sendMessage({
        action: 'openStorybookWindow',
        mode: selectedType,
        payload: {
          url,
          level: explainLevel
        }
      });
    } else {
      chrome.runtime.sendMessage({
        action: 'openContentWindow',
        payload: {
          ...data,
          url,
          level: explainLevel
        },
        type: selectedType
      });
    }
  } catch (err) {
    alert('Error connecting to backend.');
    console.error("Request failed:", err);
  } finally {
    btnText.textContent = 'Extract & Process';
    spinner.classList.add('hidden');
  }
});
