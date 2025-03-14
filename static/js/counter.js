
  function countercolor(days) {
    const clampedDays = Math.min(days, 5);
    const ratio = clampedDays / 5;
    const red = Math.floor(255 * (1 - ratio));
    const green = Math.floor(255 * ratio);
    return `rgb(${red}, ${green}, 0)`;
  }

document.addEventListener('DOMContentLoaded', fetchweeklycount());
async function fetchweeklycount() {
  fetch('/api/get-weekly-count')
    .then(response => response.json())

    .then(data => {
      console.log("weeklyworkout data: "+data.weekly_count)
      const count = data.weekly_count;
      // const count = 0; test purposes
      const counterEl = document.getElementById('gym-days-counter');
      const entirecounterelement = document.getElementById('gym-counter');
      counterEl.innerText = count;
      entirecounterelement.style.color = countercolor(count);
    })

  }