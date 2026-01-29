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

        // ✅ SAFE: backend untouched
        resultText.innerText =
        `Priority: ${result.level}
Score: ${result.score}`;

        resultModal.style.display = "flex";
    });

    closeBtn.addEventListener("click", () => {
        resultModal.style.display = "none";
    });

});
