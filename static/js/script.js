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
          const data = await response.text();
          console.log(data);
          if (data.includes("500 Internal Server Error")) {
            console.error("Server error.");
            document.getElementById("output").innerText = "Server error.";
          }
          else {
            console.error("Error compiling code.");
            // fix whitespace
            let formattedErrorMessage = data.replace(/\s/g, "\u00A0");
            // fix backslashes and newlines
            formattedErrorMessage = formattedErrorMessage.replace(/(?<!\\)\\n/g, "\n").replace(/(?<!\\)\\/g, "");
            // remove leading and trailing quotation marks
            formattedErrorMessage = formattedErrorMessage.slice(1, -2);
            document.getElementById("output").innerText = formattedErrorMessage;
          }
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