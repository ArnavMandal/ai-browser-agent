// Background script for the AI Browser Agent extension

// Listen for messages from the popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'EXECUTE_COMMAND') {
    handleCommand(request.command)
      .then(response => sendResponse({ success: true, message: response }))
      .catch(error => sendResponse({ success: false, message: error.message }));
    return true; // Required for async response
  }
});

// Handle different types of commands
async function handleCommand(command) {
  try {
    // Parse the command to determine the action
    const [action, ...args] = command.toLowerCase().split(' ');

    switch (action) {
      case 'simplify':
        return await handleSimplifyCommand(args);
      case 'picture_book':
        return await handlePictureBookCommand(args);
      case 'podcast':
        return await handlePodcastCommand(args);
      case 'quiz':
        return await handleQuizCommand(args);
      default:
        throw new Error(`Unknown command: ${action}`);
    }
  } catch (error) {
    console.error('Error handling command:', error);
    throw error;
  }
}

// Handle simplify command
async function handleSimplifyCommand(args) {
  if (args.length < 2) {
    throw new Error('Simplify command requires a URL and grade level');
  }

  const url = args[0];
  const gradeLevel = args[1];

  const response = await fetch('http://localhost:8000/process-url', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      url: url,
      mode: 'simplify',
      level: gradeLevel
    })
  });

  if (!response.ok) {
    throw new Error(`Failed to process URL: ${response.statusText}`);
  }

  const data = await response.json();
  return data.simplified;
}

// Handle picture book command
async function handlePictureBookCommand(args) {
  if (args.length < 1) {
    throw new Error('Picture book command requires a URL');
  }

  const url = args[0];

  const response = await fetch('http://localhost:8000/process-url', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      url: url,
      mode: 'picture_book',
      level: 3  // Default to 3rd grade level for picture books
    })
  });

  if (!response.ok) {
    throw new Error(`Failed to process URL: ${response.statusText}`);
  }

  const data = await response.json();
  return data.simplified;
}

// Handle podcast command
async function handlePodcastCommand(args) {
  if (args.length < 1) {
    throw new Error('Podcast command requires a URL');
  }

  const url = args[0];

  const response = await fetch('http://localhost:8000/process-url', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      url: url,
      mode: 'podcast',
      level: 8  // Default to 8th grade level for podcasts
    })
  });

  if (!response.ok) {
    throw new Error(`Failed to process URL: ${response.statusText}`);
  }

  const data = await response.json();
  return data.simplified;
}

// Handle quiz command
async function handleQuizCommand(args) {
  if (args.length < 1) {
    throw new Error('Quiz command requires a URL');
  }

  const url = args[0];

  const response = await fetch('http://localhost:8000/process-url', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      url: url,
      mode: 'quiz',
      level: 8  // Default to 8th grade level for quizzes
    })
  });

  if (!response.ok) {
    throw new Error(`Failed to process URL: ${response.statusText}`);
  }

  const data = await response.json();
  return data.simplified;
} 