// JavaScript para a página de software

// Configurações de cores para gráficos
const CHART_COLORS = {
    white: '#ffffff',
    whiteTransparent: 'rgba(255, 255, 255, 0.8)',
    primary: 'rgba(75, 192, 192, 0.6)',
    primaryBorder: 'rgba(75, 192, 192, 1)',
    secondary: 'rgba(54, 162, 235, 0.6)',
    secondaryBorder: 'rgba(54, 162, 235, 1)',
    palette: [
        'rgba(255, 99, 132, 0.6)',
        'rgba(54, 162, 235, 0.6)',
        'rgba(255, 205, 86, 0.6)',
        'rgba(75, 192, 192, 0.6)',
        'rgba(153, 102, 255, 0.6)',
        'rgba(255, 159, 64, 0.6)',
        'rgba(199, 199, 199, 0.6)',
        'rgba(83, 102, 255, 0.6)',
        'rgba(255, 99, 255, 0.6)',
        'rgba(99, 255, 132, 0.6)'
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
    // Gráfico Geral por Softwares Instalados
    const ctxGeneral = document.getElementById('generalSoftwareChart').getContext('2d');
    const generalSoftwareChart = new Chart(ctxGeneral, {
        type: 'bar',
        data: {
            labels: chartData.general_software.labels,
            datasets: [{
                label: 'Quantidade de Instalações',
                data: chartData.general_software.data,
                backgroundColor: CHART_COLORS.primary,
                borderColor: CHART_COLORS.primaryBorder,
                borderWidth: 1
            }]
        },
        options: {
            ...DEFAULT_CHART_OPTIONS,
            maintainAspectRatio: false,
            plugins: {
                ...DEFAULT_CHART_OPTIONS.plugins,
                title: {
                    ...DEFAULT_CHART_OPTIONS.plugins.title,
                    text: 'Softwares Mais Instalados no Ambiente'
                }
            },
            scales: {
                ...DEFAULT_CHART_OPTIONS.scales,
                y: {
                    ...DEFAULT_CHART_OPTIONS.scales.y,
                    title: {
                        ...DEFAULT_CHART_OPTIONS.scales.y.title,
                        text: 'Quantidade de Instalações'
                    }
                },
                x: {
                    ...DEFAULT_CHART_OPTIONS.scales.x,
                    title: {
                        ...DEFAULT_CHART_OPTIONS.scales.x.title,
                        text: 'Software'
                    }
                }
            }
        }
    });

    // Gráfico de Software Mais Instalados
    const ctx1 = document.getElementById('topInstalledChart').getContext('2d');
    const topInstalledChart = new Chart(ctx1, {
        type: 'bar',
        data: {
            labels: chartData.top_installed.labels,
            datasets: [{
                label: 'Instalações',
                data: chartData.top_installed.data,
                backgroundColor: CHART_COLORS.secondary,
                borderColor: CHART_COLORS.secondaryBorder,
                borderWidth: 1
            }]
        },
        options: {
            ...DEFAULT_CHART_OPTIONS,
            plugins: {
                ...DEFAULT_CHART_OPTIONS.plugins,
                title: {
                    ...DEFAULT_CHART_OPTIONS.plugins.title,
                    text: 'Top 10 Software Mais Instalados'
                }
            },
            scales: {
                ...DEFAULT_CHART_OPTIONS.scales,
                y: {
                    ...DEFAULT_CHART_OPTIONS.scales.y,
                    title: {
                        ...DEFAULT_CHART_OPTIONS.scales.y.title,
                        text: 'Instalações'
                    }
                },
                x: {
                    ...DEFAULT_CHART_OPTIONS.scales.x,
                    title: {
                        ...DEFAULT_CHART_OPTIONS.scales.x.title,
                        text: 'Software'
                    }
                }
            }
        }
    });

    // Gráfico de Top Fabricantes
    const ctx2 = document.getElementById('topVendorsChart').getContext('2d');
    const topVendorsChart = new Chart(ctx2, {
        type: 'doughnut',
        data: {
            labels: chartData.top_vendors.labels,
            datasets: [{
                label: 'Software por Fabricante',
                data: chartData.top_vendors.data,
                backgroundColor: CHART_COLORS.palette
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Top 10 Fabricantes',
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

    // Gráfico de Distribuição por Fabricante
    if (document.getElementById('licenseDistributionChart')) {
        const ctx3 = document.getElementById('licenseDistributionChart').getContext('2d');
        const vendorDistributionChart = new Chart(ctx3, {
            type: 'pie',
            data: {
                labels: chartData.vendor_distribution.labels,
                datasets: [{
                    label: 'Distribuição por Fabricante',
                    data: chartData.vendor_distribution.data,
                    backgroundColor: CHART_COLORS.palette.slice(0, 8)
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Distribuição por Fabricante',
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
    }
}

// Função para busca dinâmica
function performLiveSearch() {
    const searchName = document.getElementById('search_name').value;
    const searchVendor = document.getElementById('search_vendor').value;
    
    // Usar a URL da API de busca
    const apiUrl = window.location.origin + '/software/api/search';
    
    fetch(`${apiUrl}?search_name=${searchName}&search_vendor=${searchVendor}`)
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#softwareTable tbody');
            tbody.innerHTML = '';
            
            if (data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="4">Nenhum software encontrado.</td></tr>';
            } else {
                data.forEach(software => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${software.name}</td>
                        <td>${software.vendor}</td>
                        <td>${software.version}</td>
                        <td><span class="badge badge-primary">${software.quantity}</span></td>
                    `;
                    tbody.appendChild(row);
                });
            }
            
            // Atualizar contador de resultados
            document.querySelector('.card-header h5').textContent = `Lista de Software Instalado (${data.length} resultados)`;
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
    // Verificar se existe o botão de busca (caso seja adicionado no futuro)
    const liveSearchBtn = document.getElementById('liveSearchBtn');
    if (liveSearchBtn) {
        liveSearchBtn.addEventListener('click', performLiveSearch);
    }

    // Busca em tempo real ao digitar
    const searchNameInput = document.getElementById('search_name');
    const searchVendorInput = document.getElementById('search_vendor');
    
    if (searchNameInput) {
        searchNameInput.addEventListener('input', debounce(performLiveSearch, 500));
    }
    
    if (searchVendorInput) {
        searchVendorInput.addEventListener('input', debounce(performLiveSearch, 500));
    }
}

// Função global para inicializar tudo
function initializeSoftwarePage(chartData) {
    console.log('Inicializando página de software...', chartData);
    
    // Inicializar gráficos
    initializeCharts(chartData);
    
    // Inicializar event listeners
    initializeEventListeners();
    
    console.log('Página de software inicializada com sucesso!');
}

// Função para inicializar a página quando chamada pelo template
function initializeSoftwarePageFromTemplate(chartData) {
    // Aguardar um pouco para garantir que todos os elementos estão carregados
    setTimeout(() => {
        initializeSoftwarePage(chartData);
    }, 100);
}

// Exportar funções para uso global
window.initializeSoftwarePage = initializeSoftwarePage;
window.initializeSoftwarePageFromTemplate = initializeSoftwarePageFromTemplate; 