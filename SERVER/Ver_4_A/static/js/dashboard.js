// Dashboard JavaScript - Ambiente ISAC

document.addEventListener('DOMContentLoaded', function() {
    // Gráfico de Status dos Assets
    const ctx = document.getElementById('assetStatusChart');
    if (ctx) {
        // Obter dados do template via variáveis globais
        const chartLabels = window.chartLabels || [];
        const chartValues = window.chartValues || [];
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: chartLabels,
                datasets: [{
                    data: chartValues,
                    backgroundColor: [
                        '#28a745',
                        '#ffc107',
                        '#dc3545',
                        '#17a2b8',
                        '#6c757d'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
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
    
    // Animações dos cards de estatísticas
    const statCards = document.querySelectorAll('.dashboard-stats .card');
    statCards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'all 0.5s ease';
            
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 100);
        }, index * 100);
    });
    
    // Efeitos hover nos botões de ação rápida
    const quickActionButtons = document.querySelectorAll('.quick-actions .btn');
    quickActionButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px) scale(1.02)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Atualização automática de estatísticas (opcional)
    if (window.enableAutoRefresh) {
        setInterval(updateDashboardStats, 30000); // Atualiza a cada 30 segundos
    }
});

// Função para atualizar estatísticas do dashboard
function updateDashboardStats() {
    fetch('/api/dashboard/stats')
        .then(response => response.json())
        .then(data => {
            // Atualizar contadores
            if (data.organization_count !== undefined) {
                updateCounter('organizationCount', data.organization_count);
            }
            if (data.user_count !== undefined) {
                updateCounter('userCount', data.user_count);
            }
            if (data.asset_count !== undefined) {
                updateCounter('assetCount', data.asset_count);
            }
            if (data.vulnerability_count !== undefined) {
                updateCounter('vulnerabilityCount', data.vulnerability_count);
            }
        })
        .catch(error => {
            console.error('Erro ao atualizar estatísticas:', error);
        });
}

// Função para animar contadores
function updateCounter(elementId, newValue) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const currentValue = parseInt(element.textContent) || 0;
    const increment = (newValue - currentValue) / 20;
    let current = currentValue;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= newValue) || (increment < 0 && current <= newValue)) {
            current = newValue;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current);
    }, 50);
}

// Função para mostrar notificações no dashboard
function showDashboardNotification(message, type = 'info') {
    const notificationDiv = document.createElement('div');
    notificationDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notificationDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notificationDiv.innerHTML = `
        <i class="bi bi-${type === 'error' ? 'exclamation-triangle' : type === 'success' ? 'check-circle' : 'info-circle'}"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notificationDiv);
    
    // Auto-remove após 5 segundos
    setTimeout(() => {
        if (notificationDiv.parentNode) {
            notificationDiv.remove();
        }
    }, 5000);
}

// Função para exportar dados do dashboard
function exportDashboardData() {
    const data = {
        organization_count: document.querySelector('[data-stat="organizations"]')?.textContent,
        user_count: document.querySelector('[data-stat="users"]')?.textContent,
        asset_count: document.querySelector('[data-stat="assets"]')?.textContent,
        vulnerability_count: document.querySelector('[data-stat="vulnerabilities"]')?.textContent,
        export_date: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `dashboard-export-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    window.URL.revokeObjectURL(url);
}

// Função para alternar modo escuro (opcional)
function toggleDarkMode() {
    const body = document.body;
    const isDark = body.classList.toggle('dark-mode');
    
    localStorage.setItem('darkMode', isDark);
    
    // Atualizar ícones e cores conforme necessário
    const icon = document.querySelector('#darkModeToggle i');
    if (icon) {
        icon.className = isDark ? 'bi bi-sun' : 'bi bi-moon';
    }
}

// Inicializar modo escuro se configurado
document.addEventListener('DOMContentLoaded', function() {
    const darkMode = localStorage.getItem('darkMode') === 'true';
    if (darkMode) {
        document.body.classList.add('dark-mode');
    }
}); 