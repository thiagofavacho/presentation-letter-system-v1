if (!isLoggedIn()) {
  window.location.href = "login.html";
}

const alertBox = document.getElementById("alert-box");
const usersList = document.getElementById("users-list");
const createForm = document.getElementById("create-form");

function showAlert(message, type = "error") {
  alertBox.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
}

function clearAlert() {
  alertBox.innerHTML = "";
}

/* ===================================================================
   Garante que só admin acesse esta tela. Diferente do "esconder o
   link" no perfil.html (que é só visual), aqui fazemos uma checagem
   real: se não for admin, expulsa da página.
   =================================================================== */
async function checkAdminAccess() {
  const response = await authFetch("/auth/me");
  if (!response) return false;

  const user = await response.json();
  if (!user.is_admin) {
    window.location.href = "index.html";
    return false;
  }
  return true;
}

createForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearAlert();

  const payload = {
    name: document.getElementById("new-name").value.trim(),
    username: document.getElementById("new-username").value.trim(),
    cpf: document.getElementById("new-cpf").value.trim(),
    password: document.getElementById("new-password").value,
    is_admin: document.getElementById("new-is-admin").checked,
  };

  try {
    const response = await authFetch("/users/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response) return;

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || "Não foi possível criar o usuário.");
    }

    createForm.reset();
    showAlert("Usuário criado com sucesso!", "success");
    loadUsers();
  } catch (error) {
    showAlert(error.message);
  }
});

let allUsers = [];

function renderUsers() {
  if (allUsers.length === 0) {
    usersList.innerHTML = `<p style="color: var(--color-text-muted); text-align: center; padding: 20px 0;">Nenhum usuário cadastrado.</p>`;
    return;
  }

  usersList.innerHTML = allUsers
    .map(
      (user) => `
      <div class="card" id="user-card-${user.id}">
        <div style="display: flex; justify-content: space-between; align-items: start;">
          <div>
            <div style="font-weight: 700;">${user.name}</div>
            <div style="font-size: 0.85rem; color: var(--color-text-muted);">@${user.username}</div>
            <div style="font-size: 0.75rem; margin-top: 4px;">
              ${user.is_admin ? '<span style="color: var(--color-primary); font-weight: 600;">Admin</span>' : "Usuário comum"}
              ${!user.active ? ' · <span style="color: var(--color-danger);">Inativo</span>' : ""}
            </div>
          </div>
        </div>

        <div style="display: flex; gap: 8px; margin-top: 12px;">
          <button class="btn btn-primary edit-btn" data-id="${user.id}" style="font-size: 0.8rem; padding: 8px;">
            Editar
          </button>
          ${
            user.active
              ? `<button class="btn deactivate-btn" data-id="${user.id}" style="font-size: 0.8rem; padding: 8px; background-color: var(--color-danger); color: white;">Desativar</button>`
              : `<button class="btn reactivate-btn" data-id="${user.id}" style="font-size: 0.8rem; padding: 8px; background-color: var(--color-success); color: white;">Reativar</button>`
          }
        </div>

        <div id="edit-form-${user.id}" style="display: none; margin-top: 14px; border-top: 1px solid var(--color-border); padding-top: 14px;">
          <div class="field">
            <label class="field-label">Nome</label>
            <input type="text" class="input edit-name" value="${user.name}" />
          </div>
          <div class="field">
            <label class="field-label">Nova senha (deixe em branco para não alterar)</label>
            <div class="password-field">
            <input type="password" class="input edit-password" placeholder="••••••••" />
            <button type="button" class="password-toggle edit-password-toggle" aria-label="Mostrar senha">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12z"/><circle cx="12" cy="12" r="2.5"/></svg>
            </button>
          </div>
          </div>
          <button class="btn btn-primary save-btn" data-id="${user.id}" style="font-size: 0.85rem;">
            Salvar alterações
          </button>
        </div>
      </div>
    `
    )
    .join("");

  attachRowListeners();
  document.querySelectorAll(".edit-password-toggle").forEach(setupPasswordToggle);
}

function attachRowListeners() {
  document.querySelectorAll(".edit-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const formDiv = document.getElementById(`edit-form-${btn.dataset.id}`);
      formDiv.style.display = formDiv.style.display === "none" ? "block" : "none";
    });
  });

  document.querySelectorAll(".save-btn").forEach((btn) => {
    btn.addEventListener("click", () => saveUser(btn.dataset.id));
  });

  document.querySelectorAll(".deactivate-btn").forEach((btn) => {
    btn.addEventListener("click", () => deactivateUser(btn.dataset.id));
  });

  document.querySelectorAll(".reactivate-btn").forEach((btn) => {
    btn.addEventListener("click", () => reactivateUser(btn.dataset.id));
  });
}

async function saveUser(userId) {
  clearAlert();

  const card = document.getElementById(`user-card-${userId}`);
  const name = card.querySelector(".edit-name").value.trim();
  const password = card.querySelector(".edit-password").value;

  const payload = { name };
  if (password) {
    payload.password = password;
  }

  try {
    const response = await authFetch(`/users/${userId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response) return;

    if (!response.ok) {
      throw new Error("Não foi possível salvar as alterações.");
    }

    showAlert("Usuário atualizado com sucesso!", "success");
    loadUsers();
  } catch (error) {
    showAlert(error.message);
  }
}

async function deactivateUser(userId) {
  if (!confirm("Tem certeza que deseja desativar este usuário?")) return;

  try {
    const response = await authFetch(`/users/${userId}`, { method: "DELETE" });
    if (!response) return;
    if (!response.ok) throw new Error("Não foi possível desativar o usuário.");
    loadUsers();
  } catch (error) {
    showAlert(error.message);
  }
}

async function reactivateUser(userId) {
  try {
    const response = await authFetch(`/users/${userId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ active: true }),
    });
    if (!response) return;
    if (!response.ok) throw new Error("Não foi possível reativar o usuário.");
    loadUsers();
  } catch (error) {
    showAlert(error.message);
  }
}

async function loadUsers() {
  try {
    const response = await authFetch("/users/");
    if (!response) return;
    allUsers = await response.json();
    renderUsers();
  } catch (error) {
    showAlert("Não foi possível carregar os usuários.");
  }
}

/* ===================================================================
   Inicialização: só carrega a lista se a checagem de admin passar.
   =================================================================== */
checkAdminAccess().then((isAdmin) => {
  if (isAdmin) loadUsers();
});

function setupPasswordToggle(button) {
  const input = button.parentElement.querySelector("input");
  if (!input) return;

  button.addEventListener("click", () => {
    const showing = input.type === "text";
    input.type = showing ? "password" : "text";
    button.setAttribute("aria-label", showing ? "Mostrar senha" : "Ocultar senha");
    button.innerHTML = showing
      ? `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12z"/><circle cx="12" cy="12" r="2.5"/></svg>`
      : `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3l18 18"/><path d="M10.6 10.6a2 2 0 0 0 2.8 2.8"/><path d="M9.9 5.2A10.7 10.7 0 0 1 12 5c6.5 0 10 7 10 7a17.5 17.5 0 0 1-3.1 3.8M6.1 6.1C3.5 7.9 2 12 2 12s3.5 7 10 7c1.3 0 2.5-.2 3.5-.7"/></svg>`;
  });
}

const newPasswordToggle = document.querySelector(
  '[data-password-toggle="new-password"]'
);

if (newPasswordToggle) {
  setupPasswordToggle(newPasswordToggle);
}
