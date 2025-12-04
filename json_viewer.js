// ================= JSON JS =================

let currentJSONData = null;

// DOM elements (json viewer)
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const jsonViewer = document.getElementById('jsonViewer');
const jsonStats = document.getElementById('jsonStats');

// Drop zone → open file dialog
dropZone.addEventListener('click', () => fileInput.click());

// Input → load file
fileInput.addEventListener('change', e => {
  const file = e.target.files[0];
  if (file) loadJSONFile(file);
});

// Drag & drop handlers
['dragenter','dragover','dragleave','drop'].forEach(evt =>
  dropZone.addEventListener(evt, e => { e.preventDefault(); e.stopPropagation(); })
);

['dragenter', 'dragover'].forEach(evt =>
  dropZone.addEventListener(evt, () => dropZone.classList.add("dragover"))
);

['dragleave', 'drop'].forEach(evt =>
  dropZone.addEventListener(evt, () => dropZone.classList.remove("dragover"))
);

// On drop
dropZone.addEventListener('drop', e => {
  const file = e.dataTransfer.files[0];
  if (!file || !file.name.endsWith('.json')) {
    showJSONMessage("Vain JSON-tiedostot sallittu", "error");
    return;
  }
  loadJSONFile(file);
});

// Read file
function loadJSONFile(file) {
  const reader = new FileReader();
  reader.onload = e => {
    try {
      const jsonData = JSON.parse(e.target.result);
      processJSONData(jsonData, file.name);
    } catch (err) {
      showJSONMessage("Virhe JSON tiedostossa: " + err, "error");
    }
  };
  reader.readAsText(file);
}

// Handle loaded data
function processJSONData(jsonData, source) {
  currentJSONData = jsonData;
  displayFormattedJSON(jsonData);
  updateJSONStats(jsonData, source);
  showJSONMessage("JSON ladattu: " + source, "success");
}

// Format with syntax highlighting
function displayFormattedJSON(data) {
  let str = JSON.stringify(data, null, 2);
  str = str.replace(
    /("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?)/g,
    match => {
      let cls = 'json-number';
      if (match.startsWith('"')) {
        cls = match.endsWith(':') ? 'json-key' : 'json-string';
      }
      return `<span class="${cls}">${match}</span>`;
    }
  );
  jsonViewer.innerHTML = str;
}

// Stats
function updateJSONStats(data, source) {
  const size = (new Blob([JSON.stringify(data)]).size / 1024).toFixed(2);
  const count = Array.isArray(data)
    ? data.length
    : Object.keys(data).length;

  jsonStats.innerHTML = `
    <strong>JSON-tiedoston tiedot:</strong><br>
    Lähde: ${source}<br>
    Tyyppi: ${Array.isArray(data) ? 'Array' : 'Object'}<br>
    Koko: ${size} KB<br>
    Kohteita: ${count}
  `;
}

// Copy
function copyJSON() {
  if (!currentJSONData)
    return showJSONMessage("Ei kopioitavaa", "error");

  navigator.clipboard.writeText(JSON.stringify(currentJSONData, null, 2));
  showJSONMessage("Kopioitu!", "success");
}

// Download
function downloadJSON() {
  if (!currentJSONData)
    return showJSONMessage("Ei ladattavaa", "error");

  const blob = new Blob(
    [JSON.stringify(currentJSONData, null, 2)],
    { type: "application/json" }
  );
  const url = URL.createObjectURL(blob);

  const a = document.createElement('a');
  a.href = url;
  a.download = "data.json";
  a.click();
  URL.revokeObjectURL(url);
}

// Reset viewer
function clearJSON() {
  currentJSONData = null;
  jsonViewer.innerHTML = "Lataa JSON-tiedosto nähdäksesi sisällön...";
  jsonStats.innerHTML = "Ei ladattua JSON-tiedostoa";
  fileInput.value = "";
}

// Message popup
function showJSONMessage(msg, type) {
  const div = document.createElement('div');
  div.className = type;
  div.textContent = msg;
  jsonStats.parentNode.insertBefore(div, jsonStats);
  setTimeout(() => div.remove(), 3000);
}
