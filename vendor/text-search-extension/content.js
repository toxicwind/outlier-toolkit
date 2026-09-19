
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (!searchVariable) {
    console.warn("Search variable not set.");
    alert("Search variable not set. Please set it in the extension options.");
  }
  chrome.storage.sync.get("searchVariable", ({searchVariable}) => {
    if (searchVariable && document.body.innerHTML.includes(`<span>${searchVariable}</span>`)) {
      chrome.runtime.sendMessage({action: "found"});
    }

  });
});
