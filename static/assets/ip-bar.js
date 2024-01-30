// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

fetch('/api/log')
    .then(response => response.json())
    .then(data => {
        var ctx = document.getElementById("IpBarChart");
        var myLineChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.ip.labels, // 백엔드에서 전송된 레이블 사용
                datasets: [{
                    label: "Revenue",
                    backgroundColor: "rgba(2,117,216,1)",
                    borderColor: "rgba(2,117,216,1)",
                    data: data.ip.values, // 백엔드에서 전송된 값 사용
                }],
            },
              options: {
                scales: {
                  xAxes: [{
                    time: {
                      unit: 'month'
                    },
                    gridLines: {
                      display: false
                    },
                    ticks: {
                      maxTicksLimit: 6
                    }
                  }],
                  yAxes: [{
                    ticks: {
                      min: 0,
                      max: Math.max(...data.ip.values) + 10, 
                      maxTicksLimit: 5
                    },
                    gridLines: {
                      display: true
                    }
                  }],
                },
                legend: {
                  display: false
                }
              }
            });
          })
          .catch(error => {
              console.error("Error loading chart data:", error);
          });