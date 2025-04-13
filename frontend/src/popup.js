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
  const level = document.getElementById('explain-level').value;
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const url = tab.url;

  const queryString = new URLSearchParams({
    mode: selectedType,
    url: url,
    level: level
  }).toString();

  await chrome.runtime.sendMessage({
    type: 'OPEN_NEW_WINDOW',
    url: `storybook.html?${queryString}`
  });
});
