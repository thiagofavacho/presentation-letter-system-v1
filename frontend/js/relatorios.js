
if (!isLoggedIn()) {
  window.location.href = "login.html";
}

const alertBox = document.getElementById("alert-box");

const periodFilter = document.getElementById("filter-period");
const userFilter = document.getElementById("filter-user");
const userFilterContainer = document.getElementById("user-filter-container");

const historyTableBody = document.getElementById("history-table-body");
const historyCount = document.getElementById("history-count");

let currentUser = null;
let historyRecords = [];

// Exibe mensagens de erro na tela.
function showError(message) {
  alertBox.textContent = message;
  alertBox.className = "alert alert-error";
}

// Converte uma data para o formato brasileiro.
function formatDate(dateValue) {
  if (!dateValue) {
    return "--";
  }

  const date = new Date(dateValue);

  if (Number.isNaN(date.getTime())) {
    return "--";
  }

  return date.toLocaleDateString("pt-BR");
}

// Busca os dados do usuário autenticado.
async function loadCurrentUser() {
  const response = await authFetch("/auth/me");

  if (!response) return null;

  if (!response.ok) {
    throw new Error("Não foi possível identificar o usuário.");
  }

  currentUser = await response.json();

  return currentUser;
}

// Carrega os indicadores de cartas geradas.
async function loadReport() {
  const response = await authFetch("/letters/report");

  if (!response) return;

  if (!response.ok) {
    throw new Error("Não foi possível carregar o relatório.");
  }

  const report = await response.json();

  document.getElementById("report-today").textContent = report.today;
  document.getElementById("report-week").textContent = report.this_week;
  document.getElementById("report-month").textContent = report.this_month;
}

// Calcula a quantidade de cartas geradas no ano atual.
function updateAnnualReport() {
  const annualCount = historyRecords.filter(record => {
    return isWithinPeriod(record.generated_at, "year");
  }).length;

  document.getElementById("report-year").textContent = annualCount;
}

// Carrega o histórico de cartas.
async function loadHistory() {
  const response = await authFetch("/letters/history");

  if (!response) return;

  if (!response.ok) {
    throw new Error("Não foi possível carregar o histórico.");
  }

  historyRecords = await response.json();
  
  updateAnnualReport();

  // O filtro de usuários só será carregado para administradores.
  if (currentUser.is_admin) {
    userFilterContainer.style.display = "block";
    await loadUsers();
  }

  applyFilters();
}

// Carrega a lista de usuários para o filtro administrativo.
async function loadUsers() {
  const response = await authFetch("/users/");

  if (!response) return;

  if (!response.ok) {
    throw new Error("Não foi possível carregar a lista de usuários.");
  }

  const users = await response.json();

  userFilter.replaceChildren();

  const allUsersOption = document.createElement("option");
  allUsersOption.value = "all";
  allUsersOption.textContent = "Todos os usuários";

  userFilter.appendChild(allUsersOption);

  users
    .filter(user => user.active)
    .sort((a, b) => a.name.localeCompare(b.name, "pt-BR"))
    .forEach(user => {
      const option = document.createElement("option");

      option.value = user.id;
      option.textContent = user.name;

      userFilter.appendChild(option);
    });
}

// Retorna o início da semana, considerando segunda-feira.
function getStartOfWeek(date) {
  const start = new Date(date);

  start.setHours(0, 0, 0, 0);

  const day = start.getDay();
  const daysSinceMonday = (day + 6) % 7;

  start.setDate(start.getDate() - daysSinceMonday);

  return start;
}

// Verifica se uma data pertence ao período selecionado.
function isWithinPeriod(dateValue, period) {
  const date = new Date(dateValue);

  if (Number.isNaN(date.getTime())) {
    return false;
  }

  const today = new Date();
  today.setHours(0, 0, 0, 0);

  switch (period) {
    case "today": {
      const tomorrow = new Date(today);
      tomorrow.setDate(tomorrow.getDate() + 1);

      return date >= today && date < tomorrow;
    }

    case "week": {
      const startOfWeek = getStartOfWeek(today);
      const endOfWeek = new Date(startOfWeek);

      endOfWeek.setDate(endOfWeek.getDate() + 7);

      return date >= startOfWeek && date < endOfWeek;
    }

    case "month": {
      const startOfMonth = new Date(
        today.getFullYear(),
        today.getMonth(),
        1
      );

      const startOfNextMonth = new Date(
        today.getFullYear(),
        today.getMonth() + 1,
        1
      );

      return date >= startOfMonth && date < startOfNextMonth;
    }

    case "year": {
      const startOfYear = new Date(today.getFullYear(), 0, 1);
      const startOfNextYear = new Date(today.getFullYear() + 1, 0, 1);

      return date >= startOfYear && date < startOfNextYear;
    }

    default:
      return true;
  }
}

// Cria uma célula da tabela com segurança.
function createCell(value) {
  const cell = document.createElement("td");

  cell.style.padding = "10px 8px";
  cell.textContent = value ?? "--";

  return cell;
}

// Exibe os registros na tabela.
function renderHistory(records) {
  historyTableBody.replaceChildren();

  historyCount.textContent =
    `${records.length} registro(s) encontrado(s).`;

  if (records.length === 0) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");

    cell.colSpan = 5;
    cell.textContent = "Nenhuma carta encontrada para os filtros selecionados.";
    cell.style.textAlign = "center";
    cell.style.padding = "16px";

    row.appendChild(cell);
    historyTableBody.appendChild(row);

    return;
  }

  records.forEach(record => {
    const row = document.createElement("tr");

    row.appendChild(createCell(formatDate(record.generated_at)));
    row.appendChild(createCell(record.user_name));
    row.appendChild(createCell(record.promoter_name));
    row.appendChild(createCell(record.promoter_employee_id));
    row.appendChild(
      createCell(`${record.store_code} - ${record.store_name}`)
    );

    historyTableBody.appendChild(row);
  });
}

// Aplica os filtros selecionados.
function applyFilters() {
  const selectedPeriod = periodFilter.value;
  const selectedUser = userFilter.value;

  let filteredRecords = historyRecords.filter(record => {
    return isWithinPeriod(record.generated_at, selectedPeriod);
  });

  // O filtro de usuário só é aplicado para administradores.
  if (currentUser.is_admin && selectedUser !== "all") {
    filteredRecords = filteredRecords.filter(record => {
      return String(record.user_id) === selectedUser;
    });
  }

  renderHistory(filteredRecords);
}

// Inicializa a tela de relatórios.
async function initializeReports() {
  try {
    await loadCurrentUser();

    if (!currentUser) return;

    await Promise.all([
      loadReport(),
      loadHistory()
    ]);

  } catch (error) {
    showError(error.message);
  }
}

// Atualiza a tabela quando o período muda.
periodFilter.addEventListener("change", applyFilters);

// Atualiza a tabela quando o usuário muda.
userFilter.addEventListener("change", applyFilters);

// Inicia o carregamento.
initializeReports();
