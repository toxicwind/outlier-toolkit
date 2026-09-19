document.getElementById("saveBtn").addEventListener("click", async () => {
    const searchVariable = document.getElementById("searchVariable").value.trim();
    const interval = document.getElementById("interval").value.trim();
try {
    if (!searchVariable) {
        throw new Error("Please enter a search variable.");
    }

    await chrome.storage.sync.set({ searchVariable });  
    document.getElementById("successSearch").innerText = "Search variable updated!";

    alert(`Saved successfully! Searching for: "${searchVariable}"`);
} catch (error) {
    console.error("Error saving search variable: ", error);
    alert(`Failed to save: "${error.message}"`);
    document.getElementById("successSearch").innerText = "Search variable not updated.";
}
try {
    if (!interval) {
        throw new Error("Please enter an interval.");
    }

    await chrome.storage.sync.set({ interval });  
    document.getElementById("successInterval").innerText = "Interval variable saved!";

    alert(`Saved successfully! Interval: "${interval}"`);
} catch (error) {
    console.error("Error saving interval: ", error);
    alert(`Failed to save: "${error.message}"`);
    document.getElementById("successInterval").innerText = "Interval not updated!";
}
});