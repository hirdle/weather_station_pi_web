const urlPattern = "http://127.0.0.1:5000"

const getDataAPI = (url, callback) => {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.responseType = 'json';
    xhr.send();
    
    xhr.onload = function() {
        let responseObj = xhr.response;
        // callback(JSON.parse(responseObj))
        callback(responseObj)
    };
}

const selectDays = document.querySelector("#selectDays")
const forecastInfo = document.querySelector("#forecastInfo")

let selectDaysForecast = 1


let lineChart = undefined

const addNowData = () => {
    getDataAPI(`${urlPattern}/now`, (data) => {
        console.log(typeof data)
        console.log(Object.keys(data).length)
        if (Object.keys(data).length != 0) {
            document.querySelector("#temp").innerHTML = `${data.tempStreet}°C | ${data.tempRoom}°C`
            document.querySelector("#realTemp").innerHTML = data.tempStreetReal
            document.querySelector("#humidity").innerHTML = `${data.humidity_room}% | ${data.humidity_street}%`
            document.querySelector("#alt").innerHTML = data.alt
            document.querySelector("#pressure").innerHTML = data.pressure
        }
        
    })
}

const getAddData = () => {

    if (lineChart != undefined)
        lineChart.destroy()

    

    getDataAPI(`${urlPattern}/forecast/${selectDaysForecast}`, (data) => {
        forecastInfo.innerHTML = data.map(item => 
            `
            <div class="col">
                <div class="card mb-4 rounded-3 shadow-sm">
                <div class="card-header py-3">
                    <h4 class="my-0 fw-normal">${item[0]}</h4>
                </div>
                <div class="card-body">
                    <!-- <h1 class="card-title pricing-card-title">$0<small class="text-muted fw-light">/mo</small></h1> -->
                    <ul class="list-unstyled mt-3 mb-4">
                        ${item.slice(1).map(item_forecast => (
                            `<li>${item_forecast}</li>`
                        )).join('')}
                    </ul>
                </div>
                </div>
            </div>`
        ).join('')
    })
    
    getDataAPI(`${urlPattern}/forecast_chart/${selectDaysForecast}`, (data) => {
        let tempChart = document.getElementById("tempChart");
    
        let tempData = {
        labels: data[0],
        datasets: [{
            label: "Температура (°C)",
            data: data[1],
        }]
        };
    
        let chartOptions = {
        legend: {
            display: true,
            position: 'top',
            labels: {
                boxWidth: 80,
                fontColor: 'black',
            }
        }
        };
    
        lineChart = new Chart(tempChart, {
            type: 'line',
            data: tempData,
            options: chartOptions
        });
    })    
}

getAddData()

selectDays.oninput = () => {
    selectDaysForecast = selectDays.value
    getAddData()
}

setInterval(
    () => {
        getAddData()
    }, 20000
)

setInterval(
    () => {
        addNowData()
    }, 1000
)
