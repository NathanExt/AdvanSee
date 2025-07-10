// static/js/scripts.js
document.addEventListener('DOMContentLoaded', function() {
    // Gráfico de Assets por Status no Dashboard
    const assetsStatusCanvas = document.getElementById('assetsStatusChart');
    if (assetsStatusCanvas) {
        const labels = JSON.parse(assetsStatusCanvas.dataset.labels);
        const values = JSON.parse(assetsStatusCanvas.dataset.values);
        createPieChart('assetsStatusChart', labels, values, 'Assets by Status');
    }

    // Adicione chamadas para outros gráficos aqui, se houver na página index.html
});

