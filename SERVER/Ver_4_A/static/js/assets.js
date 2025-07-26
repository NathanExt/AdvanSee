// Assets JavaScript - Ambiente ISAC

// Variáveis globais
let selectedAssetsForGroup = new Set();
let availableAssets = [];

// Função para inicializar a página de assets
function initializeAssetsPageFromTemplate(chartData) {
    if (!chartData) {
        console.error('Dados do gráfico não fornecidos');
        return;
    }
    
    // Inicializar gráficos
    initializeCharts(chartData);
    
    // Configurar funcionalidades de busca
    setupSearchFunctionality();
    
    // Configurar botões de sincronização
    setupSyncButtons();
    
    // Configurar modal de grupos
    setupAssetGroupModal();
}

// Inicializar gráficos
function initializeCharts(chartData) {
    // Gráfico de Status
    if (chartData.status && chartData.status.labels.length > 0) {
        const ctx = document.getElementById('statusChart');
        if (ctx) {
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: chartData.status.labels,
                    datasets: [{
                        data: chartData.status.data,
                        backgroundColor: [
                            '#28a745', // active - verde
                            '#ffc107', // inactive - amarelo
                            '#6c757d'  // outros - cinza
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }
    }
    
    // Gráfico de Sistemas Operacionais
    if (chartData.operating_systems && chartData.operating_systems.labels.length > 0) {
        const ctx = document.getElementById('osChart');
        if (ctx) {
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: chartData.operating_systems.labels,
                    datasets: [{
                        data: chartData.operating_systems.data,
                        backgroundColor: [
                            '#0d6efd', '#6610f2', '#6f42c1', '#d63384', '#dc3545',
                            '#fd7e14', '#ffc107', '#28a745', '#20c997', '#17a2b8'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'right'
                        }
                    }
                }
            });
        }
    }
    
    // Gráfico de Fabricantes
    if (chartData.manufacturers && chartData.manufacturers.labels.length > 0) {
        const ctx = document.getElementById('manufacturersChart');
        if (ctx) {
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: chartData.manufacturers.labels,
                    datasets: [{
                        label: 'Quantidade',
                        data: chartData.manufacturers.data,
                        backgroundColor: '#0d6efd'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
        }
    }
    
    // Gráfico de Modelos
    if (chartData.models && chartData.models.labels.length > 0) {
        const ctx = document.getElementById('modelsChart');
        if (ctx) {
            new Chart(ctx, {
                type: 'horizontalBar',
                data: {
                    labels: chartData.models.labels,
                    datasets: [{
                        label: 'Quantidade',
                        data: chartData.models.data,
                        backgroundColor: '#28a745'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            beginAtZero: true
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
        }
    }
    
    // Gráfico de Departamentos
    if (chartData.departments && chartData.departments.labels.length > 0) {
        const ctx = document.getElementById('departmentChart');
        if (ctx) {
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: chartData.departments.labels,
                    datasets: [{
                        label: 'Assets',
                        data: chartData.departments.data,
                        backgroundColor: '#ffc107'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
        }
    }
    
    // Gráfico de Idade dos Equipamentos
    if (chartData.age_distribution && chartData.age_distribution.labels.length > 0) {
        const ctx = document.getElementById('ageChart');
        if (ctx) {
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: chartData.age_distribution.labels,
                    datasets: [{
                        label: 'Quantidade de Assets',
                        data: chartData.age_distribution.data,
                        borderColor: '#dc3545',
                        backgroundColor: 'rgba(220, 53, 69, 0.1)',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
    }
}

// Configurar funcionalidades de busca
function setupSearchFunctionality() {
    // Busca automática ao digitar (debounce)
    let searchTimeout;
    const searchInputs = ['search_name', 'search_user'];
    
    searchInputs.forEach(inputId => {
        const input = document.getElementById(inputId);
        if (input) {
            input.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    performSearch();
                }, 500); // Aguarda 500ms após parar de digitar
            });
        }
    });
    
    // Para selects, busca imediatamente
    const searchSelects = ['search_manufacturer', 'search_model', 'search_status'];
    searchSelects.forEach(selectId => {
        const select = document.getElementById(selectId);
        if (select) {
            select.addEventListener('change', function() {
                performSearch();
            });
        }
    });
}

// Configurar botões de sincronização
function setupSyncButtons() {
    const syncPmocBtn = document.getElementById('syncPmocBtn');
    const syncPmocV2Btn = document.getElementById('syncPmocV2Btn');
    
    if (syncPmocBtn) {
        syncPmocBtn.addEventListener('click', function() {
            executeSync('/assets/sync-pmoc', syncPmocBtn, '<i class="bi bi-arrow-clockwise"></i> Sincronizar PMOC (API)');
        });
    }
    
    if (syncPmocV2Btn) {
        syncPmocV2Btn.addEventListener('click', function() {
            executeSync('/assets/sync-pmoc-v2', syncPmocV2Btn, '<i class="bi bi-database"></i> Sincronizar PMOC (Banco)');
        });
    }
}

// Configurar modal de grupos de assets
function setupAssetGroupModal() {
    const modal = document.getElementById('createAssetGroupModal');
    if (modal) {
        modal.addEventListener('show.bs.modal', function() {
            // Limpar seleção anterior
            selectedAssetsForGroup.clear();
            document.getElementById('selected_assets_count').textContent = '0';
            
            // Carregar assets disponíveis
            loadAvailableAssetsForGroup();
            
            // Limpar formulário
            document.getElementById('createAssetGroupForm').reset();
        });
    }
}

// Carregar assets disponíveis para grupo
function loadAvailableAssetsForGroup() {
    const container = document.getElementById('available_assets_list');
    if (!container) return;
    
    container.innerHTML = '<div class="text-center py-3"><div class="spinner-border spinner-border-sm"></div> Carregando...</div>';
    
    fetch('/assets/api/search')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.assets) {
                availableAssets = data.assets;
                displayAvailableAssetsForGroup(data.assets);
            }
        })
        .catch(error => {
            console.error('Erro ao carregar assets:', error);
            container.innerHTML = '<div class="text-center text-danger py-3">Erro ao carregar assets</div>';
        });
}

// Exibir assets disponíveis para seleção
function displayAvailableAssetsForGroup(assets) {
    const container = document.getElementById('available_assets_list');
    if (!container) return;
    
    if (!assets || assets.length === 0) {
        container.innerHTML = '<div class="text-muted text-center py-3">Nenhum asset disponível</div>';
        return;
    }
    
    let html = '<div class="list-group list-group-flush">';
    assets.forEach(asset => {
        const isSelected = selectedAssetsForGroup.has(asset.id);
        html += `
            <label class="list-group-item list-group-item-action">
                <div class="d-flex align-items-center">
                    <input class="form-check-input me-2" type="checkbox" 
                           value="${asset.id}" 
                           ${isSelected ? 'checked' : ''}
                           onchange="toggleAssetSelection(${asset.id})">
                    <div class="flex-grow-1">
                        <strong>${escapeHtml(asset.name || asset.asset_tag || 'N/A')}</strong>
                        <br>
                        <small class="text-muted">
                            ${escapeHtml(asset.computer_manufacturer || '')} 
                            ${escapeHtml(asset.computer_model || '')} - 
                            ${escapeHtml(asset.logged_user || 'N/A')}
                        </small>
                    </div>
                    <span class="badge bg-${asset.status === 'active' ? 'success' : 'warning'}">
                        ${asset.status || 'N/A'}
                    </span>
                </div>
            </label>
        `;
    });
    html += '</div>';
    
    container.innerHTML = html;
}

// Alternar seleção de asset
function toggleAssetSelection(assetId) {
    if (selectedAssetsForGroup.has(assetId)) {
        selectedAssetsForGroup.delete(assetId);
    } else {
        selectedAssetsForGroup.add(assetId);
    }
    
    document.getElementById('selected_assets_count').textContent = selectedAssetsForGroup.size;
}

// Buscar assets para grupo
function searchAssetsForGroup() {
    const searchTerm = document.getElementById('asset_search_modal').value.toLowerCase();
    
    if (!searchTerm) {
        displayAvailableAssetsForGroup(availableAssets);
        return;
    }
    
    const filteredAssets = availableAssets.filter(asset => {
        return (asset.name && asset.name.toLowerCase().includes(searchTerm)) ||
               (asset.asset_tag && asset.asset_tag.toLowerCase().includes(searchTerm)) ||
               (asset.logged_user && asset.logged_user.toLowerCase().includes(searchTerm)) ||
               (asset.computer_manufacturer && asset.computer_manufacturer.toLowerCase().includes(searchTerm)) ||
               (asset.computer_model && asset.computer_model.toLowerCase().includes(searchTerm));
    });
    
    displayAvailableAssetsForGroup(filteredAssets);
}

// Selecionar todos os assets
function selectAllAssetsForGroup() {
    availableAssets.forEach(asset => {
        selectedAssetsForGroup.add(asset.id);
    });
    
    // Atualizar checkboxes
    document.querySelectorAll('#available_assets_list input[type="checkbox"]').forEach(checkbox => {
        checkbox.checked = true;
    });
    
    document.getElementById('selected_assets_count').textContent = selectedAssetsForGroup.size;
}

// Limpar seleção de assets
function clearAssetSelection() {
    selectedAssetsForGroup.clear();
    
    // Desmarcar checkboxes
    document.querySelectorAll('#available_assets_list input[type="checkbox"]').forEach(checkbox => {
        checkbox.checked = false;
    });
    
    document.getElementById('selected_assets_count').textContent = '0';
}

// Criar grupo de assets
function createAssetGroup() {
    const form = document.getElementById('createAssetGroupForm');
    if (!form) return;
    
    const groupName = document.getElementById('group_name').value;
    if (!groupName || !groupName.trim()) {
        alert('Nome do grupo é obrigatório');
        return;
    }
    
    // Atualizar input hidden com assets selecionados
    document.getElementById('selected_assets_input').value = JSON.stringify(Array.from(selectedAssetsForGroup));
    
    const formData = new FormData(form);
    
    // Desabilitar botão durante envio
    const submitButton = document.querySelector('[onclick="createAssetGroup()"]');
    if (submitButton) {
        submitButton.disabled = true;
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Criando...';
    }
    
    fetch('/assets/groups', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Fechar modal e recarregar página
            const modal = bootstrap.Modal.getInstance(document.getElementById('createAssetGroupModal'));
            if (modal) modal.hide();
            
            // Recarregar a página na aba de grupos
            window.location.href = '/assets?tab=groups';
        } else {
            alert('Erro ao criar grupo: ' + (data.message || 'Erro desconhecido'));
        }
    })
    .catch(error => {
        console.error('Erro ao criar grupo:', error);
        alert('Erro ao criar grupo: ' + error.message);
    })
    .finally(() => {
        // Reabilitar botão
        if (submitButton) {
            submitButton.disabled = false;
            submitButton.innerHTML = '<i class="bi bi-check-circle"></i> Criar Grupo';
        }
    });
}

// Visualizar detalhes do grupo
function viewAssetGroupDetails(groupId) {
    fetch(`/assets/groups/${groupId}/details`)
        .then(response => response.json())
        .then(data => {
            showAssetGroupDetailsModal(data);
        })
        .catch(error => {
            console.error('Erro ao carregar detalhes:', error);
            alert('Erro ao carregar detalhes do grupo');
        });
}

// Exibir modal de detalhes
function showAssetGroupDetailsModal(groupData) {
    const content = document.getElementById('assetGroupDetailsContent');
    if (!content) return;
    
    let assetsHtml = '';
    if (groupData.assets && groupData.assets.length > 0) {
        assetsHtml = '<ul class="list-group">';
        groupData.assets.forEach(asset => {
            assetsHtml += `
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    <div>
                        <strong>${escapeHtml(asset.name || asset.asset_tag || 'N/A')}</strong>
                        <br>
                        <small class="text-muted">${escapeHtml(asset.computer_manufacturer || '')} ${escapeHtml(asset.computer_model || '')}</small>
                    </div>
                    <span class="badge bg-${asset.status === 'active' ? 'success' : 'warning'}">${asset.status || 'N/A'}</span>
                </li>
            `;
        });
        assetsHtml += '</ul>';
    } else {
        assetsHtml = '<p class="text-muted">Nenhum asset neste grupo</p>';
    }
    
    content.innerHTML = `
        <div class="row">
            <div class="col-md-6">
                <h6>Informações do Grupo</h6>
                <p><strong>Nome:</strong> ${escapeHtml(groupData.name || '')}</p>
                <p><strong>Descrição:</strong> ${escapeHtml(groupData.description || 'N/A')}</p>
                <p><strong>Criado em:</strong> ${groupData.created_at ? new Date(groupData.created_at).toLocaleString() : 'N/A'}</p>
            </div>
            <div class="col-md-6">
                <h6>Estatísticas</h6>
                <p><strong>Total de Assets:</strong> ${groupData.assets ? groupData.assets.length : 0}</p>
            </div>
        </div>
        <div class="row mt-3">
            <div class="col-12">
                <h6>Assets do Grupo</h6>
                ${assetsHtml}
            </div>
        </div>
    `;
    
    const modal = new bootstrap.Modal(document.getElementById('assetGroupDetailsModal'));
    modal.show();
}

// Editar grupo de assets
function editAssetGroup(groupId) {
    // Implementar edição de grupo
    alert('Funcionalidade de edição será implementada em breve');
}

// Excluir grupo de assets
function deleteAssetGroup(groupId) {
    if (confirm('Tem certeza que deseja excluir este grupo?')) {
        fetch(`/assets/groups/${groupId}/delete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                alert('Erro ao excluir grupo: ' + (data.message || 'Erro desconhecido'));
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao excluir grupo');
        });
    }
}

// Funções existentes mantidas...

function showLoading() {
    const loadingArea = document.getElementById('loadingArea');
    if (loadingArea) {
        loadingArea.classList.remove('d-none');
    }
}

function hideLoading() {
    const loadingArea = document.getElementById('loadingArea');
    if (loadingArea) {
        loadingArea.classList.add('d-none');
    }
}

function performSearch() {
    const searchParams = {
        search_name: document.getElementById('search_name')?.value || '',
        search_manufacturer: document.getElementById('search_manufacturer')?.value || '',
        search_model: document.getElementById('search_model')?.value || '',
        search_user: document.getElementById('search_user')?.value || '',
        search_status: document.getElementById('search_status')?.value || ''
    };
    
    showLoading();
    
    // Construir query string
    const queryString = Object.keys(searchParams)
        .filter(key => searchParams[key])
        .map(key => `${key}=${encodeURIComponent(searchParams[key])}`)
        .join('&');
    
    fetch(`/assets/api/search?${queryString}`)
        .then(response => response.json())
        .then(data => {
            hideLoading();
            displaySearchResults(data);
        })
        .catch(error => {
            hideLoading();
            console.error('Erro na busca:', error);
            showAlert('Erro ao realizar busca: ' + error.message, 'error');
        });
}

function displaySearchResults(data) {
    const tableBody = document.getElementById('assetsTableBody');
    const assetsCount = document.getElementById('assetsCount');
    
    if (!tableBody || !assetsCount) return;
    
    // Atualizar contador
    assetsCount.textContent = data.total || 0;
    
    if (!data.assets || data.assets.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="9" class="text-center text-muted">
                    <i class="bi bi-info-circle"></i> Nenhum asset encontrado.
                </td>
            </tr>
        `;
        return;
    }
    
    // Gerar HTML da tabela
    let html = '';
    data.assets.forEach(asset => {
        const statusBadgeClass = asset.status === 'active' ? 'success' : 
                                asset.status === 'inactive' ? 'warning' : 'secondary';
        
        const pmocBadge = asset.pmoc_assets_count > 0 ? 
            '<span class="badge bg-success"><i class="bi bi-check"></i> Sincronizado</span>' :
            '<span class="badge bg-secondary"><i class="bi bi-x"></i> Não encontrado</span>';
        
        html += `
            <tr>
                <td>${asset.id}</td>
                <td>${asset.asset_tag || 'N/A'}</td>
                <td>${asset.name || 'N/A'}</td>
                <td>${asset.computer_model || 'N/A'}</td>
                <td>${asset.computer_manufacturer || 'N/A'}</td>
                <td>${asset.logged_user || 'N/A'}</td>
                <td>
                    <span class="badge bg-${statusBadgeClass}">
                        ${asset.status || 'N/A'}
                    </span>
                </td>
                <td>${pmocBadge}</td>
                <td>
                    <a href="/asset/${asset.id}" class="btn btn-sm btn-info">
                        <i class="bi bi-eye"></i> Detalhes
                    </a>
                </td>
            </tr>
        `;
    });
    
    tableBody.innerHTML = html;
}

function clearSearch() {
    // Limpar campos
    const fields = ['search_name', 'search_manufacturer', 'search_model', 'search_user', 'search_status'];
    fields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.value = '';
        }
    });
    
    // Recarregar dados originais
    performSearch();
}

function exportAssetsToCSV() {
    window.location.href = '/assets/api/export-csv';
}

// Função auxiliar para escapar HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text || '';
    return div.innerHTML;
}

// Inicializar quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Verificar aba ativa pela URL
    const urlParams = new URLSearchParams(window.location.search);
    const activeTab = urlParams.get('tab');
    
    if (activeTab) {
        const tabButton = document.querySelector(`[data-bs-target="#${activeTab}"]`);
        if (tabButton) {
            const tab = new bootstrap.Tab(tabButton);
            tab.show();
        }
    }
    
    // Configurar busca automática
    setupSearchFunctionality();
    
    // Configurar botões de sincronização
    setupSyncButtons();
    
    // Configurar modal de grupos
    setupAssetGroupModal();
});