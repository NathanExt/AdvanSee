// Software Management JavaScript - Versão Atualizada
class SoftwareManager {
    constructor() {
        this.charts = {};
        this.availableAssets = [];
        this.selectedAssets = new Set();
        this.selectedSoftware = new Map(); // Map para rastrear software selecionado e seu status
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Event listeners para tabs
        document.addEventListener('DOMContentLoaded', () => {
            this.initializeTabs();
            this.setupRealTimeSearch();
        });
    }

    initializeTabs() {
        const urlParams = new URLSearchParams(window.location.search);
        const activeTab = urlParams.get('tab') || 'dashboard';
        
        // Ativar a aba correspondente
        const tabButton = document.querySelector(`[data-bs-target="#${activeTab}"]`);
        if (tabButton) {
            const tab = new bootstrap.Tab(tabButton);
            tab.show();
        }
    }

    initializeCharts(chartData) {
        if (!chartData) {
            console.warn('Dados do gráfico não fornecidos');
            return;
        }

        // Aguardar elementos DOM estarem disponíveis
        setTimeout(() => {
            try {
                // Gráfico Top Software Instalado
                if (chartData.top_installed) {
                    this.createBarChart('topInstalledChart', 'Top 10 Software Mais Instalados', chartData.top_installed);
                }
                
                // Gráfico Top Fabricantes
                if (chartData.top_vendors) {
                    this.createBarChart('topVendorsChart', 'Top 10 Fabricantes', chartData.top_vendors);
                }
                
                // Gráfico Distribuição por Sistema Operacional
                if (chartData.os_distribution) {
                    this.createPieChart('osDistributionChart', 'Distribuição por Sistema Operacional', chartData.os_distribution);
                }
                
                // Gráfico Distribuição por Versão
                if (chartData.version_distribution) {
                    this.createBarChart('versionDistributionChart', 'Distribuição por Versão', chartData.version_distribution);
                }
            } catch (error) {
                console.error('Erro ao inicializar gráficos:', error);
            }
        }, 100);
    }

    createBarChart(canvasId, title, data) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) {
            console.warn(`Canvas ${canvasId} não encontrado`);
            return;
        }

        if (!data || !data.labels || !data.data) {
            console.warn(`Dados inválidos para gráfico ${canvasId}`);
            return;
        }

        // Destruir gráfico existente se houver
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }

        this.charts[canvasId] = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: title,
                    data: data.data,
                    backgroundColor: this.getRandomColors(data.labels.length),
                    borderColor: this.getRandomColors(data.labels.length),
                    borderWidth: 1
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

    createPieChart(canvasId, title, data) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) {
            console.warn(`Canvas ${canvasId} não encontrado`);
            return;
        }

        if (!data || !data.labels || !data.data) {
            console.warn(`Dados inválidos para gráfico ${canvasId}`);
            return;
        }

        // Destruir gráfico existente se houver
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }

        this.charts[canvasId] = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.data,
                    backgroundColor: this.getRandomColors(data.labels.length),
                    borderColor: '#fff',
                    borderWidth: 2
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

    getRandomColors(count) {
        const colors = [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
            '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384'
        ];
        
        const result = [];
        for (let i = 0; i < count; i++) {
            result.push(colors[i % colors.length]);
        }
        return result;
    }

    // Funções para o modal de criação de grupos
    initializeCreateGroupModal() {
        console.log('Inicializando modal de criação de grupo');
        
        // Limpar estado anterior
        this.clearModalState();
        
        // Carregar dados
        this.loadAvailableSoftware();
        this.loadAvailableAssets();
        this.loadAssetGroups(); // Carregar grupos de assets
        
        // Configurar eventos
        this.setupModalEvents();
    }

    clearModalState() {
        // Limpar seleções anteriores
        this.selectedSoftware.clear();
        this.selectedAssets.clear();
        
        // Limpar listas visuais
        const selectedSoftwareList = document.getElementById('selected_software_list');
        if (selectedSoftwareList) {
            selectedSoftwareList.innerHTML = `
                <div class="text-muted text-center py-4">
                    <i class="bi bi-list"></i>
                    <p>Nenhum software selecionado</p>
                </div>
            `;
        }
        
        const selectedAssetsList = document.getElementById('selected_assets_list');
        if (selectedAssetsList) {
            selectedAssetsList.innerHTML = `
                <div class="text-muted text-center py-3">
                    <i class="bi bi-pc-display"></i>
                    <p>Nenhum asset selecionado</p>
                </div>
            `;
        }
        
        // Limpar formulário
        const form = document.getElementById('createGroupForm');
        if (form) {
            form.reset();
        }
    }

    loadAvailableSoftware() {
        const container = document.getElementById('available_software_list');
        if (container) {
            container.innerHTML = '<div class="text-center py-3"><div class="spinner-border spinner-border-sm"></div> Carregando...</div>';
        }

        fetch('/software/api/search')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                this.displayAvailableSoftware(data);
            })
            .catch(error => {
                console.error('Erro ao carregar software:', error);
                if (container) {
                    container.innerHTML = '<div class="text-center text-danger py-3">Erro ao carregar software disponível</div>';
                }
            });
    }

    displayAvailableSoftware(softwareList) {
        const container = document.getElementById('available_software_list');
        if (!container) return;

        if (!softwareList || softwareList.length === 0) {
            container.innerHTML = '<div class="text-muted text-center py-3">Nenhum software encontrado</div>';
            return;
        }

        const html = softwareList.map(software => {
            const softwareKey = `${software.name}|${software.vendor}|${software.version}`;
            const isSelected = this.selectedSoftware.has(softwareKey);
            const status = isSelected ? this.selectedSoftware.get(softwareKey) : null;
            
            return `
                <div class="software-item d-flex justify-content-between align-items-center p-2 border-bottom" 
                     data-software-key="${this.escapeHtml(softwareKey)}">
                    <div>
                        <strong>${this.escapeHtml(software.name || '')}</strong>
                        <br>
                        <small class="text-muted">${this.escapeHtml(software.vendor || '')} - ${this.escapeHtml(software.version || '')}</small>
                    </div>
                    <div class="btn-group btn-group-sm" role="group">
                        <button class="btn ${status === 'allowed' ? 'btn-success' : 'btn-outline-success'}" 
                                onclick="softwareManager.toggleSoftwareStatus('${this.escapeHtml(softwareKey)}', 'allowed')" 
                                title="Permitir">
                            <i class="bi bi-check-circle"></i>
                        </button>
                        <button class="btn ${status === 'blocked' ? 'btn-danger' : 'btn-outline-danger'}" 
                                onclick="softwareManager.toggleSoftwareStatus('${this.escapeHtml(softwareKey)}', 'blocked')" 
                                title="Proibir">
                            <i class="bi bi-x-circle"></i>
                        </button>
                    </div>
                </div>
            `;
        }).join('');

        container.innerHTML = html;
    }

    toggleSoftwareStatus(softwareKey, status) {
        const [name, vendor, version] = softwareKey.split('|');
        
        // Se já está selecionado com o mesmo status, remover
        if (this.selectedSoftware.has(softwareKey) && this.selectedSoftware.get(softwareKey) === status) {
            this.selectedSoftware.delete(softwareKey);
        } else {
            // Caso contrário, definir o novo status
            this.selectedSoftware.set(softwareKey, status);
        }
        
        // Atualizar visualizações
        this.updateSoftwareSelectionDisplay();
        this.updateAvailableSoftwareButtons();
    }

    updateSoftwareSelectionDisplay() {
        const container = document.getElementById('selected_software_list');
        if (!container) return;

        if (this.selectedSoftware.size === 0) {
            container.innerHTML = `
                <div class="text-muted text-center py-4">
                    <i class="bi bi-list"></i>
                    <p>Nenhum software selecionado</p>
                </div>
            `;
            return;
        }

        const allowedSoftware = [];
        const blockedSoftware = [];

        this.selectedSoftware.forEach((status, softwareKey) => {
            const [name, vendor, version] = softwareKey.split('|');
            const item = { name, vendor, version, key: softwareKey };
            
            if (status === 'allowed') {
                allowedSoftware.push(item);
            } else {
                blockedSoftware.push(item);
            }
        });

        let html = '';

        if (allowedSoftware.length > 0) {
            html += '<h6 class="text-success mb-2"><i class="bi bi-check-circle"></i> Software Permitido</h6>';
            html += '<div class="mb-3">';
            allowedSoftware.forEach(item => {
                html += `
                    <div class="selected-software-item d-flex justify-content-between align-items-center p-2 border-bottom">
                        <div>
                            <strong>${this.escapeHtml(item.name)}</strong>
                            <br>
                            <small class="text-muted">${this.escapeHtml(item.vendor)} - ${this.escapeHtml(item.version)}</small>
                        </div>
                        <button class="btn btn-sm btn-outline-danger" 
                                onclick="softwareManager.removeSoftwareSelection('${this.escapeHtml(item.key)}')" 
                                title="Remover">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                `;
            });
            html += '</div>';
        }

        if (blockedSoftware.length > 0) {
            html += '<h6 class="text-danger mb-2"><i class="bi bi-x-circle"></i> Software Proibido</h6>';
            html += '<div class="mb-3">';
            blockedSoftware.forEach(item => {
                html += `
                    <div class="selected-software-item d-flex justify-content-between align-items-center p-2 border-bottom">
                        <div>
                            <strong>${this.escapeHtml(item.name)}</strong>
                            <br>
                            <small class="text-muted">${this.escapeHtml(item.vendor)} - ${this.escapeHtml(item.version)}</small>
                        </div>
                        <button class="btn btn-sm btn-outline-danger" 
                                onclick="softwareManager.removeSoftwareSelection('${this.escapeHtml(item.key)}')" 
                                title="Remover">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                `;
            });
            html += '</div>';
        }

        container.innerHTML = html;
    }

    updateAvailableSoftwareButtons() {
        // Atualizar os botões na lista de software disponível
        const availableItems = document.querySelectorAll('#available_software_list .software-item');
        
        availableItems.forEach(item => {
            const softwareKey = item.dataset.softwareKey;
            const status = this.selectedSoftware.get(softwareKey);
            
            const allowButton = item.querySelector('.btn-group .btn:first-child');
            const blockButton = item.querySelector('.btn-group .btn:last-child');
            
            if (allowButton) {
                if (status === 'allowed') {
                    allowButton.classList.remove('btn-outline-success');
                    allowButton.classList.add('btn-success');
                } else {
                    allowButton.classList.remove('btn-success');
                    allowButton.classList.add('btn-outline-success');
                }
            }
            
            if (blockButton) {
                if (status === 'blocked') {
                    blockButton.classList.remove('btn-outline-danger');
                    blockButton.classList.add('btn-danger');
                } else {
                    blockButton.classList.remove('btn-danger');
                    blockButton.classList.add('btn-outline-danger');
                }
            }
        });
    }

    removeSoftwareSelection(softwareKey) {
        this.selectedSoftware.delete(softwareKey);
        this.updateSoftwareSelectionDisplay();
        this.updateAvailableSoftwareButtons();
    }

    loadAssetGroups() {
        const select = document.getElementById('asset_group_select');
        if (!select) return;
        
        // Limpar opções existentes
        select.innerHTML = '<option value="">-- Selecione um grupo de assets --</option>';
        
        fetch('/assets/api/groups')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.groups && data.groups.length > 0) {
                    data.groups.forEach(group => {
                        const option = document.createElement('option');
                        option.value = group.id;
                        option.textContent = `${group.name} (${group.asset_count} assets)`;
                        select.appendChild(option);
                    });
                } else {
                    const option = document.createElement('option');
                    option.value = "";
                    option.textContent = "Nenhum grupo de assets disponível";
                    option.disabled = true;
                    select.appendChild(option);
                }
            })
            .catch(error => {
                console.error('Erro ao carregar grupos de assets:', error);
                const option = document.createElement('option');
                option.value = "";
                option.textContent = "Erro ao carregar grupos";
                option.disabled = true;
                select.appendChild(option);
            });
    }

    loadAssetsFromGroup(groupId) {
        if (!groupId) return;
        
        // Mostrar loading
        const container = document.getElementById('selected_assets_list');
        if (container) {
            const currentHTML = container.innerHTML;
            container.innerHTML += '<div class="text-center py-2"><div class="spinner-border spinner-border-sm"></div> Carregando assets do grupo...</div>';
        }
        
        fetch(`/assets/groups/${groupId}/assets`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.assets && data.assets.length > 0) {
                    // Adicionar cada asset do grupo
                    data.assets.forEach(asset => {
                        if (!this.selectedAssets.has(asset.id)) {
                            // Adicionar ao availableAssets se não estiver lá
                            const existingAsset = this.availableAssets.find(a => a.id === asset.id);
                            if (!existingAsset) {
                                this.availableAssets.push(asset);
                            }
                            
                            // Adicionar à seleção
                            this.addAssetToGroup(asset.id);
                        }
                    });
                    
                    // Mostrar mensagem de sucesso
                    this.showTemporaryMessage(`${data.assets.length} assets adicionados do grupo`, 'success');
                } else {
                    this.showTemporaryMessage('O grupo selecionado não possui assets', 'warning');
                }
                
                // Resetar o select
                document.getElementById('asset_group_select').value = '';
            })
            .catch(error => {
                console.error('Erro ao carregar assets do grupo:', error);
                this.showTemporaryMessage('Erro ao carregar assets do grupo', 'danger');
                
                // Remover loading em caso de erro
                if (container) {
                    const loadingDiv = container.querySelector('.spinner-border').parentElement;
                    if (loadingDiv) {
                        loadingDiv.remove();
                    }
                }
            });
    }

    showTemporaryMessage(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
        alertDiv.style.zIndex = '9999';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alertDiv);
        
        // Remover automaticamente após 3 segundos
        setTimeout(() => {
            alertDiv.remove();
        }, 3000);
    }

    loadAvailableAssets() {
        fetch('/software/api/assets')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                this.availableAssets = data || [];
                console.log('Assets carregados:', this.availableAssets.length);
            })
            .catch(error => {
                console.error('Erro ao carregar assets:', error);
                this.availableAssets = [];
            });
    }

    setupModalEvents() {
        // Evento para busca de software
        const softwareSearch = document.getElementById('software_search');
        if (softwareSearch) {
            softwareSearch.removeEventListener('input', this.softwareSearchHandler);
            this.softwareSearchHandler = this.debounce(() => {
                this.searchSoftware();
            }, 300);
            softwareSearch.addEventListener('input', this.softwareSearchHandler);
        }

        // Evento para busca de assets
        const assetSearch = document.getElementById('asset_search');
        if (assetSearch) {
            assetSearch.removeEventListener('input', this.assetSearchHandler);
            this.assetSearchHandler = this.debounce(() => {
                this.searchAssets();
            }, 300);
            assetSearch.addEventListener('input', this.assetSearchHandler);
        }
    }

    searchSoftware() {
        const searchTerm = document.getElementById('software_search')?.value || '';
        const container = document.getElementById('available_software_list');
        
        if (container) {
            container.innerHTML = '<div class="text-center py-3"><div class="spinner-border spinner-border-sm"></div> Buscando...</div>';
        }

        fetch(`/software/api/search?search_name=${encodeURIComponent(searchTerm)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                this.displayAvailableSoftware(data);
            })
            .catch(error => {
                console.error('Erro na busca de software:', error);
                if (container) {
                    container.innerHTML = '<div class="text-center text-danger py-3">Erro na busca</div>';
                }
            });
    }

    searchAssets() {
        const searchTerm = document.getElementById('asset_search')?.value || '';
        if (!this.availableAssets) return;

        const filteredAssets = this.availableAssets.filter(asset => 
            asset.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            asset.asset_tag?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            asset.ip_address?.toLowerCase().includes(searchTerm.toLowerCase())
        );

        this.displayAssetSearchResults(filteredAssets);
    }

    displayAssetSearchResults(assets) {
        const container = document.getElementById('asset_search_results');
        if (!container) {
            // Criar container se não existir
            const assetSearch = document.getElementById('asset_search');
            if (assetSearch && assetSearch.parentNode) {
                const resultsContainer = document.createElement('div');
                resultsContainer.id = 'asset_search_results';
                resultsContainer.className = 'mt-2 border rounded p-2';
                resultsContainer.style.maxHeight = '200px';
                resultsContainer.style.overflowY = 'auto';
                assetSearch.parentNode.parentNode.appendChild(resultsContainer);
            }
            return;
        }

        if (!assets || assets.length === 0) {
            container.innerHTML = '<div class="text-muted text-center py-2">Nenhum asset encontrado</div>';
            return;
        }

        const html = assets.slice(0, 10).map(asset => { // Limitar a 10 resultados
            const isSelected = this.selectedAssets.has(asset.id);
            
            return `
                <div class="d-flex justify-content-between align-items-center p-2 border-bottom">
                    <div>
                        <strong>${this.escapeHtml(asset.name || '')}</strong>
                        <br>
                        <small class="text-muted">${this.escapeHtml(asset.asset_tag || '')} - ${this.escapeHtml(asset.ip_address || '')}</small>
                    </div>
                    <button class="btn btn-sm ${isSelected ? 'btn-success' : 'btn-outline-primary'}" 
                            onclick="softwareManager.toggleAssetSelection(${asset.id})" 
                            title="${isSelected ? 'Remover' : 'Adicionar'}">
                        <i class="bi ${isSelected ? 'bi-check' : 'bi-plus'}"></i>
                    </button>
                </div>
            `;
        }).join('');

        container.innerHTML = html;
    }

    toggleAssetSelection(assetId) {
        if (this.selectedAssets.has(assetId)) {
            this.removeAssetFromGroup(assetId);
        } else {
            this.addAssetToGroup(assetId);
        }
        
        // Atualizar visualização da busca se existir
        const searchTerm = document.getElementById('asset_search')?.value || '';
        if (searchTerm) {
            this.searchAssets();
        }
    }

    addAssetToGroup(assetId) {
        const asset = this.availableAssets.find(a => a.id === assetId);
        if (!asset) return;

        // Verificar se já foi selecionado
        if (this.selectedAssets.has(assetId)) {
            return;
        }

        const container = document.getElementById('selected_assets_list');
        if (!container) return;

        // Remover mensagem de "nenhum asset" se for a primeira adição
        if (this.selectedAssets.size === 0) {
            container.innerHTML = '';
        }

        this.selectedAssets.add(assetId);

        const assetItem = document.createElement('div');
        assetItem.className = 'asset-item d-flex justify-content-between align-items-center p-2 border-bottom';
        assetItem.dataset.assetId = assetId;

        assetItem.innerHTML = `
            <div>
                <strong>${this.escapeHtml(asset.name || '')}</strong>
                <br>
                <small class="text-muted">${this.escapeHtml(asset.asset_tag || '')} - ${this.escapeHtml(asset.ip_address || '')}</small>
            </div>
            <button class="btn btn-sm btn-outline-danger" 
                    onclick="softwareManager.removeAssetFromGroup(${assetId})" 
                    title="Remover">
                <i class="bi bi-trash"></i>
            </button>
        `;

        container.appendChild(assetItem);
    }

    removeAssetFromGroup(assetId) {
        this.selectedAssets.delete(assetId);
        
        const item = document.querySelector(`[data-asset-id="${assetId}"]`);
        if (item && item.parentNode) {
            item.parentNode.removeChild(item);
        }
        
        const container = document.getElementById('selected_assets_list');
        
        // Verificar se a lista ficou vazia
        if (this.selectedAssets.size === 0 && container) {
            container.innerHTML = `
                <div class="text-muted text-center py-3">
                    <i class="bi bi-pc-display"></i>
                    <p>Nenhum asset selecionado</p>
                </div>
            `;
        }
        
        // Atualizar visualização da busca se existir
        const searchTerm = document.getElementById('asset_search')?.value || '';
        if (searchTerm) {
            this.searchAssets();
        }
    }

    selectAllAssets() {
        if (!this.availableAssets || this.availableAssets.length === 0) {
            alert('Nenhum asset disponível');
            return;
        }

        this.availableAssets.forEach(asset => {
            if (!this.selectedAssets.has(asset.id)) {
                this.addAssetToGroup(asset.id);
            }
        });
    }

    createGroup() {
        const form = document.getElementById('createGroupForm');
        if (!form) {
            alert('Formulário não encontrado');
            return;
        }

        // Validação básica
        const groupName = document.getElementById('group_name')?.value;
        if (!groupName || !groupName.trim()) {
            alert('Nome do grupo é obrigatório');
            return;
        }

        // Preparar dados de software
        const allowedSoftware = [];
        const blockedSoftware = [];
        
        this.selectedSoftware.forEach((status, softwareKey) => {
            const [name, vendor, version] = softwareKey.split('|');
            const softwareData = { name, vendor, version };
            
            if (status === 'allowed') {
                allowedSoftware.push(softwareData);
            } else {
                blockedSoftware.push(softwareData);
            }
        });

        // Atualizar inputs hidden
        document.getElementById('allowed_software_input').value = JSON.stringify(allowedSoftware);
        document.getElementById('blocked_software_input').value = JSON.stringify(blockedSoftware);
        document.getElementById('selected_assets_input').value = JSON.stringify(Array.from(this.selectedAssets));

        const formData = new FormData(form);

        // Desabilitar botão durante o envio
        const submitButton = document.querySelector('[onclick="createGroup()"]');
        if (submitButton) {
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Criando...';
        }

        fetch('/software/groups', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Fechar modal e recarregar página
                const modal = bootstrap.Modal.getInstance(document.getElementById('createGroupModal'));
                if (modal) modal.hide();
                location.href = '/software?tab=grupos';
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

    // Funções para visualização e edição de grupos
    viewGroupDetails(groupId) {
        console.log('Ver detalhes do grupo:', groupId);
        
        this.showLoadingInModal('groupDetailsModal', 'groupDetailsContent');
        
        fetch(`/software/groups/${groupId}/details`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                this.showGroupDetailsModal(data);
            })
            .catch(error => {
                console.error('Erro ao carregar detalhes do grupo:', error);
                this.showErrorInModal('groupDetailsModal', 'groupDetailsContent', 'Erro ao carregar detalhes do grupo');
            });
    }

    showGroupDetailsModal(groupData) {
        const modal = new bootstrap.Modal(document.getElementById('groupDetailsModal'));
        const content = document.getElementById('groupDetailsContent');
        
        const createdAt = groupData.created_at ? new Date(groupData.created_at).toLocaleDateString() : 'N/A';
        
        content.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <h6>Informações do Grupo</h6>
                    <p><strong>Nome:</strong> ${this.escapeHtml(groupData.name || '')}</p>
                    <p><strong>Descrição:</strong> ${this.escapeHtml(groupData.description || 'N/A')}</p>
                    <p><strong>Tipo:</strong> ${groupData.is_required ? 'Obrigatório' : 'Opcional'}</p>
                    <p><strong>Criado em:</strong> ${createdAt}</p>
                </div>
                <div class="col-md-6">
                    <h6>Estatísticas</h6>
                    <p><strong>Software Permitido:</strong> ${groupData.allowed_count || 0}</p>
                    <p><strong>Software Proibido:</strong> ${groupData.blocked_count || 0}</p>
                    <p><strong>Assets Atribuídos:</strong> ${groupData.assets_count || 0}</p>
                </div>
            </div>
            <div class="row mt-3">
                <div class="col-12">
                    <h6>Software do Grupo</h6>
                    <div class="table-responsive">
                        <table class="table table-sm">
                            <thead>
                                <tr>
                                    <th>Nome</th>
                                    <th>Fabricante</th>
                                    <th>Versão</th>
                                    <th>Tipo</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${groupData.software ? groupData.software.map(item => `
                                    <tr>
                                        <td>${this.escapeHtml(item.software_name || '')}</td>
                                        <td>${this.escapeHtml(item.software_vendor || 'N/A')}</td>
                                        <td>${this.escapeHtml(item.software_version || 'N/A')}</td>
                                        <td>
                                            <span class="badge ${item.is_required ? 'bg-success' : 'bg-danger'}">
                                                ${item.is_required ? 'Permitido' : 'Proibido'}
                                            </span>
                                        </td>
                                    </tr>
                                `).join('') : '<tr><td colspan="4">Nenhum software</td></tr>'}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `;
        
        modal.show();
    }

    editGroup(groupId) {
        console.log('Editar grupo:', groupId);
        
        this.showLoadingInModal('editGroupModal', 'editGroupContent');
        
        fetch(`/software/groups/${groupId}/details`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                this.showEditGroupModal(data);
            })
            .catch(error => {
                console.error('Erro ao carregar grupo:', error);
                this.showErrorInModal('editGroupModal', 'editGroupContent', 'Erro ao carregar dados do grupo');
            });
    }

    showEditGroupModal(groupData) {
        const modal = new bootstrap.Modal(document.getElementById('editGroupModal'));
        const content = document.getElementById('editGroupContent');
        
        content.innerHTML = `
            <form method="POST" action="/software/groups/${groupData.id}/update">
                <div class="mb-3">
                    <label for="edit_group_name" class="form-label">Nome do Grupo</label>
                    <input type="text" class="form-control" id="edit_group_name" name="name" 
                           value="${this.escapeHtml(groupData.name || '')}" required>
                </div>
                <div class="mb-3">
                    <label for="edit_group_description" class="form-label">Descrição</label>
                    <textarea class="form-control" id="edit_group_description" name="description" 
                              rows="3">${this.escapeHtml(groupData.description || '')}</textarea>
                </div>
                <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" id="edit_group_required" 
                           name="is_required" ${groupData.is_required ? 'checked' : ''}>
                    <label class="form-check-label" for="edit_group_required">
                        Software obrigatório
                    </label>
                </div>
                <button type="submit" class="btn btn-primary">Salvar Alterações</button>
            </form>
        `;
        
        modal.show();
    }

    deleteGroup(groupId) {
        if (confirm('Tem certeza que deseja excluir este grupo?')) {
            fetch(`/software/groups/${groupId}/delete`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            }).then(response => {
                if (response.ok) {
                    location.href = '/software?tab=grupos';
                } else {
                    alert('Erro ao excluir grupo');
                }
            }).catch(error => {
                console.error('Erro:', error);
                alert('Erro ao excluir grupo');
            });
        }
    }

    // Funções auxiliares
    showLoadingInModal(modalId, contentId) {
        const content = document.getElementById(contentId);
        if (content) {
            content.innerHTML = '<div class="text-center py-4"><div class="spinner-border"></div><p class="mt-2">Carregando...</p></div>';
        }
        
        const modal = new bootstrap.Modal(document.getElementById(modalId));
        modal.show();
    }

    showErrorInModal(modalId, contentId, message) {
        const content = document.getElementById(contentId);
        if (content) {
            content.innerHTML = `<div class="text-center py-4 text-danger"><i class="bi bi-exclamation-triangle" style="font-size: 2rem;"></i><p class="mt-2">${message}</p></div>`;
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    exportToCSV() {
        console.log('Exportar para CSV');
        
        fetch('/software/api/export-csv')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                return response.blob();
            })
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'software_list.csv';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            })
            .catch(error => {
                console.error('Erro ao exportar:', error);
                alert('Erro ao exportar arquivo CSV');
            });
    }

    setupRealTimeSearch() {
        const searchName = document.getElementById('search_name');
        const searchVendor = document.getElementById('search_vendor');
        
        if (searchName) {
            searchName.addEventListener('input', this.debounce(() => {
                this.performSearch();
            }, 300));
        }
        
        if (searchVendor) {
            searchVendor.addEventListener('input', this.debounce(() => {
                this.performSearch();
            }, 300));
        }
    }

    performSearch() {
        const searchName = document.getElementById('search_name')?.value || '';
        const searchVendor = document.getElementById('search_vendor')?.value || '';
        
        const params = new URLSearchParams();
        if (searchName) params.append('search_name', searchName);
        if (searchVendor) params.append('search_vendor', searchVendor);
        params.append('tab', 'software');
        
        window.location.href = `/software?${params.toString()}`;
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Função global para inicializar a página
window.initializeSoftwarePageFromTemplate = function(chartData) {
    window.softwareManager = new SoftwareManager();
    
    if (chartData) {
        window.softwareManager.initializeCharts(chartData);
    }
    
    // Inicializar modal de criação de grupos quando necessário
    const createGroupModal = document.getElementById('createGroupModal');
    if (createGroupModal) {
        createGroupModal.addEventListener('show.bs.modal', function() {
            window.softwareManager.initializeCreateGroupModal();
        });
    }
};

// Funções globais para compatibilidade
window.editGroup = function(groupId) {
    if (window.softwareManager) {
        window.softwareManager.editGroup(groupId);
    }
};

window.deleteGroup = function(groupId) {
    if (window.softwareManager) {
        window.softwareManager.deleteGroup(groupId);
    }
};

window.viewGroupDetails = function(groupId) {
    if (window.softwareManager) {
        window.softwareManager.viewGroupDetails(groupId);
    }
};

window.exportToCSV = function() {
    if (window.softwareManager) {
        window.softwareManager.exportToCSV();
    }
};

window.createGroup = function() {
    if (window.softwareManager) {
        window.softwareManager.createGroup();
    }
};