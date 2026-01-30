document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("ticketform");
    const resultModal = document.getElementById("result");
    const resultText = document.getElementById("resultText");
    const closeBtn = document.querySelector(".close-button");

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const data = {
            issue_type: document.getElementById("issue_type").value,
            impact: parseInt(document.getElementById("impact").value),
            customer_type: document.getElementById("customer_type").value
        };

        const response = await fetch("http://127.0.0.1:5000/tickets", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });



        const result = await response.json();

        resultText.innerText =
        `Priority: ${result.level}
Score: ${result.score}`;

        resultModal.style.display = "flex";
    });

    closeBtn.addEventListener("click", () => {
        resultModal.style.display = "none";
    });

});

let page = 1;
const limit = 10;
let total = 0;

const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const pageInfo = document.getElementById("pageInfo");
const ticketsContainer = document.getElementById("ticketsContainer");

async function loadTickets() {
    const response = await fetch(`/tickets?page=${page}&limit=${limit}`);
    const data = await response.json();


    total = data.total;

    ticketsContainer.innerHTML = "";
    data.tickets.forEach(ticket => {
        const div = document.createElement("div");
        div.innerText = `Priority: ${ticket.level} | Score: ${ticket.score}`;
        ticketsContainer.appendChild(div);
    });

    pageInfo.innerText = `Page ${page}`;

    prevBtn.disabled = page === 1;
    nextBtn.disabled = (page * limit) >= total;
}

prevBtn.addEventListener("click", () => {
    if (page > 1) {
        page--;
        loadTickets();
    }
});

nextBtn.addEventListener("click", () => {
    if ((page * limit) < total) {
        page++;
        loadTickets();
    }
});

loadTickets();
