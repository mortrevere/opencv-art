var config = {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'FPS',
            backgroundColor: "#00FF00",
            borderColor: "#00FF00",
            data: [

            ],
            fill: false,
        },
        {
            label: 'CAPFPS',
            backgroundColor: "#FF0000",
            borderColor: "#FF0000",
            data: [

            ],
            fill: false,
        },
        {
            label: 'IN QUEUE',
            backgroundColor: "#FF0000",
            borderColor: "#FF0000",
            data: [

            ],
            fill: false,
        },
        {
            label: 'OUTQUEUE',
            backgroundColor: "#FF0000",
            borderColor: "#FF0000",
            data: [

            ],
            fill: false,
        }]
    },
    options: {
        responsive: true,
        title: {
            display: true,
            text: 'FPS'
        },
        tooltips: {
            mode: 'index',
            intersect: false,
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Last minute'
                }
            }],
            yAxes: [{
                display: true,
                ticks: {
                    beginAtZero: true,
                    maxTicksLimit: 32,
                    suggestedMax: 32
                },
                scaleLabel: {
                    display: false,
                    labelString: 'Value'
                }
            }]
        }
    }
};


function connect() {
    var ws = new WebSocket('ws://192.168.0.22:8765');
    ws.onopen = function () {
        // subscribe to some channels
        console.log("Connected !")
    };

    ws.onmessage = function (e) {
        console.log('Message:', e.data);

        var chunks = e.data.split(":")

        if (chunks[1] == "fps") {
            config.data.labels.push('')
            config.data.datasets[0].data.push(chunks[2])
        }

        if (chunks[1] == "capfps") {
            //config.data.labels.push('')
            config.data.datasets[1].data.push(chunks[2])
        }

        if (chunks[1] == "inq") {
            //config.data.labels.push('')
            config.data.datasets[2].data.push(chunks[2])
        }
        if (chunks[1] == "outq") {
            //config.data.labels.push('')
            config.data.datasets[3].data.push(chunks[2])
        }

        if (config.data.labels.length >= 60) {
            config.data.labels.shift()
            config.data.datasets[0].data.shift()
            config.data.datasets[1].data.shift()
        }
        window.myLine.update();
    };

    ws.onclose = function (e) {
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
        setTimeout(connect, 1000);
    };

    ws.onerror = function (err) {
        console.error('Socket encountered error: ', err.message, 'Closing socket');
        ws.close();
        //setTimeout(connect, 2000);
    };
}


window.onload = function () {
    var ctx = document.getElementById('canvas').getContext('2d');
    window.myLine = new Chart(ctx, config);
    connect();
};