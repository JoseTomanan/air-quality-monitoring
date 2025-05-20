async function drawChart() {

  const res = await fetch(`/api/chart-data?device_id=${dev_id}`);

  const chartData = await res.json();

  const ctx = document.getElementById("dataChart").getContext("2d");

  new Chart(ctx, {
    type: "line",
    data: {
      labels: chartData.labels,
      datasets: chartData.datasets,
    },
    options: {
      responsive: false,
      maintainAspectRatio: false,
      scales: {
        x: {
          ticks: { minRotation: 90, maxRotation: 90 },
        },
      },
    },
  });
}

window.addEventListener("DOMContentLoaded", drawChart);