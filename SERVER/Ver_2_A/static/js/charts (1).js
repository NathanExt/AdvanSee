// static/js/charts.js

function createPieChart(canvasId, labels, data, title) {
    const ctx = document.getElementById(canvasId);
    if (ctx) {
        new Chart(ctx.getContext('2d'), {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.7)', // Red
                        'rgba(54, 162, 235, 0.7)', // Blue
                        'rgba(255, 206, 86, 0.7)', // Yellow
                        'rgba(75, 192, 192, 0.7)', // Green
                        'rgba(153, 102, 255, 0.7)', // Purple
                        'rgba(255, 159, 64, 0.7)', // Orange
                        'rgba(192, 192, 192, 0.7)' // Gray
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)',
                        'rgba(192, 192, 192, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: title
                    },
                    legend: {
                        position: 'right', // Pode ser 'top', 'left', 'bottom', 'right'
                    }
                }
            }
        });
    }
}


// static/js/grafico.js
function criarGraficoPizza(idCanvas, labels, valores, cores) {
    new Chart(document.getElementById(idCanvas), {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: valores,
                 backgroundColor: [
                        'rgba(255, 99, 132, 0.6)',
                        'rgba(54, 162, 235, 0.6)',
                        'rgba(255, 206, 86, 0.6)',
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(153, 102, 255, 0.6)',
                        'rgba(255, 159, 64, 0.6)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom' },
                title: { display: true, text: 'Distribuição de Categorias' }
            }
        }
    });
}

// Executa após o DOM estar pronto
//document.addEventListener('DOMContentLoaded', function () {
//    criarGraficoPizza('graficoPizza',user_role_values,user_role_labels);
//})
//

fetch('/api/grafico')
  .then(response => response.json())
  .then(data => {
      criarGraficoPizza('graficoPizza', data.labels, data.values);
});;
