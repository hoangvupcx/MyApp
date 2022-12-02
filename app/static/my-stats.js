function cateChart(labels, data) {
    const ctx = document.getElementById('cateStats');

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        label: '# of Votes',
        data: data,
        borderWidth: 1,
        backgroundColor: ['red', 'blue', 'yellow', 'orange', 'brown', 'purple']
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

function revenueChart(labels, data) {
    const ctx = document.getElementById('revenueStats');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Revenue',
        data: data,
        borderWidth: 1,
        backgroundColor: ['red', 'blue', 'yellow', 'orange', 'brown', 'purple']
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}
