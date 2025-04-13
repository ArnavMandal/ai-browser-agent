chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'OPEN_NEW_WINDOW') {
    chrome.windows.create({
      url: chrome.runtime.getURL(request.url),
      type: 'popup',
      width: 1000,
      height: 800
    });
  }
});
