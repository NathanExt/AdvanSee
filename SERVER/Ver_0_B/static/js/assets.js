// JavaScript para a página de assets

// Configurações de cores para gráficos
const CHART_COLORS = {
    white: '#ffffff',
    whiteTransparent: 'rgba(255, 255, 255, 0.8)',
    primary: 'rgba(54, 162, 235, 0.6)',
    primaryBorder: 'rgba(54, 162, 235, 1)',
    secondary: 'rgba(255, 99, 132, 0.6)',
    secondaryBorder: 'rgba(255, 99, 132, 1)',
    tertiary: 'rgba(75, 192, 192, 0.6)',
    tertiaryBorder: 'rgba(75, 192, 192, 1)',
    quaternary: 'rgba(255, 205, 86, 0.6)',
    quaternaryBorder: 'rgba(255, 205, 86, 1)',
    palette: [
        'rgba(54, 162, 235, 0.6)',  // Azul
        'rgba(255, 99, 132, 0.6)',  // Vermelho
        'rgba(75, 192, 192, 0.6)',  // Verde
        'rgba(255, 205, 86, 0.6)',  // Amarelo
        'rgba(153, 102, 255, 0.6)', // Roxo
        'rgba(255, 159, 64, 0.6)',  // Laranja
        'rgba(199, 199, 199, 0.6)', // Cinza
        'rgba(83, 102, 255, 0.6)',  // Azul Índigo
        'rgba(255, 99, 255, 0.6)',  // Magenta
        'rgba(99, 255, 132, 0.6)'   // Verde Claro
    ]
};

// Configurações padrão para gráficos
const DEFAULT_CHART_OPTIONS = {
    responsive: true,
    plugins: {
        title: {
            display: true,
            color: CHART_COLORS.white,
            font: {
                size: 14,
                weight: 'bold'
            }
        },
        legend: {
            display: true,
            position: 'top',
            labels: {
                color: CHART_COLORS.white,
                font: {
                    size: 12
                }
            }
        }
    },
    scales: {
        y: {
            beginAtZero: true,
            title: {
                display: true,
                color: CHART_COLORS.white,
                font: {
                    size: 12,
                    weight: 'bold'
                }
            },
            ticks: {
                color: CHART_COLORS.white,
                font: {
                    size: 11
                }
            },
            grid: {
                color: CHART_COLORS.whiteTransparent
            }
        },
        x: {
            title: {
                display: true,
                color: CHART_COLORS.white,
                font: {
                    size: 12,
                    weight: 'bold'
                }
            },
            ticks: {
                color: CHART_COLORS.white,
                font: {
                    size: 10
                },
                maxRotation: 45,
                minRotation: 45
            },
            grid: {
                color: CHART_COLORS.whiteTransparent
            }
        }
    }
};

// Função para inicializar os gráficos
function initializeCharts(chartData) {
    // Gráfico de Equipamentos por Fabricante
    const ctxManufacturers = document.getElementById('manufacturersChart').getContext('2d');
    const manufacturersChart = new Chart(ctxManufacturers, {
        type: 'bar',
        data: {
            labels: chartData.manufacturers.labels,
            datasets: [{
                label: 'Quantidade de Equipamentos',
                data: chartData.manufacturers.data,
                backgroundColor: CHART_COLORS.primary,
                borderColor: CHART_COLORS.primaryBorder,
                borderWidth: 1
            }]
        },
        options: {
            ...DEFAULT_CHART_OPTIONS,
            plugins: {
                ...DEFAULT_CHART_OPTIONS.plugins,
                title: {
                    ...DEFAULT_CHART_OPTIONS.plugins.title,
                    text: 'Equipamentos por Fabricante'
                }
            },
            scales: {
                ...DEFAULT_CHART_OPTIONS.scales,
                y: {
                    ...DEFAULT_CHART_OPTIONS.scales.y,
                    title: {
                        ...DEFAULT_CHART_OPTIONS.scales.y.title,
                        text: 'Quantidade de Equipamentos'
                    }
                },
                x: {
                    ...DEFAULT_CHART_OPTIONS.scales.x,
                    title: {
                        ...DEFAULT_CHART_OPTIONS.scales.x.title,
                        text: 'Fabricante'
                    }
                }
            }
        }
    });

    // Gráfico de Equipamentos por Modelo
    const ctxModels = document.getElementById('modelsChart').getContext('2d');
    const modelsChart = new Chart(ctxModels, {
        type: 'doughnut',
        data: {
            labels: chartData.models.labels,
            datasets: [{
                label: 'Equipamentos por Modelo',
                data: chartData.models.data,
                backgroundColor: CHART_COLORS.palette
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Equipamentos por Modelo',
                    color: CHART_COLORS.white,
                    font: {
                        size: 14,
                        weight: 'bold'
                    }
                },
                legend: {
                    display: true,
                    position: 'right',
                    labels: {
                        color: CHART_COLORS.white,
                        font: {
                            size: 11
                        }
                    }
                }
            }
        }
    });

    // Gráfico de Status dos Assets
    const ctxStatus = document.getElementById('statusChart').getContext('2d');
    const statusChart = new Chart(ctxStatus, {
        type: 'pie',
        data: {
            labels: chartData.status.labels,
            datasets: [{
                label: 'Status dos Assets',
                data: chartData.status.data,
                backgroundColor: CHART_COLORS.palette.slice(0, chartData.status.labels.length)
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Status dos Assets',
                    color: CHART_COLORS.white,
                    font: {
                        size: 14,
                        weight: 'bold'
                    }
                },
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        color: CHART_COLORS.white,
                        font: {
                            size: 11
                        }
                    }
                }
            }
        }
    });

    // Gráfico de Fabricantes PMOC
    const ctxPmocManufacturers = document.getElementById('pmocManufacturersChart').getContext('2d');
    const pmocManufacturersChart = new Chart(ctxPmocManufacturers, {
        type: 'bar',
        data: {
            labels: chartData.pmoc_manufacturers.labels,
            datasets: [{
                label: 'Equipamentos PMOC',
                data: chartData.pmoc_manufacturers.data,
                backgroundColor: CHART_COLORS.tertiary,
                borderColor: CHART_COLORS.tertiaryBorder,
                borderWidth: 1
            }]
        },
        options: {
            ...DEFAULT_CHART_OPTIONS,
            plugins: {
                ...DEFAULT_CHART_OPTIONS.plugins,
                title: {
                    ...DEFAULT_CHART_OPTIONS.plugins.title,
                    text: 'Fabricantes no PMOC'
                }
            },
            scales: {
                ...DEFAULT_CHART_OPTIONS.scales,
                y: {
                    ...DEFAULT_CHART_OPTIONS.scales.y,
                    title: {
                        ...DEFAULT_CHART_OPTIONS.scales.y.title,
                        text: 'Quantidade de Equipamentos'
                    }
                },
                x: {
                    ...DEFAULT_CHART_OPTIONS.scales.x,
                    title: {
                        ...DEFAULT_CHART_OPTIONS.scales.x.title,
                        text: 'Fabricante'
                    }
                }
            }
        }
    });
}

// Função para busca dinâmica
function performLiveSearch() {
    const searchName = document.getElementById('search_name').value;
    const searchManufacturer = document.getElementById('search_manufacturer').value;
    const searchModel = document.getElementById('search_model').value;
    const searchUser = document.getElementById('search_user').value;
    const searchStatus = document.getElementById('search_status').value;
    
    // Usar a URL da API de busca
    const apiUrl = window.location.origin + '/assets/api/search';
    
    const params = new URLSearchParams({
        search_name: searchName,
        search_manufacturer: searchManufacturer,
        search_model: searchModel,
        search_user: searchUser,
        search_status: searchStatus
    });
    
    fetch(`${apiUrl}?${params}`)
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#assetsTable tbody');
            tbody.innerHTML = '';
            
            if (data.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="8" class="text-center text-muted">
                            <i class="fas fa-info-circle"></i> Nenhum asset encontrado.
                        </td>
                    </tr>
                `;
            } else {
                data.forEach(asset => {
                    const statusBadgeClass = asset.status === 'active' ? 'success' : 
                                           asset.status === 'inactive' ? 'warning' : 'secondary';
                    
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${asset.id}</td>
                        <td>${asset.asset_tag}</td>
                        <td>${asset.name}</td>
                        <td>${asset.computer_model}</td>
                        <td>${asset.computer_manufacturer}</td>
                        <td>${asset.logged_user}</td>
                        <td>
                            <span class="badge badge-${statusBadgeClass}">
                                ${asset.status}
                            </span>
                        </td>
                        <td>
                            <a href="/asset_detail/${asset.id}" class="btn btn-sm btn-info">
                                <i class="fas fa-eye"></i> Detalhes
                            </a>
                        </td>
                    `;
                    tbody.appendChild(row);
                });
            }
            
            // Atualizar contador de resultados
            document.querySelector('.card-header h5').textContent = `Lista de Assets (${data.length} resultados)`;
        })
        .catch(error => {
            console.error('Erro na busca:', error);
            alert('Erro ao realizar busca. Tente novamente.');
        });
}

// Função de debounce para evitar muitas requisições
function debounce(func, wait) {
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

// Função para inicializar os event listeners
function initializeEventListeners() {
    // Busca em tempo real ao digitar
    const searchInputs = [
        'search_name',
        'search_manufacturer', 
        'search_model',
        'search_user',
        'search_status'
    ];
    
    searchInputs.forEach(inputId => {
        const input = document.getElementById(inputId);
        if (input) {
            if (input.type === 'text') {
                input.addEventListener('input', debounce(performLiveSearch, 500));
            } else {
                input.addEventListener('change', performLiveSearch);
            }
        }
    });
}

// Função global para inicializar tudo
function initializeAssetsPage(chartData) {
    console.log('Inicializando página de assets...', chartData);
    
    // Inicializar gráficos
    initializeCharts(chartData);
    
    // Inicializar event listeners
    initializeEventListeners();
    
    console.log('Página de assets inicializada com sucesso!');
}

// Função para inicializar a página quando chamada pelo template
function initializeAssetsPageFromTemplate(chartData) {
    // Aguardar um pouco para garantir que todos os elementos estão carregados
    setTimeout(() => {
        initializeAssetsPage(chartData);
    }, 100);
}

// Exportar funções para uso global
window.initializeAssetsPage = initializeAssetsPage;
window.initializeAssetsPageFromTemplate = initializeAssetsPageFromTemplate; 