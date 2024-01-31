// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

$(document).ready(function() {
        // 폼 제출 이벤트를 처리합니다.
        $('#packetSimulateForm').on('submit', function(e) {
            e.preventDefault(); // 기본 제출 동작 방지
            
            var serializedArray = $(this).serializeArray();
            console.log(serializedArray); // 콘솔에 serializedArray 출력

            var dataObject = {};

            $.each(serializedArray, function(index, item) {
                dataObject[item.name] = item.value;
            });

            console.log(dataObject); // 콘솔에 dataObject 출력

           
            // AJAX 요청 설정
            $.ajax({
                url: './packet_simulate', // 요청 URL
                type: 'post', // HTTP 메소드
                contentType: 'application/json',
                dataType: 'json', // 응답 데이터 타입
                data: JSON.stringify(dataObject), // 폼 데이터 직렬화
                success: function(data) {
                    // AJAX 요청 성공 시 그래프 그리기
                    drawGraph(data);
                    // 기존 버튼 컨테이너 비우기
                    var $btnContainer = $('#MatchLinkButton').empty();

                    // 'Matched Info' 버튼 생성 및 클릭 이벤트 핸들링
                    $('<button/>', {
                        text: 'Matched Info',
                        id: 'matchedInfoBtn'
                    }).click(function() {
                        fetchAndSendData(data.original_values[0], './matched');
                    }).appendTo($btnContainer);

                    // 'Un-Matched Info' 버튼 생성 및 클릭 이벤트 핸들링
                    $('<button/>', {
                        text: 'Un-Matched Info',
                        id: 'unmatchedInfoBtn'
                    }).click(function() {
                        fetchAndSendData(data.original_values[1], './unmatched');
                    }).appendTo($btnContainer);
                    
                    
                    // 생성한 버튼을 원하는 위치에 추가
                    $('#MatchLinkButton').append($btnContainer);
                },
                error: function(xhr, status, error) {
                    // 에러 처리
                    alert("에러 발생: " + error);
                }
            });
        });
    });
    
    function fetchAndSendData(originalValues, url) {
        $.ajax({
            url: url,
            type: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({ original_values: originalValues }),
            success: function(response) {
                sendToMatchTable(response);
                console.log(response)
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error(textStatus, errorThrown);
            }
        });
    }

    function sendToMatchTable(data) {
        $.ajax({
            url: '/match_table',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response) {
                // 성공 처리 로직
                document.open();
                document.write(response);
                document.close();
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error(textStatus, errorThrown);
            }
        });
    }

    function drawGraph(data) {
        var ctx = document.getElementById("MatchingBarChart").getContext('2d');

        // 기존에 그래프가 있다면 삭제합니다.
        if (window.myLineChart) {
            window.myLineChart.destroy();
        }

        // 새로운 그래프 생성
        window.myLineChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels, // X축 레이블
                datasets: [{
                    label: "Revenue",
                    backgroundColor: "rgba(2,117,216,1)",
                    borderColor: "rgba(2,117,216,1)",
                    data: data.values, // Y축 데이터
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
                            max: Math.max(...data.values) + 3,
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
}