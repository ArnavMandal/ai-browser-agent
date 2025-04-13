// popup.js

let selectedType = 'simplify';
let currentPage = 0;
let storybook = [];

// Initialize UI animations with Framer Motion-like transitions
function initAnimations() {
    // Simulate Framer Motion with CSS + JS
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('mouseenter', () => {
            btn.style.transform = 'scale(1.02)';
        });
        btn.addEventListener('mouseleave', () => {
            btn.style.transform = 'scale(1)';
        });
    });
}

// Update the level value display when slider changes
document.getElementById('explain-level').addEventListener('input', (e) => {
    document.getElementById('level-value').textContent = e.target.value;
});

// Handle content type button clicks
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all buttons
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        // Add active class to clicked button
        btn.classList.add('active');
        // Update selected type
        selectedType = btn.dataset.type;
        // Update button text
        document.querySelector('.btn-text').textContent = `Extract & Process`;
        
        // Show/hide appropriate sections based on content type
        const audioPlayer = document.getElementById('audio-player');
        const storybookView = document.getElementById('storybook-view');
        
        audioPlayer.classList.add('hidden');
        storybookView.classList.add('hidden');
        
        if (selectedType === 'podcast') {
            audioPlayer.classList.remove('hidden');
        } else if (selectedType === 'picture_book') {
            storybookView.classList.remove('hidden');
        }
    });
});

// Handle storybook navigation
function updateStorybookPage() {
    if (storybook.length === 0) return;
    
    const pageIndicator = document.getElementById('page-indicator');
    const prevBtn = document.getElementById('prev-page');
    const nextBtn = document.getElementById('next-page');
    const imageContainer = document.querySelector('.storybook-image');
    const textContainer = document.querySelector('.storybook-text');
    
    // Update page indicator
    pageIndicator.textContent = `Page ${currentPage + 1} of ${storybook.length}`;
    
    // Update navigation buttons
    prevBtn.disabled = currentPage === 0;
    nextBtn.disabled = currentPage === storybook.length - 1;
    
    // Update content
    const currentSection = storybook[currentPage];
    textContainer.innerHTML = currentSection.text;
    
    // Update image with fade animation
    imageContainer.innerHTML = currentSection.image_url
        ? `<img src="${currentSection.image_url}" alt="Storybook illustration" style="opacity: 0;">`
        : '<div class="placeholder-image">Loading image...</div>';
        
    // Fade in the image
    setTimeout(() => {
        const img = imageContainer.querySelector('img');
        if (img) img.style.opacity = '1';
    }, 100);
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

// When the Extract & Process button is clicked
document.getElementById('extract-btn').addEventListener('click', async () => {
    const explainLevel = document.getElementById('explain-level').value;
    const resultElement = document.getElementById("result");
    const btnText = document.querySelector('.btn-text');
    const spinner = document.querySelector('.loading-spinner');
    const audioPlayer = document.getElementById('audio-player');
    const podcastAudio = document.getElementById('podcast-audio');
    const storybookView = document.getElementById('storybook-view');
  
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
        
        // Hide all special sections initially
        audioPlayer.classList.add('hidden');
        storybookView.classList.add('hidden');
        
        // Handle response based on content type
        if (selectedType === 'podcast' && data.audio_url) {
            // Display the podcast content
            resultElement.innerText = data.simplified || data.raw || "No content available";
            
            // Show audio player with podcast
            audioPlayer.classList.remove('hidden');
            podcastAudio.src = `http://localhost:8000${data.audio_url}`;
            podcastAudio.load();
        }
        else if (selectedType === 'picture_book' && data.storybook_sections) {
            // Handle storybook
            storybook = data.storybook_sections;
            currentPage = 0;
            
            // Show text in result area
            resultElement.innerText = "Storybook created successfully! Navigate through the pages below.";
            
            // Show storybook view
            storybookView.classList.remove('hidden');
            updateStorybookPage();
        }
        else {
            // Display standard content
            resultElement.innerText = data.simplified || data.raw || "No content available";
        }
    } catch (error) {
        console.error("Error:", error);
        resultElement.innerText = "Error: Could not connect to the AI service. Please make sure the backend server is running.";
    } finally {
        // Reset button state
        btnText.textContent = `Extract & Process`;
        spinner.classList.add('hidden');
    }
});

// Initialize animations
initAnimations();
  