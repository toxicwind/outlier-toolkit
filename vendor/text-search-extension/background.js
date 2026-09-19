let intervalId;

// Listener for extension installation
chrome.runtime.onInstalled.addListener(() => {
  console.log("Outlier Task Queue Monitor extension installed.");
  chrome.runtime.openOptionsPage();
});

// Listener for browser action (icon click)
chrome.action.onClicked.addListener((tab) => {
  if (intervalId) {
    // Stop the scanning if already running
    clearInterval(intervalId);
    intervalId = null;
    chrome.notifications.create({
      type: "basic",
      iconUrl: "icon.png",
      title: "Outlier Task Queue Monitor",
      message: "Scanning stopped.",
    });
    return;
  }

chrome.storage.sync.get(["interval"], (result) => {
  const interval = result.interval || 8; // Default to 8 seconds if interval is not set

  // Start refreshing and scanning
  intervalId = setInterval(() => {
    chrome.tabs.reload(tab.id); // Refresh the page
    chrome.tabs.sendMessage(tab.id, { action: "scan" }); // Trigger scanning
  }, interval * 1000); // Convert seconds to milliseconds

  // Notify the user with the dynamic interval value
  chrome.notifications.create({
    type: "basic",
    iconUrl: "icon.png",
    title: "Outlier Task Queue Monitor",
    message: `Scanning started. Refreshing every ${interval} seconds.`,
  });
});

  })
  

  

// Listener for messages from the content script
chrome.runtime.onMessage.addListener((message) => {
  if (message.action === "found") {
    // Stop the interval if the target tag is found
    if (intervalId) {
      clearInterval(intervalId);
      intervalId = null;
    }

    // Send a notification
    chrome.notifications.create({
      type: "basic",
      iconUrl: "icon.png",
      title: "Outlier Task Queue Monitor",
      message: "The tag was found!",
    });
  }
});
