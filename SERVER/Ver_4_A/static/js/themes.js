/**
 * Sistema de Temas para Ambiente ISAC
 * Gerencia a aplicação de temas dinamicamente
 */

class ThemeManager {
    constructor() {
        this.currentTheme = this.getStoredTheme() || 'light';
        this.init();
    }

    /**
     * Inicializa o gerenciador de temas
     */
    init() {
        this.applyTheme(this.currentTheme);
        this.setupThemeListener();
    }

    /**
     * Obtém o tema armazenado na sessão
     */
    getStoredTheme() {
        // Tentar obter da sessão do servidor via AJAX
        return sessionStorage.getItem('user_theme') || 'light';
    }

    /**
     * Armazena o tema na sessão
     */
    storeTheme(theme) {
        sessionStorage.setItem('user_theme', theme);
    }

    /**
     * Aplica um tema ao documento
     */
    applyTheme(theme) {
        // Remover classes de tema anteriores
        document.body.classList.remove('theme-light', 'theme-dark', 'theme-blue', 'theme-green', 'theme-auto');
        
        // Aplicar novo tema
        if (theme === 'auto') {
            this.applyAutoTheme();
        } else {
            document.body.classList.add(`theme-${theme}`);
        }
        
        // Armazenar tema
        this.storeTheme(theme);
        this.currentTheme = theme;
        
        // Disparar evento de mudança de tema
        this.dispatchThemeChangeEvent(theme);
    }

    /**
     * Aplica tema automático baseado na preferência do sistema
     */
    applyAutoTheme() {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const autoTheme = prefersDark ? 'dark' : 'light';
        
        document.body.classList.add(`theme-${autoTheme}`);
        this.currentTheme = autoTheme;
    }

    /**
     * Configura listener para mudanças de preferência do sistema
     */
    setupThemeListener() {
        // Listener para mudanças de preferência do sistema
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (this.currentTheme === 'auto') {
                this.applyAutoTheme();
            }
        });
    }

    /**
     * Dispara evento de mudança de tema
     */
    dispatchThemeChangeEvent(theme) {
        const event = new CustomEvent('themeChanged', {
            detail: { theme: theme }
        });
        document.dispatchEvent(event);
    }

    /**
     * Obtém o tema atual
     */
    getCurrentTheme() {
        return this.currentTheme;
    }

    /**
     * Verifica se o tema atual é escuro
     */
    isDarkTheme() {
        return this.currentTheme === 'dark' || 
               (this.currentTheme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches);
    }

    /**
     * Alterna entre tema claro e escuro
     */
    toggleTheme() {
        const newTheme = this.isDarkTheme() ? 'light' : 'dark';
        this.applyTheme(newTheme);
        return newTheme;
    }
}

/**
 * Função para aplicar tema baseado na configuração do usuário
 */
function applyUserTheme(theme) {
    if (window.themeManager) {
        window.themeManager.applyTheme(theme);
    } else {
        // Fallback se o ThemeManager não estiver disponível
        document.body.classList.remove('theme-light', 'theme-dark', 'theme-blue', 'theme-green', 'theme-auto');
        document.body.classList.add(`theme-${theme}`);
    }
}

/**
 * Função para obter configurações do usuário
 */
function getUserConfig() {
    return fetch('/config/get-config')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                return data.config;
            }
            return null;
        })
        .catch(error => {
            console.error('Erro ao obter configurações:', error);
            return null;
        });
}

/**
 * Função para aplicar configurações do usuário
 */
function applyUserConfig() {
    getUserConfig().then(config => {
        if (config && config.theme) {
            applyUserTheme(config.theme);
        }
    });
}

/**
 * Função para salvar configuração de tema
 */
function saveThemeConfig(theme) {
    return fetch('/config/save', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ theme: theme })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            applyUserTheme(theme);
            return true;
        }
        return false;
    })
    .catch(error => {
        console.error('Erro ao salvar tema:', error);
        return false;
    });
}

/**
 * Função para preview de tema
 */
function previewTheme(theme) {
    // Aplicar tema temporariamente
    const originalTheme = window.themeManager ? window.themeManager.getCurrentTheme() : 'light';
    
    applyUserTheme(theme);
    
    // Restaurar tema original após 3 segundos
    setTimeout(() => {
        applyUserTheme(originalTheme);
    }, 3000);
}

/**
 * Inicialização quando o DOM estiver pronto
 */
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar gerenciador de temas
    window.themeManager = new ThemeManager();
    
    // Aplicar configurações do usuário se disponíveis
    applyUserConfig();
    
    // Listener para mudanças de tema
    document.addEventListener('themeChanged', function(e) {
        console.log('Tema alterado para:', e.detail.theme);
        
        // Atualizar ícones e elementos específicos se necessário
        updateThemeSpecificElements(e.detail.theme);
    });
});

/**
 * Atualiza elementos específicos baseado no tema
 */
function updateThemeSpecificElements(theme) {
    // Atualizar favicon se necessário
    const favicon = document.querySelector('link[rel="icon"]');
    if (favicon) {
        const isDark = theme === 'dark' || 
                      (theme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches);
        
        favicon.href = isDark ? '/static/images/favicon-dark.ico' : '/static/images/favicon-light.ico';
    }
    
    // Atualizar meta theme-color
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (metaThemeColor) {
        const isDark = theme === 'dark' || 
                      (theme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches);
        
        metaThemeColor.content = isDark ? '#1a1a1a' : '#667eea';
    }
}

/**
 * Função para alternar tema rapidamente (atalho de teclado)
 */
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + T para alternar tema
    if ((e.ctrlKey || e.metaKey) && e.key === 't') {
        e.preventDefault();
        if (window.themeManager) {
            const newTheme = window.themeManager.toggleTheme();
            console.log('Tema alternado para:', newTheme);
        }
    }
});

// Exportar funções para uso global
window.applyUserTheme = applyUserTheme;
window.saveThemeConfig = saveThemeConfig;
window.previewTheme = previewTheme;
window.getUserConfig = getUserConfig; 