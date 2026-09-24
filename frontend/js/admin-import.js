if (!isLoggedIn()) window.location.href = "login.html";

const resource = document.body.dataset.resource;
const label = document.body.dataset.label;
const alertBox = document.getElementById("alert-box");
const form = document.getElementById("import-form");
const input = document.getElementById("import-file");
const button = document.getElementById("import-button");
const errorsSection = document.getElementById("errors-section");
const errorsList = document.getElementById("errors-list");

function showAlert(message, type = "error") {
  alertBox.innerHTML = "";
  const notice = document.createElement("div");
  notice.className = `alert alert-${type}`;
  notice.textContent = message;
  alertBox.appendChild(notice);
}

async function verifyAdmin() {
  const response = await authFetch("/auth/me");
  if (!response) return false;
  const user = await response.json();
  if (!user.is_admin) window.location.href = "index.html";
  return user.is_admin;
}

function showErrors(errors) {
  errorsList.innerHTML = "";
  errors.forEach((error) => {
    const item = document.createElement("li");
    item.textContent = `Linha ${error.line}: ${error.message}`;
    errorsList.appendChild(item);
  });
  errorsSection.style.display = errors.length ? "block" : "none";
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const file = input.files[0];
  if (!file) return;
  if (!file.name.toLowerCase().endsWith(".xlsx")) return showAlert("Selecione um arquivo .xlsx.");
  if (file.size > 10 * 1024 * 1024) return showAlert("O arquivo deve ter no máximo 10 MB.");

  button.disabled = true;
  button.textContent = "Importando...";
  errorsSection.style.display = "none";
  alertBox.innerHTML = "";
  try {
    const body = new FormData();
    body.append("file", file);
    const response = await authFetch(`/${resource}/import`, { method: "POST", body });
    if (!response) return;
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || "Não foi possível importar a planilha.");
    if (data.errors.length) {
      showAlert("Nenhum registro foi alterado. Corrija as linhas indicadas e importe novamente.");
      showErrors(data.errors);
      return;
    }
    form.reset();
    showAlert(`${label}: ${data.created} cadastrado(s) e ${data.updated} atualizado(s).`, "success");
  } catch (error) {
    showAlert(error.message);
  } finally {
    button.disabled = false;
    button.textContent = "Importar planilha";
  }
});

verifyAdmin();
