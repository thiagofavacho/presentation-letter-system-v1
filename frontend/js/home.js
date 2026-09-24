if (!isLoggedIn()) {
  window.location.href = "login.html";
}

const alertBox = document.getElementById("alert-box");
const generateButton = document.getElementById("generate-button");
const downloadButton = document.getElementById("download-button");
const logoutButton = document.getElementById("logout-button");
let generatedPdfBlob = null;
let generatedFileName = "carta-apresentacao.pdf";

function setDefaultLetterDate() {
  const today = new Date();
  const localDate = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;
  document.getElementById("letter-date").value = localDate;
}

function showAlert(message, type = "error") {
  alertBox.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
}

function clearAlert() {
  alertBox.innerHTML = "";
}

async function loadCurrentUser() {
  try {
    const response = await authFetch("/auth/me");
    if (!response) return;

    const user = await response.json();
    document.getElementById("user-name").textContent = user.name;
    document.getElementById("user-avatar").textContent = user.name
      .split(" ")
      .map((word) => word[0])
      .slice(0, 2)
      .join("")
      .toUpperCase();
  } catch (error) {
    console.error("Erro ao carregar usuário:", error);
  }
}

async function generateLetter() {
  clearAlert();

  const promoterCode = document.getElementById("promoter-code").value.trim();
  const storeCode = document.getElementById("store-code").value.trim();
  const letterDate = document.getElementById("letter-date").value;

  if (!promoterCode || !storeCode || !letterDate) {
    showAlert("Preencha o código do promotor, o código da loja e a data da carta.");
    return;
  }

  generateButton.disabled = true;
  generateButton.innerHTML = "Gerando...";
  downloadButton.classList.remove("visible");
  generatedPdfBlob = null;

  try {
    const response = await authFetch("/letters/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        promoter_employee_id: promoterCode,
        store_code: storeCode,
        letter_date: `${letterDate}T00:00:00`,
      }),
    });

    if (!response) return;

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || "Não foi possível gerar a carta.");
    }

    generatedPdfBlob = await response.blob();
    generatedFileName = `carta_${promoterCode}_${storeCode}.pdf`;
    downloadButton.classList.add("visible");
    showAlert("Carta gerada com sucesso. Clique em BAIXAR ARQUIVO para salvar o PDF.", "success");
  } catch (error) {
    showAlert(error.message);
  } finally {
    generateButton.disabled = false;
    generateButton.innerHTML = `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
        <path d="M14 2v6h6M8 13h8M8 17h5"/>
      </svg>
      GERAR
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
        <path d="M5 12h13M13 6l6 6-6 6"/>
      </svg>`;
  }
}

function downloadGeneratedFile() {
  if (!generatedPdfBlob) {
    showAlert("Gere a carta antes de baixar o arquivo.");
    return;
  }

  const downloadUrl = window.URL.createObjectURL(generatedPdfBlob);
  const link = document.createElement("a");
  link.href = downloadUrl;
  link.download = generatedFileName;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(downloadUrl);
}

generateButton.addEventListener("click", generateLetter);
downloadButton.addEventListener("click", downloadGeneratedFile);

if (logoutButton) {
  logoutButton.addEventListener("click", logout);
}

setDefaultLetterDate();
loadCurrentUser();
