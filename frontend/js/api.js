/* ===================================================================
   Configuração central da API. Se o endereço do backend mudar
   (ex: for rodar em outro servidor no futuro), só muda aqui.
   =================================================================== */
const API_BASE_URL = "http://127.0.0.1:8000";

/* ===================================================================
   Armazenamento do token de acesso.
   Usamos localStorage: o token persiste mesmo se a aba for fechada
   e reaberta (diferente de sessionStorage, que se perde ao fechar).
   =================================================================== */
function saveToken(token) {
  localStorage.setItem("access_token", token);
}

function getToken() {
  return localStorage.getItem("access_token");
}

function clearToken() {
  localStorage.removeItem("access_token");
}

function isLoggedIn() {
  return !!getToken();
}

/* ===================================================================
   login(username, password)
   Chama POST /auth/login. Note que o backend espera esse endpoint
   no formato de formulário (OAuth2PasswordRequestForm), não JSON --
   por isso usamos URLSearchParams em vez de JSON.stringify.
   =================================================================== */
async function login(username, password) {
  const body = new URLSearchParams();
  body.append("username", username);
  body.append("password", password);

  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: body,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "Usuário ou senha incorretos");
  }

  const data = await response.json();
  saveToken(data.access_token);
  return data;
}

/* ===================================================================
   authFetch(path, options)
   Wrapper em volta do fetch normal que já inclui o token no cabeçalho
   Authorization automaticamente. Use esta função (em vez de fetch puro)
   para toda chamada que exige login -- assim você não repete essa
   lógica em cada tela.
   =================================================================== */
async function authFetch(path, options = {}) {
  const token = getToken();

  const headers = {
    ...(options.headers || {}),
    Authorization: `Bearer ${token}`,
  };

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  });

  // Token inválido ou expirado (30 min, como definimos no Módulo 2):
  // manda de volta pro login automaticamente.
  if (response.status === 401) {
    clearToken();
    window.location.href = "login.html";
    return;
  }

  return response;
}

function logout() {
  clearToken();
  window.location.href = "login.html";
}