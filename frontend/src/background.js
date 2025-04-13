chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'EXECUTE_COMMAND') {
    handleCommand(request.command)
      .then(response => sendResponse({ success: true, message: response }))
      .catch(error => sendResponse({ success: false, message: error.message }));
    return true;
  }

  // For all modes opening new windows with content
  if (request.action === 'openContentWindow') {
    const mode = request.type || 'simplify';
    const encodedUrl = encodeURIComponent(request.payload.url || '');
    const level = request.payload.level || 5;

    let page = 'simplify.html';
    if (mode === 'podcast') page = 'podcast.html';
    else if (mode === 'quiz') page = 'quiz.html';
    else if (mode === 'picture_book') page = 'storybook.html';

    const finalUrl = `${page}?mode=${mode}&url=${encodedUrl}&level=${level}`;
    chrome.windows.create({
      url: chrome.runtime.getURL(finalUrl),
      type: 'popup',
      width: 1000,
      height: 800
    });
  }

  if (request.action === 'openStorybookWindow') {
    const mode = request.mode || 'picture_book';
    const url = request.payload?.url || '';
    const level = request.payload?.level || 5;

    const finalUrl = `storybook.html?mode=${mode}&url=${encodeURIComponent(url)}&level=${level}`;
    chrome.windows.create({
      url: chrome.runtime.getURL(finalUrl),
      type: 'popup',
      width: 1000,
      height: 800
    });
  }
});

// Text-based command support
async function handleCommand(command) {
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
}

async function handleSimplifyCommand(args) {
  if (args.length < 2) throw new Error('Simplify command requires a URL and grade level');
  const [url, level] = args;
  const res = await fetch('http://localhost:8000/process-url', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, mode: 'simplify', level: parseInt(level) })
  });
  const data = await res.json();
  return data.simplified;
}

async function handlePictureBookCommand(args) {
  if (args.length < 1) throw new Error('Picture book command requires a URL');
  const url = args[0];
  const res = await fetch('http://localhost:8000/process-url', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, mode: 'picture_book', level: 3 })
  });
  const data = await res.json();
  return data.simplified;
}

async function handlePodcastCommand(args) {
  if (args.length < 1) throw new Error('Podcast command requires a URL');
  const url = args[0];
  const res = await fetch('http://localhost:8000/process-url', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, mode: 'podcast', level: 8 })
  });
  const data = await res.json();
  return data.simplified;
}

async function handleQuizCommand(args) {
  if (args.length < 1) throw new Error('Quiz command requires a URL');
  const url = args[0];
  const res = await fetch('http://localhost:8000/process-url', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, mode: 'quiz', level: 8 })
  });
  const data = await res.json();
  return data.simplified;
}
