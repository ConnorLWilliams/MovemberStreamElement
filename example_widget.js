async function updateValue() {
  try {
    const res = await fetch("https://*****NGROK_ADDRESS*****/values");
    const data = await res.json();
    document.getElementById("value-display").textContent = data.donations || "Loading...";
  } catch (err) {
    console.error("Error fetching value:", err);
  }
}

updateValue();
setInterval(updateValue, 30000); // every 30s
