window.onload = function() {
    // Hide loader after page loads
    const loader = document.getElementById("loader");
    const mainContent = document.getElementById("main-content");
    setTimeout(() => {
        loader.classList.add("hidden");
        mainContent.classList.remove("hidden");
    }, 1500); // Loader timeout in ms (adjust as needed)
};

// Navigate to URL on Enter
document.getElementById("url-input").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        let url = this.value.trim();
        if (!url.startsWith("http://") && !url.startsWith("https://")) {
            url = "http://" + url;
        }
        window.location.href = url;
    }
});
