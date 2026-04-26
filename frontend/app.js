const API_BASE = "http://127.0.0.1:8000";

// ── Element refs ───────────────────────────────────────────
const dropZone     = document.getElementById("dropZone");
const fileInput    = document.getElementById("fileInput");
const browseBtn    = document.getElementById("browseBtn");
const fileName     = document.getElementById("fileName");
const uploadBtn    = document.getElementById("uploadBtn");
const uploadStatus = document.getElementById("uploadStatus");

const queryInput   = document.getElementById("queryInput");
const kInput       = document.getElementById("kInput");
const queryBtn     = document.getElementById("queryBtn");
const queryStatus  = document.getElementById("queryStatus");

const answerBox    = document.getElementById("answerBox");
const answerMeta   = document.getElementById("answerMeta");

// ── State ──────────────────────────────────────────────────
let selectedFile     = null;
let uploadedSuccessfully = false;

// ── File selection ─────────────────────────────────────────
browseBtn.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", () => {
  if (fileInput.files.length > 0) handleFileSelect(fileInput.files[0]);
});

dropZone.addEventListener("click", () => fileInput.click());

dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => {
  dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("dragover");
  if (e.dataTransfer.files.length > 0) handleFileSelect(e.dataTransfer.files[0]);
});

function handleFileSelect(file) {
  const allowed = [".txt", ".pdf", ".docx"];
  const ext = "." + file.name.split(".").pop().toLowerCase();

  if (!allowed.includes(ext)) {
    setStatus(uploadStatus, `❌ Unsupported file type: ${ext}`, "error");
    return;
  }

  selectedFile = file;
  fileName.textContent = file.name;
  fileName.classList.add("has-file");
  uploadBtn.disabled = false;
  setStatus(uploadStatus, "", "");
}

// ── Upload ─────────────────────────────────────────────────
uploadBtn.addEventListener("click", async () => {
  if (!selectedFile) return;

  const formData = new FormData();
  formData.append("file", selectedFile);

  setStatus(uploadStatus, "Indexing document", "loading");
  uploadBtn.disabled = true;
  uploadBtn.querySelector(".btn-text").textContent = "Indexing...";

  try {
    const res = await fetch(`${API_BASE}/upload`, {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    if (!res.ok) throw new Error(data.detail || "Upload failed");

    uploadedSuccessfully = true;
    setStatus(uploadStatus, `✓ ${data.message} — ${data.chunks} chunks indexed`, "success");
    queryBtn.disabled = false;

  } catch (err) {
    setStatus(uploadStatus, `❌ ${err.message}`, "error");
    uploadBtn.disabled = false;
  } finally {
    uploadBtn.querySelector(".btn-text").textContent = "Index Document";
    uploadBtn.disabled = uploadedSuccessfully;
  }
});

// ── Query ──────────────────────────────────────────────────
queryBtn.addEventListener("click", async () => {
  const question = queryInput.value.trim();
  const k = parseInt(kInput.value) || 5;

  if (!question) {
    setStatus(queryStatus, "❌ Please enter a question", "error");
    return;
  }

  if (!uploadedSuccessfully) {
    setStatus(queryStatus, "❌ Upload a document first", "error");
    return;
  }

  clearAnswer();
  setStatus(queryStatus, "Thinking", "loading");
  queryBtn.disabled = true;
  queryBtn.querySelector(".btn-text").textContent = "Thinking...";

  try {
    const res = await fetch(`${API_BASE}/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, k }),
    });

    const data = await res.json();

    if (!res.ok) throw new Error(data.detail || "Query failed");

    setStatus(queryStatus, "", "");
    typeAnswer(data.answer, data.k);

  } catch (err) {
    setStatus(queryStatus, `❌ ${err.message}`, "error");
  } finally {
    queryBtn.disabled = false;
    queryBtn.querySelector(".btn-text").textContent = "Ask";
  }
});

// ── Typing effect ──────────────────────────────────────────
function typeAnswer(text, k) {
  answerBox.classList.add("has-answer");
  answerBox.innerHTML = "";

  const cursor = document.createElement("span");
  cursor.className = "cursor";
  answerBox.appendChild(cursor);

  let i = 0;
  const speed = Math.max(10, Math.min(30, 3000 / text.length));

  const interval = setInterval(() => {
    if (i < text.length) {
      cursor.insertAdjacentText("beforebegin", text[i]);
      i++;
    } else {
      clearInterval(interval);
      cursor.remove();
      answerMeta.textContent = `↳ Retrieved ${k} chunks · ${new Date().toLocaleTimeString()}`;
    }
  }, speed);
}

// ── Helpers ────────────────────────────────────────────────
function clearAnswer() {
  answerBox.classList.remove("has-answer");
  answerBox.innerHTML = '<p class="answer-placeholder">Your answer will appear here after you ask a question.</p>';
  answerMeta.textContent = "";
}

function setStatus(el, message, type) {
  el.textContent = message;
  el.className = `status-bar ${type}`;
}

// ── Enter key to submit query ──────────────────────────────
queryInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    queryBtn.click();
  }
});