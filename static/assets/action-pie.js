// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

fetch('/api/log')
    .then(response => response.json())
    .then(data => {
        var ctx = document.getElementById("ActionPieChart");
        var myPieChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: data.action.labels, // 백엔드에서 가져온 레이블
                datasets: [{
                    data: data.action.values, // 백엔드에서 가져온 데이터
                    backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745'], // 색상 설정
                }],
            },
        });
    })
    .catch(error => {
        console.error("Error loading pie chart data:", error);
    });
