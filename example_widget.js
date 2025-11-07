// === CONFIG ===
const ENDPOINT_URL = "https://movemberstreamelement.onrender.com/values"; // Replace with your Render.com URL
const REFRESH_INTERVAL = 10 * 1000; // 10 seconds (adjust as needed)

// === FUNCTION TO UPDATE DISPLAY ===
async function updateValues() {
  try {
    const response = await fetch(ENDPOINT_URL);
    if (!response.ok) throw new Error("Network response was not ok");

    const data = await response.json();

    // Loop through each key-value pair
    for (const [key, value] of Object.entries(data)) {
      // Look for an element with id="<key>"
      const el = document.getElementById(key);
      if (el) {
        el.textContent = value;
      } else {
        console.warn(`No element found for key '${key}'`);
      }
    }
  } catch (err) {
    console.error("Failed to update values:", err);
    console.error("Error name:", err.name);
    console.error("Error message:", err.message);
    console.error("Error stack:", err.stack);
  }
}

// === AUTO REFRESH LOOP ===
updateValues(); // Run once at load
setInterval(updateValues, REFRESH_INTERVAL);
