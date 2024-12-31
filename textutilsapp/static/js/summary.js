document.getElementById("action").addEventListener("change", function () {
  var action = this.value;

  // Hide all input sections initially
  document.getElementById("text-input").style.display = "none";
  document.getElementById("pdf-input").style.display = "none";
  document.getElementById("url-input").style.display = "none";

  // Show the selected input section
  if (action === "summarize_text") {
    document.getElementById("text-input").style.display = "block";
  } else if (action === "summarize_pdf") {
    document.getElementById("pdf-input").style.display = "block";
  } else if (action === "summarize_url") {
    document.getElementById("url-input").style.display = "block";
  }
});

// Trigger change event to initialize visibility on page load
document.getElementById("action").dispatchEvent(new Event("change"));
