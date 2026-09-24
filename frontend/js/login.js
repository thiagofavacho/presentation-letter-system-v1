/* ===================================================================
   Se o usuário já estiver logado (token salvo), pula direto pra Home
   =================================================================== */

if (isLoggedIn()) {
  window.location.href = "index.html";
}


const loginForm = document.getElementById("login-form");
const loginButton = document.getElementById("login-button");
const alertBox = document.getElementById("alert-box");


/* ===================================================================
   Exibe mensagem de erro
   =================================================================== */

function showError(message) {
  alertBox.innerHTML = `
    <div class="alert alert-error">
      ${message}
    </div>
  `;
}


/* ===================================================================
   Limpa mensagem de erro
   =================================================================== */

function clearAlert() {
  alertBox.innerHTML = "";
}


/* ===================================================================
   Formatação visual do CPF

   Exemplo:

   12345678900

   vira:

   123.456.789-00
   =================================================================== */

function formatCPF(value) {

  // Remove tudo que não for número
  const numbers = value.replace(/\D/g, "").slice(0, 11);

  if (numbers.length <= 3) {
    return numbers;
  }

  if (numbers.length <= 6) {
    return `${numbers.slice(0, 3)}.${numbers.slice(3)}`;
  }

  if (numbers.length <= 9) {
    return `${numbers.slice(0, 3)}.${numbers.slice(3, 6)}.${numbers.slice(6)}`;
  }

  return `${numbers.slice(0, 3)}.${numbers.slice(3, 6)}.${numbers.slice(6, 9)}-${numbers.slice(9)}`;
}


/* ===================================================================
   Aplica máscara no CPF enquanto o usuário digita
   =================================================================== */

const cpfInput = document.getElementById("cpf");

cpfInput.addEventListener("input", () => {

  cpfInput.value = formatCPF(cpfInput.value);

});


/* ===================================================================
   LOGIN
   =================================================================== */

loginForm.addEventListener("submit", async (event) => {

  // Impede o navegador de recarregar a página
  event.preventDefault();

  clearAlert();


  /*
   * Pega o CPF digitado.
   *
   * Exemplo:
   *
   * 123.456.789-00
   *
   * vira:
   *
   * 12345678900
   */

  const cpf = document
    .getElementById("cpf")
    .value
    .replace(/\D/g, "");


  const password = document
    .getElementById("password")
    .value;


  /* ===============================================================
     Validação simples
     =============================================================== */

  if (cpf.length !== 11) {

    showError("Digite um CPF válido.");

    return;
  }


  /* ===============================================================
     Desabilita o botão durante o login
     =============================================================== */

  loginButton.disabled = true;

  loginButton.textContent = "Entrando...";


  try {

    /*
     * O CPF será enviado como primeiro parâmetro.
     *
     * Dentro do api.js ele continuará sendo chamado de "username",
     * porque é assim que o OAuth2PasswordRequestForm espera receber.
     */

    await login(cpf, password);


    /*
     * Login realizado.
     * Vai para a Home.
     */

    window.location.href = "index.html";


  } catch (error) {

    showError(error.message);


    loginButton.disabled = false;


    /*
     * Restaura o botão original.
     */

    loginButton.innerHTML = `
      INICIAR

      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <path d="M5 12h13"/>
        <path d="m13 6 6 6-6 6"/>
      </svg>
    `;

  }

});


/* ===================================================================
   MOSTRAR / OCULTAR SENHA
   =================================================================== */

function setupPasswordToggle(button) {

  const input = document.getElementById(
    button.dataset.passwordToggle
  );

  if (!input) return;


  button.addEventListener("click", () => {

    const showing = input.type === "text";


    input.type = showing
      ? "password"
      : "text";


    button.setAttribute(
      "aria-label",
      showing
        ? "Mostrar senha"
        : "Ocultar senha"
    );


    button.innerHTML = showing

      ? `
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12z"/>
          <circle cx="12" cy="12" r="2.5"/>
        </svg>
      `

      : `
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M3 3l18 18"/>
          <path d="M10.6 10.6a2 2 0 0 0 2.8 2.8"/>
          <path d="M9.9 5.2A10.7 10.7 0 0 1 12 5c6.5 0 10 7 10 7a17.5 17.5 0 0 1-3.1 3.8"/>
          <path d="M6.1 6.1C3.5 7.9 2 12 2 12s3.5 7 10 7c1.3 0 2.5-.2 3.5-.7"/>
        </svg>
      `;

  });

}


document
  .querySelectorAll("[data-password-toggle]")
  .forEach(setupPasswordToggle);
