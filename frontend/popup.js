// popup.js

let selectedType = 'simplify';

// Update the level value display when slider changes
document.getElementById('explain-level').addEventListener('input', (e) => {
    document.getElementById('level-value').textContent = e.target.value;
});

// Handle content type button clicks
document.querySelectorAll('.content-type-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all buttons
        document.querySelectorAll('.content-type-btn').forEach(b => b.classList.remove('active'));
        // Add active class to clicked button
        btn.classList.add('active');
        // Update selected type
        selectedType = btn.dataset.type;
        // Update button text
        document.querySelector('.btn-text').textContent = `Extract & ${btn.textContent}`;
        
        // Show/hide audio player based on content type
        const audioPlayer = document.getElementById('audio-player');
        if (selectedType === 'podcast') {
            audioPlayer.classList.remove('hidden');
        } else {
            audioPlayer.classList.add('hidden');
        }
    });
});

// When the Extract & Process button is clicked
document.getElementById('extract-btn').addEventListener('click', async () => {
    const explainLevel = document.getElementById('explain-level').value;
    const resultElement = document.getElementById("result");
    const btnText = document.querySelector('.btn-text');
    const spinner = document.querySelector('.loading-spinner');
    const audioPlayer = document.getElementById('audio-player');
    const podcastAudio = document.getElementById('podcast-audio');
  
    try {
        // Get the current active tab information
        let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        const url = tab.url;
    
        // Show loading state
        resultElement.innerText = "Processing...";
        btnText.textContent = "Processing";
        spinner.classList.remove('hidden');
    
        // Send a POST request to your backend API endpoint
        const response = await fetch("http://localhost:8000/process-url", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                url: url,
                mode: selectedType,
                level: parseInt(explainLevel)
            })
        });

        const data = await response.json();
        
        // Display the processed content
        resultElement.innerText = data.simplified || data.raw || "No content available";
        
        // Handle audio for podcast mode
        if (selectedType === 'podcast' && data.audio_url) {
            audioPlayer.classList.remove('hidden');
            podcastAudio.src = `http://localhost:8000${data.audio_url}`;
            podcastAudio.load();
        } else {
            audioPlayer.classList.add('hidden');
        }
    } catch (error) {
        console.error("Error:", error);
        resultElement.innerText = "Error: Could not connect to the AI service. Please make sure the backend server is running.";
    } finally {
        // Reset button state
        btnText.textContent = `Extract & ${document.querySelector('.content-type-btn.active').textContent}`;
        spinner.classList.add('hidden');
    }
});
  