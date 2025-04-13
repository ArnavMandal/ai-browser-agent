let storybook = [];
let currentPage = 0;

function getQueryParams() {
  const urlParams = new URLSearchParams(window.location.search);
  return {
    mode: urlParams.get('mode') || 'simplify',
    url: urlParams.get('url'),
    level: urlParams.get('level') || 5
  };
}

async function fetchContent(mode, url, level) {
  const response = await fetch("http://localhost:8000/process-url", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, mode, level: parseInt(level) })
  });
  return response.json();
}

function updateStorybookPage() {
  const pageIndicator = document.getElementById('page-indicator');
  const prevBtn = document.getElementById('prev-page');
  const nextBtn = document.getElementById('next-page');
  const imageContainer = document.querySelector('.storybook-image');
  const textContainer = document.querySelector('.storybook-text');

  pageIndicator.textContent = `Page ${currentPage + 1} of ${storybook.length}`;
  prevBtn.disabled = currentPage === 0;
  nextBtn.disabled = currentPage === storybook.length - 1;

  const current = storybook[currentPage];
  textContainer.innerHTML = current.text;

  imageContainer.innerHTML = current.image_url
    ? `<img src="${current.image_url}" alt="Storybook illustration" />`
    : '<div class="placeholder-image">No image</div>';
}

document.getElementById('prev-page').addEventListener('click', () => {
  if (currentPage > 0) {
    currentPage--;
    updateStorybookPage();
  }
});

document.getElementById('next-page').addEventListener('click', () => {
  if (currentPage < storybook.length - 1) {
    currentPage++;
    updateStorybookPage();
  }
});

(async function init() {
  const { mode, url, level } = getQueryParams();
  document.getElementById("mode-display").textContent = `Mode: ${mode}`;

  try {
    const resultElement = document.getElementById('result');
    const storybookView = document.getElementById('storybook-view');
    const audioPlayer = document.getElementById('audio-player');
    const podcastAudio = document.getElementById('podcast-audio');
    const audioStatus = document.querySelector('.audio-status');

    if (mode === 'picture_book') {
      // 🔹 Try loading from local storage first
      chrome.storage.local.get(['storybook_sections'], async (result) => {
        if (result.storybook_sections) {
          storybook = result.storybook_sections;
          currentPage = 0;
          storybookView.classList.remove('hidden');
          resultElement.innerText = "Use navigation to view the storybook.";
          updateStorybookPage();
        } else {
          // fallback: fetch from backend if not in storage
          const data = await fetchContent(mode, url, level);
          if (data.storybook_sections) {
            storybook = data.storybook_sections;
            currentPage = 0;
            storybookView.classList.remove('hidden');
            resultElement.innerText = "Use navigation to view the storybook.";
            updateStorybookPage();
          }
        }
      });
    } else if (mode === 'podcast') {
      const data = await fetchContent(mode, url, level);
      resultElement.innerText = data.simplified || data.raw || "No content available";
      audioPlayer.classList.remove('hidden');
      if (data.audio_url) {
        podcastAudio.src = `http://localhost:8000${data.audio_url}`;
        podcastAudio.load();
        podcastAudio.onloadeddata = () => (audioStatus.textContent = "Ready to play");
        podcastAudio.onerror = () => {
          audioStatus.textContent = "Error loading podcast audio";
        };
      }
    } else {
      const data = await fetchContent(mode, url, level);
      resultElement.innerText = data.simplified || data.raw || "No content available";
    }
  } catch (error) {
    console.error("Error loading storybook:", error);
    document.getElementById('result').innerText = "Error fetching content.";
  }
})();