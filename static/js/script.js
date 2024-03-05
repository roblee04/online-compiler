async function compileCode(element) {
    // const code = document.getElementById("editor").value;
    const code = editor.getSession().getValue();
    const compiler = document.getElementById("compiler-select").value;
    // add compiler + compiler version
    const url = element.dataset.url;
  
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ compiler: compiler, code: code }),
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
    // const code = document.getElementById("editor").value;
    const code = editor.getSession().getValue();
    const compiler = document.getElementById("compiler-select").value;
    const url = element.dataset.url;
  
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ compiler: compiler, code: code }),
      });
  
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

  window.onload = function () {
    editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.session.setMode("ace/mode/c_cpp");
  };