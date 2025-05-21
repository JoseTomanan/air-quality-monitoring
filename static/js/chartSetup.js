async function drawChart(canvas_id, metric) {
  console.log(`drawing ${metric} for device ${dev_id}`);
  
  const url = `/api/chart-data?device_id=${dev_id}&metric=${metric}`;
  console.log("Fetching:", url);
  
  const res = await fetch(`/api/chart-data?device_id=${dev_id}&metric=${metric}`);
  const chartData = await res.json();

  const ctx = document.getElementById(canvas_id).getContext("2d");

  new Chart(ctx, {
    type: "line",
    data: {
      labels: chartData.labels,
      datasets: [{
        label: chartData.label,
        data: chartData.data,
        borderColor: chartData.borderColor,
        fill: false
      }],
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

window.addEventListener("DOMContentLoaded", () => {
  drawChart("dataChart_gas_conc", "gas");
  drawChart("dataChart_pm1_0", "pm1");
  drawChart("dataChart_pm2_5", "pm2.5");
  drawChart("dataChart_pm10_0", "pm10");
});
