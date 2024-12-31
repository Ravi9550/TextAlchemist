document.addEventListener("DOMContentLoaded", function () {
  const clearBtn = document.getElementById("clear-btn");
  if (clearBtn) {
    clearBtn.addEventListener("click", function () {
      const textArea = document.getElementById("text");
      if (textArea) {
        textArea.value = ""; 
      }
      const translatedResult = document.getElementById("result-section");
      if (translatedResult) {
        translatedResult.remove(); 
      }
    });
  }
});
