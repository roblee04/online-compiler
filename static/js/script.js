async function compileCode(element) {
  const code = editor.getValue();
  const compiler = document.getElementById("compiler-select").value;
  const version = document.getElementById("version-select").value; // Get selected compiler version
  let url = element.dataset.url;
  let callRunCode = false;
  if(url.includes("/run")){
    url = url.replace("/run", "");
    callRunCode = true;
  }

  try {
      const response = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ "compiler": compiler + " " + version, "code": code }), // Include compiler version in the request
      });

      if (response.ok) {
          console.log("Code compiled successfully.");
          if(callRunCode)
            runCode(element);
          else
            document.getElementById("output").innerText = "Code compiled successfully.";
      } else {
          console.error("Error compiling code.");
          const data = await response.text();
          let formattedErrorMessage = data.replace(/\\n/g, '\n');
          document.getElementById("output").innerText = formattedErrorMessage;
      }
  } catch (error) {
      console.error("Error:", error);
  }
}

async function runCode(element) {
  // const code = document.getElementById("editor").value;
  const code = editor.getValue();
  const compiler = document.getElementById("compiler-select").value;
  const version = document.getElementById("version-select").value; // Get selected compiler version
  let url = element.dataset.url;
  if(url.includes("/compile"))
    url = url.replace("/compile", "");

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ "compiler": compiler + " " + version, "code": code }),
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