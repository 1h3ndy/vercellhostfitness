
document.addEventListener('DOMContentLoaded', fetchWeightLog);


document.getElementById('weightForm').addEventListener('submit', addWeight);


async function fetchWeightLog() {
    const response = await fetch('/api/get-weight-log'); //feth data for user from backend using fetch http request
    console.log(response); //logs to client console for debug, possibly remove as not to expose raw data. (DEBUGGING)
    if (response.ok) { // ok just checks all good status codes
        const data = await response.json();
        const dates = data.weight_log.map(entry => entry.date); // entry is just json entries, map converts to array/list
        const weights = data.weight_log.map(entry => entry.weight);

        renderChart(dates, weights); //render chart canvsas with user array returned from backend
        console.log(dates + weights);
    } else {
        console.error('error');
    }
}

async function addWeight(event) {
    event.preventDefault();
    const weight = document.getElementById('weight').value; //get weight from frotend container

    const response = await fetch('/api/add-weight', { //send post request to backend to add new weight
        //python backend can more easily handle getting current date, rather than having user input the date.
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ weight })
    });

    if (response.ok) {
        alert('Weight logged');
        fetchWeightLog();
    } else {
        console.error('Failed');
    }
}

function renderChart(dates, weights) {
    const ctx = document.getElementById('weightChart').getContext('2d'); //specifying we are using 2d canvas rather than webgl
    new Chart(ctx, {  //create chart class
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Weight (kg)',
                data: weights,
                borderColor: 'red', //set styles and info
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            responsive: true, //make responseive to mouse hovers to view info about points on the chartt, this was specififed as important in my design
            scales: {
                x: { title: { display: true, text: 'Date' } },
                y: { title: { display: true, text: 'Weight (kg)' } }
            }
        }
    });
}
