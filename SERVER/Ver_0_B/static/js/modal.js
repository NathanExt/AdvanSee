function abrirModal(commandType, assetId) {
    document.getElementById('modalOverlay').style.display = 'flex';
    const modalTitle = document.getElementById('modalTitle');
    const dynamicTableContainer = document.getElementById('dynamicTableContainer');

    modalTitle.innerText = `Dados para ${commandType}`;
    dynamicTableContainer.innerHTML = ''; // Limpa qualquer conteúdo anterior

    // Simulação de dados com base no tipo de comando
    let tableHtml = '<table class="table table-sm table-striped table-bordered">';
    tableHtml += '<thead><tr><th>Chave</th><th>Valor</th></tr></thead><tbody>';

    if (commandType === 'PROCESSOS') {
        tableHtml += `
            <tr><td>ID do Ativo</td><td>${assetId}</td></tr>
            <tr><td>Comando</td><td>Listar Processos</td></tr>
            <tr><td>Status</td><td>Executando</td></tr>
            <tr><td>PID Exemplo</td><td>1234 (chrome.exe)</td></tr>
            <tr><td>PID Exemplo</td><td>5678 (explorer.exe)</td></tr>
            <tr><td>Data/Hora</td><td>${new Date().toLocaleString()}</td></tr>
        `;
    } else if (commandType === 'FORCE_GPO') {
        tableHtml += `
            <tr><td>ID do Ativo</td><td>${assetId}</td></tr>
            <tr><td>Comando</td><td>Forçar Atualização GPO</td></tr>
            <tr><td>Status</td><td>Enviado para o Agente</td></tr>
            <tr><td>Resultado Esperado</td><td>GPOs serão aplicadas</td></tr>
            <tr><td>Data/Hora</td><td>${new Date().toLocaleString()}</td></tr>
        `;
    } else if (commandType === 'FORCE_CHECKIN') {
        tableHtml += `
            <tr><td>ID do Ativo</td><td>${assetId}</td></tr>
            <tr><td>Comando</td><td>Forçar Check-in do Agente</td></tr>
            <tr><td>Status</td><td>Enviado para o Agente</td></tr>
            <tr><td>Resultado Esperado</td><td>Agente reportará status</td></tr>
            <tr><td>Data/Hora</td><td>${new Date().toLocaleString()}</td></tr>
        `;
    } else {
        tableHtml += `<tr><td colspan="2">Nenhum dado específico para este comando.</td></tr>`;
    }

    tableHtml += '</tbody></table>';
    dynamicTableContainer.innerHTML = tableHtml;

    // Em um cenário real, você faria uma requisição AJAX aqui:
    /*
    fetch(`/api/get_command_data?type=${commandType}&asset_id=${assetId}`)
        .then(response => response.json())
        .then(data => {
            // Construir a tabela com os 'data' recebidos
            let fetchedTableHtml = '<table class="table table-sm table-striped table-bordered">';
            // ... lógica para iterar sobre 'data' e criar linhas da tabela
            fetchedTableHtml += '</table>';
            dynamicTableContainer.innerHTML = fetchedTableHtml;
        })
        .catch(error => {
            console.error('Erro ao buscar dados:', error);
            dynamicTableContainer.innerHTML = '<p style="color: red;">Erro ao carregar dados.</p>';
        });
    */
}

function fecharModal() {
    document.getElementById('modalOverlay').style.display = 'none';
}

// Fecha ao clicar fora do modal
window.onclick = function(event) {
    let modal = document.getElementById('modalOverlay');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}