const API_BASE_URL=window.location.origin;
const form = document.getElementById("ticketform");
const issue_type = document.getElementById("issue_type");
const impact = document.getElementById("impact");
const customer_type = document.getElementById("customer_type");
const ticketsContainer = document.getElementById("ticketsContainer");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const pageInfo = document.getElementById("pageInfo");
const resultModal = document.getElementById("result");
const resultText = document.getElementById("resultText");
const closeBtn = document.querySelector(".close-button");

let page = 1;
const limit = 10;
let total = 0;

//APP starts here
document.addEventListener("DOMContentLoaded", async () => {
  console.log("[APP] Page loaded");
  
  try {

    const token = localStorage.getItem("token");
    console.log("[APP] Token from localStorage:", token ? "EXISTS" : "MISSING");
    
    if (!token) {
      console.log("[APP] No token, logging in...");
      await login();
    } else {
      console.log("[APP] Using existing token");
    }
    
    await loadTickets();
    console.log("[APP] Tickets loaded successfully");
  } catch (err) {
    console.error("[APP] Startup error:", err.message);
    showError(`Startup error: ${err.message}`);
  }
});

//UI
if (closeBtn) {
  closeBtn.onclick = () => { resultModal.style.display = "none"; };
}

const clearBtn = document.getElementById("clearCacheBtn");
if (clearBtn) {
  clearBtn.onclick = () => { localStorage.clear(); window.location.reload(); };
}

// Create ticket

async function authFetch(url, options = {}, retry = true) {
  const token = localStorage.getItem("token");
  options.headers = options.headers || {};
  if (!options.headers["Content-Type"]) options.headers["Content-Type"] = "application/json";
  if (token) options.headers.Authorization = `Bearer ${token}`;

  let res = await fetch(url, options);
  if (res.status === 401 && retry) {

    try {
      await login();
      const newToken = localStorage.getItem("token");
      if (newToken) {
        options.headers.Authorization = `Bearer ${newToken}`;
        res = await fetch(url, options);
      }
    } catch (e) {
      
      return res;
    }
  }
  return res;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    issue_type: issue_type.value,
    impact: parseInt(impact.value),
    customer_type: customer_type.value
  };

  try {
    const response = await authFetch(`${API_BASE_URL}/tickets`, {
      method: "POST",
      body: JSON.stringify(data)
    });

    const result = await response.json();

    if (!response.ok) {
      showError(result.error || result.msg || result.Error || "Failed to create ticket");
      return;
    }

    resultText.innerText = `Priority: ${result.level}\nScore: ${result.score}`;
    resultModal.style.display = "flex";
    form.reset();
    loadTickets();
  } catch (err) {
    showError(err.message || String(err));
  }
});

//Pagination
prevBtn.onclick = () => {
  if (page > 1) {
    page--;
    loadTickets();
  }
};

nextBtn.onclick = () => {
  page++;
  loadTickets();
};

//API
async function login() {
  try {
    console.log("[LOGIN] Attempting demo login");
    
    const DEMO_USER ={
      username: "vineel",
      password: "password"
    };
    const res = await fetch(`${API_BASE_URL}/auth/login`,{
      method:"POST",
      headers:{"Content-Type": "application/json"},
      body: JSON.stringify(DEMO_USER)
    });
    
    console.log("[LOGIN] Response status:", res.status);
    
    const data = await res.json();
    console.log("[LOGIN] Response:", data);

    if (!res.ok) {
      throw new Error(data.msg || "Login failed");
    }

    localStorage.setItem("token", data.access_identity);
    console.log("[LOGIN] Token saved to localStorage");
  } catch (err) {
    console.error("[LOGIN] Error:", err.message);
    showError(err.message || "Login failed. Check backend.");
    throw err;
  }
}

async function loadTickets() {
  const response = await fetch(`${API_BASE_URL}/tickets?page=${page}&limit=${limit}`);

  if (!response.ok) return;

  const data = await response.json();
  total = data.total;

  ticketsContainer.innerHTML = "";
  data.tickets.forEach(ticket => {
    const div = document.createElement("div");
    div.innerText = `Priority: ${ticket.priority_level} | Score: ${ticket.priority_score}`;
    ticketsContainer.appendChild(div);
  });

  pageInfo.innerText = `Page ${page}`;
  prevBtn.disabled = page === 1;
  nextBtn.disabled = page * limit >= total;
}

function showError(msg) {
  resultText.innerText = `Error: ${msg}`;
  resultModal.style.display = "flex";
}