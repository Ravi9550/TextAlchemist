var quill = new Quill("#editor-container", {
  theme: "snow",
  modules: {
    toolbar: "#toolbar-container",
  },
});

// Fullscreen toggle
document.getElementById("fullscreen").addEventListener("click", function () {
  const editor = document.getElementById("editor-container");
  const preview = document.getElementById("live-preview");
  const toolbar = document.getElementById("toolbar-container");
  const fullscreenButton = document.getElementById("fullscreen");

  if (editor.style.position === "fixed") {
    // Exit fullscreen mode
    editor.style = "";
    preview.style.display = "block";
    toolbar.style.position = "relative";
    toolbar.style.top = "";
    toolbar.style.left = "";
    toolbar.style.width = "";
    fullscreenButton.innerText = "⛶"; // Set button to "Enter Fullscreen"
  } else {
    // Enter fullscreen mode
    editor.style.position = "fixed";
    editor.style.top = "80px";
    editor.style.left = "0";
    editor.style.width = "100%";
    editor.style.height = "calc(100vh - 48px)";
    editor.style.zIndex = "9999";

    preview.style.display = "none";

    // Ensure the toolbar stays visible and behaves like part of the fullscreen mode
    toolbar.style.position = "fixed";
    toolbar.style.top = "48px";
    toolbar.style.left = "0";
    toolbar.style.width = "100%";
    toolbar.style.zIndex = "10000";

    fullscreenButton.innerText = "Exit "; // Set button to "Exit Fullscreen"
  }
});

// Live Preview
quill.on("text-change", function () {
  document.getElementById("live-preview").innerHTML = quill.root.innerHTML;
});

// Export to PDF
document.getElementById("export-pdf").addEventListener("click", function () {
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();

  // Retrieve the plain text from the editor
  const text = quill.getText();

  // Set up the font size and margins for the PDF
  const margin = 10;
  const pageHeight = doc.internal.pageSize.height;
  const pageWidth = doc.internal.pageSize.width;

  // Split the content into lines that fit within the page width
  const lines = doc.splitTextToSize(text, pageWidth - 2 * margin);

  // Add the lines to the PDF
  doc.text(lines, margin, margin + 10); // 10px margin from the top

  // Save the PDF
  doc.save("document.pdf");
});

// Export to Word
document.getElementById("export-word").addEventListener("click", function () {
  const content = `
        <!DOCTYPE html>
        <html>
        <head><title>Document</title></head>
        <body>${quill.root.innerHTML}</body>
        </html>`;
  const blob = new Blob([content], { type: "application/msword" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "document.doc";
  a.click();
});

// Export to Text
document.getElementById("export-txt").addEventListener("click", function () {
  const blob = new Blob([quill.getText()], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "document.txt";
  a.click();
});

// Apply color changes
document
  .getElementById("text-color-picker")
  .addEventListener("input", function () {
    quill.format("color", this.value);
  });

document
  .getElementById("bg-color-picker")
  .addEventListener("input", function () {
    quill.format("background", this.value);
  });
