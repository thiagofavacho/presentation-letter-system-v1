if (!isLoggedIn()) {
  window.location.href = "login.html";
}

const logoutButton = document.getElementById("logout-button");

async function loadProfile() {
  try {
    const response = await authFetch("/auth/me");
    if (!response) return;

    const user = await response.json();

    document.getElementById("user-name").textContent = user.name;
    document.getElementById("profile-name").textContent = user.name;
    document.getElementById("profile-username").textContent = user.username;

    document.getElementById("user-avatar").textContent = user.name
      .split(" ")
      .map((word) => word[0])
      .slice(0, 2)
      .join("")
      .toUpperCase();

    // Só revela a área administrativa se o usuário logado for admin.
    // O backend já protege as rotas reais -- isso aqui é só visual,
    // pra não confundir um usuário comum mostrando links que ele não
    // teria permissão de usar.
    if (user.is_admin) {
      document.getElementById("admin-section").style.display = "block";
    }
  } catch (error) {
    console.error("Erro ao carregar perfil:", error);
  }
}

logoutButton.addEventListener("click", logout);

loadProfile();