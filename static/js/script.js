async function compileCode(element) {
    const code = document.getElementById("editor").value;
    const url = element.dataset.url;
  
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });
  
      if (response.ok) {
        console.log("Code compiled successfully.");
      } else {
        console.error("Error compiling code.");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  }
  
  async function runCode(element) {
    const url = element.dataset.url;
  
    try {
      const response = await fetch(url, { method: "POST" });
  
      if (response.ok) {
        const data = await response.json();
        document.getElementById("output").innerText = data.output;
      } else {
        console.error("Error running code.");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  }