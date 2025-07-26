// Asset Detail JavaScript - Ambiente ISAC

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tab functionality
    initializeTabs();
    
    // Initialize status indicators
    initializeStatusIndicators();
    
    // Initialize action buttons
    initializeActionButtons();
    
    // Initialize health monitoring
    initializeHealthMonitoring();
    
    // Initialize animations
    initializeAnimations();
});

// Tab functionality
function initializeTabs() {
    const tabButtons = document.querySelectorAll('[data-bs-toggle="tab"]');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Remove active class from all tabs
            tabButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked tab
            this.classList.add('active');
            
            // Show corresponding content
            const target = this.getAttribute('data-bs-target');
            const targetPane = document.querySelector(target);
            
            if (targetPane) {
                // Hide all tab panes
                document.querySelectorAll('.tab-pane').forEach(pane => {
                    pane.classList.remove('show', 'active');
                });
                
                // Show target pane
                targetPane.classList.add('show', 'active');
                
                // Add fade-in animation
                targetPane.classList.add('fade-in');
                setTimeout(() => {
                    targetPane.classList.remove('fade-in');
                }, 500);
            }
        });
    });
}

// Status indicators
function initializeStatusIndicators() {
    // Update connectivity status
    updateConnectivityStatus();
    
    // Update antivirus status
    updateAntivirusStatus();
    
    // Update firewall status
    updateFirewallStatus();
    
    // Update health status
    updateHealthStatus();
}

// Connectivity status
function updateConnectivityStatus() {
    const connectivityCard = document.querySelector('.card.border-danger');
    if (!connectivityCard) return;
    
    // Simulate real-time connectivity check
    setInterval(() => {
        // This would normally make an API call to check connectivity
        const isConnected = Math.random() > 0.5; // Simulate connection status
        
        if (isConnected) {
            connectivityCard.classList.remove('border-danger');
            connectivityCard.classList.add('border-success');
            
            const icon = connectivityCard.querySelector('.bi-wifi-off');
            if (icon) {
                icon.classList.remove('bi-wifi-off', 'text-danger');
                icon.classList.add('bi-wifi', 'text-success');
            }
            
            const title = connectivityCard.querySelector('h6');
            if (title) {
                title.textContent = 'A conectividade está Conectada';
                title.classList.remove('text-danger');
                title.classList.add('text-success');
            }
        }
    }, 30000); // Check every 30 seconds
}

// Antivirus status
function updateAntivirusStatus() {
    const antivirusCard = document.querySelector('.card.border-danger:nth-child(2)');
    if (!antivirusCard) return;
    
    // Simulate antivirus detection
    setTimeout(() => {
        const isDetected = Math.random() > 0.7; // 30% chance of detection
        
        if (isDetected) {
            antivirusCard.classList.remove('border-danger');
            antivirusCard.classList.add('border-success');
            
            const icon = antivirusCard.querySelector('.bi-bug');
            if (icon) {
                icon.classList.remove('text-danger');
                icon.classList.add('text-success');
            }
            
            const title = antivirusCard.querySelector('h6');
            if (title) {
                title.textContent = 'O antivírus foi detectado';
                title.classList.remove('text-danger');
                title.classList.add('text-success');
            }
        }
    }, 15000); // Check after 15 seconds
}

// Firewall status
function updateFirewallStatus() {
    const firewallCard = document.querySelector('.card.border-danger:nth-child(3)');
    if (!firewallCard) return;
    
    // Simulate firewall activation
    setTimeout(() => {
        const isActive = Math.random() > 0.6; // 40% chance of activation
        
        if (isActive) {
            firewallCard.classList.remove('border-danger');
            firewallCard.classList.add('border-success');
            
            const icon = firewallCard.querySelector('.bi-fire');
            if (icon) {
                icon.classList.remove('text-danger');
                icon.classList.add('text-success');
            }
            
            const title = firewallCard.querySelector('h6');
            if (title) {
                title.textContent = 'Firewall está Ativado';
                title.classList.remove('text-danger');
                title.classList.add('text-success');
            }
        }
    }, 20000); // Check after 20 seconds
}

// Health status
function updateHealthStatus() {
    const healthCard = document.querySelector('.card.border-danger:nth-child(4)');
    if (!healthCard) return;
    
    // Simulate health improvement
    setTimeout(() => {
        const healthScore = Math.random();
        
        if (healthScore > 0.8) {
            healthCard.classList.remove('border-danger');
            healthCard.classList.add('border-success');
            
            const title = healthCard.querySelector('h6');
            if (title) {
                title.textContent = 'Estado de saúde: Excelente';
                title.classList.remove('text-danger');
                title.classList.add('text-success');
            }
        } else if (healthScore > 0.5) {
            healthCard.classList.remove('border-danger');
            healthCard.classList.add('border-warning');
            
            const title = healthCard.querySelector('h6');
            if (title) {
                title.textContent = 'Estado de saúde: Bom';
                title.classList.remove('text-danger');
                title.classList.add('text-warning');
            }
        }
    }, 25000); // Check after 25 seconds
}

// Action buttons
function initializeActionButtons() {
    // Edit button
    const editButton = document.querySelector('.btn-outline-info');
    if (editButton) {
        editButton.addEventListener('click', function() {
            showEditModal();
        });
    }
    
    // Download button
    const downloadButton = document.querySelector('.btn-outline-primary');
    if (downloadButton) {
        downloadButton.addEventListener('click', function() {
            showDownloadModal();
        });
    }
    
    // Flag button
    const flagButton = document.querySelector('.btn-outline-warning');
    if (flagButton) {
        flagButton.addEventListener('click', function() {
            showFlagModal();
        });
    }
    
    // Settings button
    const settingsButton = document.querySelector('.btn-outline-secondary');
    if (settingsButton) {
        settingsButton.addEventListener('click', function() {
            showSettingsModal();
        });
    }
}

// Health monitoring
function initializeHealthMonitoring() {
    // Monitor system resources
    setInterval(() => {
        updateSystemResources();
    }, 10000); // Update every 10 seconds
    
    // Monitor software updates
    setInterval(() => {
        checkSoftwareUpdates();
    }, 60000); // Check every minute
}

// System resources
function updateSystemResources() {
    // This would normally fetch real data from the asset
    const cpuUsage = Math.floor(Math.random() * 100);
    const memoryUsage = Math.floor(Math.random() * 100);
    const diskUsage = Math.floor(Math.random() * 100);
    
    // Update resource indicators
    updateResourceIndicator('cpu', cpuUsage);
    updateResourceIndicator('memory', memoryUsage);
    updateResourceIndicator('disk', diskUsage);
}

// Resource indicator
function updateResourceIndicator(type, usage) {
    const indicator = document.querySelector(`[data-resource="${type}"]`);
    if (!indicator) return;
    
    indicator.style.width = `${usage}%`;
    indicator.setAttribute('aria-valuenow', usage);
    
    // Update color based on usage
    if (usage > 80) {
        indicator.classList.remove('bg-success', 'bg-warning');
        indicator.classList.add('bg-danger');
    } else if (usage > 60) {
        indicator.classList.remove('bg-success', 'bg-danger');
        indicator.classList.add('bg-warning');
    } else {
        indicator.classList.remove('bg-warning', 'bg-danger');
        indicator.classList.add('bg-success');
    }
}

// Software updates
function checkSoftwareUpdates() {
    // This would normally check for available updates
    const hasUpdates = Math.random() > 0.8; // 20% chance of updates
    
    if (hasUpdates) {
        showUpdateNotification();
    }
}

// Update notification
function showUpdateNotification() {
    const notification = document.createElement('div');
    notification.className = 'alert alert-info alert-dismissible fade show position-fixed';
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        <i class="bi bi-download"></i>
        <strong>Atualizações disponíveis</strong>
        <p class="mb-0">Há novas atualizações de software disponíveis para este ativo.</p>
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 10 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 10000);
}

// Animations
function initializeAnimations() {
    // Animate cards on load
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in');
            setTimeout(() => {
                card.classList.remove('fade-in');
            }, 500);
        }, index * 100);
    });
    
    // Animate status indicators
    const statusCards = document.querySelectorAll('.card.border-danger');
    statusCards.forEach((card, index) => {
        setTimeout(() => {
            card.style.transform = 'scale(1.02)';
            setTimeout(() => {
                card.style.transform = 'scale(1)';
            }, 200);
        }, index * 200);
    });
}

// Modal functions
function showEditModal() {
    // Create and show edit modal
    const modal = new bootstrap.Modal(document.getElementById('editAssetModal'));
    modal.show();
}

function showDownloadModal() {
    // Create and show download modal
    const modal = new bootstrap.Modal(document.getElementById('installMsiModal'));
    modal.show();
}

function showFlagModal() {
    // Create and show flag modal
    const modal = new bootstrap.Modal(document.getElementById('flagAssetModal'));
    modal.show();
}

function showSettingsModal() {
    // Create and show settings modal
    const modal = new bootstrap.Modal(document.getElementById('settingsModal'));
    modal.show();
}

// Utility functions
function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatUptime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours}h ${minutes}m ${secs}s`;
}

function getStatusColor(status) {
    switch (status.toLowerCase()) {
        case 'active':
            return 'success';
        case 'inactive':
            return 'warning';
        case 'offline':
            return 'danger';
        default:
            return 'secondary';
    }
}

// Export functions
function exportAssetData() {
    const assetData = {
        id: document.querySelector('[data-asset-id]')?.getAttribute('data-asset-id'),
        name: document.querySelector('.asset-header h2')?.textContent,
        status: document.querySelector('.btn-outline-secondary')?.textContent,
        export_date: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(assetData, null, 2)], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `asset-${assetData.id}-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    window.URL.revokeObjectURL(url);
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Asset Detail page initialized');
}); 