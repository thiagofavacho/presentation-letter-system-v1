if (!isLoggedIn()) {
  window.location.href = "login.html";
}

const listContainer = document.getElementById("letters-list");
const alertBox = document.getElementById("alert-box");

function showError(message) {
  alertBox.innerHTML = `<div class="alert alert-error">${message}</div>`;
}

function formatDate(isoString) {
  const date = new Date(isoString);
  return date.toLocaleDateString("pt-BR");
}

function renderLetters(letters) {
  if (letters.length === 0) {
    listContainer.innerHTML = `
      <p style="color: var(--color-text-muted); text-align: center; padding: 20px 0;">
        Nenhuma carta gerada ainda.
      </p>
    `;
    return;
  }

  listContainer.innerHTML = letters
    .map(
      (letter) => `
      <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: start;">
          <div>
            <div style="font-weight: 700; margin-bottom: 4px;">
              ${letter.promoter_name}
            </div>

            <div style="font-size: 0.85rem; color: var(--color-text-muted);">
              Matrícula: ${letter.promoter_employee_id}
            </div>

            <div style="font-size: 0.85rem; color: var(--color-text-muted);">
              Loja: ${letter.store_name} (${letter.store_code})
            </div>

            <div style="font-size: 0.85rem; color: var(--color-text-muted); margin-top: 4px;">
              Data da carta: ${formatDate(letter.letter_date)}
            </div>
          </div>
        </div>

        <div style="font-size: 0.75rem; color: var(--color-text-muted); margin-top: 10px; border-top: 1px solid var(--color-border); padding-top: 8px;">
          Gerada por ${letter.user_name} em ${formatDate(letter.generated_at)}
        </div>
      </div>
    `
    )
    .join("");
}

async function loadLetters() {
  try {
    const response = await authFetch("/letters/history");

    if (!response) return;

    if (!response.ok) {
      throw new Error("Não foi possível carregar o histórico.");
    }

    const letters = await response.json();

    renderLetters(letters);
  } catch (error) {
    console.error("Erro ao carregar histórico:", error);

    showError(error.message);

    listContainer.innerHTML = "";
  }
}

loadLetters();
