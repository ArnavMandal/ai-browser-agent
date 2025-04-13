// popup.js

// Update the level value display when slider changes
document.getElementById('explain-level').addEventListener('input', (e) => {
    document.getElementById('level-value').textContent = e.target.value;
});

// When the Extract & Simplify button is clicked, run this function:
document.getElementById('extract-btn').addEventListener('click', async () => {
    const explainLevel = document.getElementById('explain-level').value;
  
    try {
      // Get the current active tab information
      let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      const url = tab.url;
  
      // Optionally, you can show a loading message while processing.
      document.getElementById("result").innerText = "Processing...";
  
      // Send a POST request to your backend API endpoint
      fetch("http://localhost:8000/process-url", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          url: url,
          mode: "simplify",
          level: parseInt(explainLevel)  // Pass the reading level as a number
        })
      })
      .then(response => response.json())
      .then(data => {
        // Display the simplified text in the result area
        document.getElementById("result").innerText = data.simplified || data.raw || "No content available";
      })
      .catch(error => {
        console.error("Error:", error);
        document.getElementById("result").innerText = "Error: Could not connect to the AI service. Please make sure the backend server is running.";
      });
    } catch (error) {
      console.error("Error fetching tab details:", error);
      document.getElementById("result").innerText = "Error retrieving tab information.";
    }
  });
  