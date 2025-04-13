// frontend/src/podcast.js

(async function init() {
    const urlParams = new URLSearchParams(window.location.search);
    const mode = urlParams.get('mode') || 'podcast';
    const url = urlParams.get('url');
    const level = urlParams.get('level') || 8;
  
    document.getElementById("mode-display").textContent = `Mode: ${mode}`;
  
    try {
      const response = await fetch("http://localhost:8000/process-url", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, mode, level: parseInt(level) }),
      });
  
      const data = await response.json();
      const resultElement = document.getElementById('result');
      const audioPlayer = document.getElementById('audio-player');
      const podcastAudio = document.getElementById('podcast-audio');
      const audioStatus = document.querySelector('.audio-status');
  
      resultElement.innerText = data.simplified || data.raw || "No content available";
  
      if (data.audio_url) {
        podcastAudio.src = `http://localhost:8000${data.audio_url}`;
        podcastAudio.load();
        podcastAudio.onloadeddata = () => audioStatus.textContent = "Ready to play!";
        podcastAudio.onerror = () => audioStatus.textContent = "Error loading audio.";
      }
    } catch (error) {
      console.error("Error loading podcast:", error);
      document.getElementById('result').innerText = "Error fetching content.";
    }
  })();
  