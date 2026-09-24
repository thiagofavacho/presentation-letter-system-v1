if (!isLoggedIn()) {
  window.location.href = "login.html";
}

const alertBox = document.getElementById("alert-box");

function showError(message) {
  alertBox.innerHTML = `<div class="alert alert-error">${message}</div>`;
}

async function loadReport() {
  try {
    const response = await authFetch("/letters/report");
    if (!response) return;

    if (!response.ok) {
      throw new Error("Não foi possível carregar o relatório.");
    }

    const report = await response.json();

    document.getElementById("report-today").textContent = report.today;
    document.getElementById("report-week").textContent = report.this_week;
    document.getElementById("report-month").textContent = report.this_month;
  } catch (error) {
    showError(error.message);
  }
}

loadReport();