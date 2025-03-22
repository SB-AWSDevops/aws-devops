function login() {
    let userId = document.getElementById("user_id").value;
    if (userId) {
        localStorage.setItem("user_id", userId);
        window.location.href = "dashboard.html"; // Redirect to Dashboard
    } else {
        alert("Please enter a valid User ID");
    }
}

document.addEventListener("DOMContentLoaded", function () {
    let userId = localStorage.getItem("user_id");

    if (!userId) {
        console.log("No active session. Please log in.");
    } else {
        document.getElementById("user_id_display").innerText = userId;
    }
});


function fetchTransactions() {
    let userId = localStorage.getItem("user_id");
    fetch(`http://127.0.0.1:5000/transactions/${userId}`)
        .then(response => response.json())
        .then(data => {
            let transactionsBody = document.getElementById("transactions_body");
            transactionsBody.innerHTML = "";  // Clear previous data
            
            data.forEach(tx => {
                let row = document.createElement("tr");
                row.innerHTML = `
                    <td>${tx.date}</td>
                    <td>${tx.type}</td>
                    <td>$${tx.amount.toFixed(2)}</td>
                `;
                transactionsBody.appendChild(row);
            });
        })
        .catch(error => alert("Error fetching transactions: " + error));
}

// Download Statement
function downloadStatement() {
    let userId = localStorage.getItem("user_id");
    fetch(`http://127.0.0.1:5000/statements/${userId}`)
        .then(response => response.json())
        .then(data => {
            if (data.download_url) {
                window.open(data.download_url, "_blank");
            } else {
                alert("Error fetching statement.");
            }
        })
        .catch(error => alert("Error: " + error));
}

