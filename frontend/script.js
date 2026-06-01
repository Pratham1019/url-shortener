const API_BASE = "http://localhost:8000";
const LINKS_KEY = "url-shortener.links";
const THEME_KEY = "url-shortener.theme";

const shortenForm = document.querySelector("#shorten-form");
const urlInput = document.querySelector("#long-url");
const durationInput = document.querySelector("#duration");
const submitButton = document.querySelector("#submit-button");
const result = document.querySelector("#result");
const shortUrlLink = document.querySelector("#short-url");
const copyButton = document.querySelector("#copy-button");
const message = document.querySelector("#message");
const linkList = document.querySelector("#link-list");
const emptyState = document.querySelector("#empty-state");
const clearHistoryButton = document.querySelector("#clear-history");
const themeToggle = document.querySelector("#theme-toggle");
const themeLabel = document.querySelector("#theme-label");

function loadLinks() {
  try {
    return JSON.parse(localStorage.getItem(LINKS_KEY)) || [];
  } catch {
    return [];
  }
}

function saveLinks(links) {
  localStorage.setItem(LINKS_KEY, JSON.stringify(links));
}

function showMessage(text, type = "") {
  message.textContent = text;
  message.className = `message ${type}`.trim();
}

function getCodeFromInput(value) {
  const trimmed = value.trim();

  try {
    const url = new URL(trimmed);
    return url.pathname.split("/").filter(Boolean).pop() || "";
  } catch {
    return trimmed.replace(/^\/+/, "");
  }
}

function formatDate(value) {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short"
  }).format(new Date(value));
}

function renderLinks() {
  const links = loadLinks();

  linkList.innerHTML = "";
  emptyState.hidden = links.length > 0;
  clearHistoryButton.disabled = links.length === 0;

  links.forEach((link) => {
    const item = document.createElement("li");
    item.className = "link-card";

    const shortLink = document.createElement("a");
    shortLink.href = link.shortUrl;
    shortLink.target = "_blank";
    shortLink.rel = "noreferrer";
    shortLink.textContent = link.shortUrl;

    const meta = document.createElement("div");
    meta.className = "link-meta";

    const original = document.createElement("span");
    original.textContent = link.originalUrl;

    const created = document.createElement("span");
    created.textContent = formatDate(link.createdAt);

    meta.append(original, created);

    const actions = document.createElement("div");
    actions.className = "link-actions";

    const copy = document.createElement("button");
    copy.type = "button";
    copy.className = "small-button";
    copy.textContent = "Copy";
    copy.addEventListener("click", () => copyText(link.shortUrl));

    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.className = "small-button danger-button";
    deleteButton.textContent = "Delete";
    deleteButton.addEventListener("click", () => deleteStoredLink(link.shortUrl));

    actions.append(copy, deleteButton);
    item.append(shortLink, meta, actions);
    linkList.append(item);
  });
}

function addStoredLink(link) {
  const links = loadLinks().filter((item) => item.shortUrl !== link.shortUrl);
  links.unshift(link);
  saveLinks(links.slice(0, 20));
  renderLinks();
}

async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
    showMessage("Copied to clipboard.", "success");
  } catch {
    showMessage("Copy failed. Select the link and copy it manually.", "error");
  }
}

async function deleteStoredLink(shortUrl) {
  const code = getCodeFromInput(shortUrl);

  if (!code) {
    showMessage("Could not find the short code for this link.", "error");
    return;
  }

  showMessage("Deleting short link...");

  try {
    const response = await fetch(`${API_BASE}/${encodeURIComponent(code)}`, {
      method: "DELETE"
    });

    if (!response.ok) {
      throw new Error(await readError(response));
    }

    saveLinks(loadLinks().filter((link) => link.shortUrl !== shortUrl));
    renderLinks();
    showMessage("Short link deleted.", "success");
  } catch (error) {
    showMessage(error.message || "Could not delete the short link.", "error");
  }
}

async function readError(response) {
  try {
    const data = await response.json();
    return data.detail || data.message || "Request failed.";
  } catch {
    return "Request failed.";
  }
}

function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  themeLabel.textContent = theme === "dark" ? "Light" : "Dark";
  localStorage.setItem(THEME_KEY, theme);
}

shortenForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const url = urlInput.value.trim();
  const duration = Number(durationInput.value);

  if (!url) {
    showMessage("Enter a destination URL.", "error");
    return;
  }

  submitButton.disabled = true;
  showMessage("Creating short link...");

  try {
    const response = await fetch(`${API_BASE}/shorten`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url, duration })
    });

    if (!response.ok) {
      throw new Error(await readError(response));
    }

    const data = await response.json();
    shortUrlLink.href = data.short_url;
    shortUrlLink.textContent = data.short_url;
    result.hidden = false;

    addStoredLink({
      originalUrl: url,
      shortUrl: data.short_url,
      duration,
      createdAt: new Date().toISOString()
    });

    showMessage("Short link created.", "success");
  } catch (error) {
    showMessage(error.message || "Could not create the short link.", "error");
  } finally {
    submitButton.disabled = false;
  }
});

copyButton.addEventListener("click", () => {
  if (shortUrlLink.textContent) {
    copyText(shortUrlLink.textContent);
  }
});

clearHistoryButton.addEventListener("click", () => {
  saveLinks([]);
  renderLinks();
  showMessage("Local history cleared.", "success");
});

themeToggle.addEventListener("click", () => {
  const current = document.documentElement.dataset.theme || "light";
  applyTheme(current === "dark" ? "light" : "dark");
});

const preferredTheme = localStorage.getItem(THEME_KEY)
  || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");

applyTheme(preferredTheme);
renderLinks();
