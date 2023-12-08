

	function updateHumidity(temperature) {
      const dial = document.getElementById('humidityDial');
      const hand = document.getElementById('humidityHand');

      const dialAngle = (temperature / 100) * 180; // Assuming temperature ranges from 0 to 100
      const handAngle = dialAngle - 90; // Offset the hand by 90 degrees

      dial.style.transform = `translateX(-50%) rotate(${dialAngle}deg)`;
      hand.style.transform = `translateX(-50%) rotate(${handAngle}deg)`;
    }

	function updateDial(temperature) {
      const dial = document.getElementById('temperatureDial');
      const hand = document.getElementById('temperatureHand');

      const dialAngle = (temperature / 100) * 180; // Assuming temperature ranges from 0 to 100
      const handAngle = dialAngle - 90; // Offset the hand by 90 degrees

      dial.style.transform = `translateX(-50%) rotate(${dialAngle}deg)`;
      hand.style.transform = `translateX(-50%) rotate(${handAngle}deg)`;
    }
    // You can use JavaScript to update the values dynamically

    // Simulating fetching data (replace with actual API calls)
    function fetchData() {
        // Simulated data
        const temperature = 28; // Replace with actual temperature data
        const humidity = 60; // Replace with actual humidity data

        // Update the HTML elements with the fetched data
        document.getElementById("temperatureValue").innerText = temperature + "°C";
        document.getElementById("humidityValue").innerText = humidity + "%";


        // Set up the clock
        updateClock();
        setInterval(updateClock, 1000); // Update every second
        updateDial(temperature);
        updateHumidity(humidity);

        const xValues = [50,60,70,80,90,100,110,120,130,140,150];
        const yValues = [7,8,8,9,9,9,10,11,14,14,15];

        new Chart("myChart", {
        type: "line",
        data: {
            labels: xValues,
            datasets: [{
            fill: false,
            lineTension: 0,
            backgroundColor: "rgba(0,0,255,1.0)",
            borderColor: "rgba(0,0,255,0.1)",
            data: yValues
            }]
        },
        options: {
            legend: {display: false},
            scales: {
            yAxes: [{ticks: {min: 6, max:16}}],
            }
        }
        });

    }

    function updateIndicator(indicatorId, value, minValue, maxValue, lowColor, highColor) {
        const percentage = (value - minValue) / (maxValue - minValue) * 100;
        const indicator = document.getElementById(indicatorId);

        // Set the background color based on the percentage
        const color = gradientColor(lowColor, highColor, percentage / 100);
        indicator.style.backgroundColor = color;
    }

    function updateClock() {
        const currentTime = new Date();
        const hours = currentTime.getHours();
        const minutes = currentTime.getMinutes();
        const seconds = currentTime.getSeconds();

        // Update the clock hands rotation angles
        const hourHand = document.getElementById('hourHand');
        const minuteHand = document.getElementById('minuteHand');
        const secondHand = document.getElementById('secondHand');

        // Calculate the initial rotation angles based on the current time
         initialHourRotation = (360 / 12) * (hours % 12) + (360 / 12) * (minutes / 60)-90;
         initialMinuteRotation = (360 / 60) * minutes + (360 / 60) * (seconds / 60)-90;
         initialSecondRotation = (360 / 60) * seconds;

        hourHand.style.transform = `rotate(${initialHourRotation}deg)`;
        minuteHand.style.transform = `rotate(${initialMinuteRotation}deg)`;
        secondHand.style.transform = `rotate(${initialSecondRotation}deg)`;

        // Display the formatted time
        const formattedTime = `${padZero(hours)}:${padZero(minutes)}:${padZero(seconds)}`;
        document.getElementById("timeValue").innerText = formattedTime;

        // Update clock numbers
        updateClockNumbers();
    }

    function padZero(num) {
        return (num < 10 ? '0' : '') + num;
    }

    function gradientColor(startColor, endColor, percentage) {
        const startRGB = hexToRgb(startColor);
        const endRGB = hexToRgb(endColor);

        const resultRed = startRGB.red + Math.round((endRGB.red - startRGB.red) * percentage);
        const resultGreen = startRGB.green + Math.round((endRGB.green - startRGB.green) * percentage);
        const resultBlue = startRGB.blue + Math.round((endRGB.blue - startRGB.blue) * percentage);

        return rgbToHex(resultRed, resultGreen, resultBlue);
    }

    function hexToRgb(hex) {
        const bigint = parseInt(hex.slice(1), 16);
        const red = (bigint >> 16) & 255;
        const green = (bigint >> 8) & 255;
        const blue = bigint & 255;
        return { red, green, blue };
    }

    function rgbToHex(red, green, blue) {
        return `#${(1 << 24 | red << 16 | green << 8 | blue).toString(16).slice(1)}`;
    }

    function updateClockNumbers() {
        const clockNumbers = document.querySelector('.clock-numbers');
        const radius = clockNumbers.offsetWidth / 2;

        // Remove existing numbers
        clockNumbers.innerHTML = '';

        for (let i = 1; i <= 12; i++) {
            const number = document.createElement('div');
            const angle = (i - 3) * 30; // Start from 12 o'clock position
            const x = radius * Math.cos(degreesToRadians(angle));
            const y = radius * Math.sin(degreesToRadians(angle));

            number.className = 'number';
            number.style.transform = `translate(${x}px, ${y}px)`;
            number.innerText = i;

            clockNumbers.appendChild(number);
        }
    }

    function degreesToRadians(degrees) {
        return degrees * (Math.PI / 180);
    }


    // Call fetchData function when the page loads
    window.onload = fetchData;
