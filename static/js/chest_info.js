document.addEventListener("DOMContentLoaded", function () {
    const caseCode = encodeURIComponent(document.querySelector("h1.h2").dataset.caseCode);
    let chart;
    let data = [];

    fetch(`/get_price_history/${caseCode}`)
        .then(response => response.json())
        .then(fetchedData => {
            data = fetchedData;
            updateChart("Weekly");
        })
        .catch(error => console.error("Błąd ładowania danych:", error));

    function updateChart(range) {
        let rangeMap = {
            "Weekly": 7,
            "Monthly": 30,
            "Yearly": 365,
            "Total": data.length
        };

        let days = rangeMap[range] || 7;

        const labels = data.slice(-days).map(entry => entry[0]);
        const prices = data.slice(-days).map(entry => entry[1]);

        if (chart) {
            chart.destroy();
        }

        const ctx = document.getElementById("myChart").getContext("2d");
        chart = new Chart(ctx, {
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: "Cena skrzyni",
                    data: prices,
                    borderColor: "rgb(75, 192, 192)",
                    backgroundColor: "rgba(75, 192, 192, 0.2)"
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: "Data",
                            color: "#FFFFFF"
                        },
                        ticks: {
                            color: "#FFFFFF"
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: "Cena (PLN)",
                            color: "#FFFFFF"
                        },
                        ticks: {
                            color: "#FFFFFF"
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: "#FFFFFF"
                        }
                    }
                }
            }
        });

        updateTable(range);
    }

    function updateTable(range) {
        const tableBody = document.getElementById("priceTableBody");
        tableBody.innerHTML = "";
        let filteredData = [];

        if (range === "Yearly") {
            filteredData = getYearlyData();
        }
        else if (range === "Total") {
            filteredData = getTotalData();
        }
        else {
            const days = {
                "Weekly": 7,
                "Monthly": 30
            }[range] || data.length;
            filteredData = data.slice(-days);
        }

        let previousPrice = null;

        const rows = [];

        filteredData.forEach(entry => {
            const row = document.createElement("tr");
            const dateCell = document.createElement("td");
            const priceCell = document.createElement("td");
            const changeCell = document.createElement("td");

            dateCell.textContent = entry[0];
            priceCell.textContent = entry[1];

            if (previousPrice !== null) {
                const change = ((entry[1] - previousPrice) / previousPrice) * 100;
                changeCell.textContent = change.toFixed(2) + "%";
                changeCell.style.color = change >= 0 ? "green" : "red";
            } else {
                changeCell.textContent = "—";
            }

            previousPrice = entry[1];

            row.appendChild(dateCell);
            row.appendChild(priceCell);
            row.appendChild(changeCell);

            rows.push(row);
        });
        rows.reverse().forEach(row => tableBody.appendChild(row));
    }

    function getYearlyData() {
        const monthlyData = {};
        const today = new Date();
        const currentDateString = today.toDateString();
        const currentDay = parseInt(currentDateString.split(' ')[2]);
        const targetDay = currentDay;
        const currentYear = today.getFullYear();
        const currentMonth = today.getMonth();


        data.forEach(entry => {
            const dateStr = entry[0];
            const date = new Date(dateStr);
            if (isNaN(date)) return;

            const year = date.getFullYear();
            const month = date.getMonth();
            const day = date.getDate();
            const key = `${year}-${month}`;

            if (year > currentYear || (year === currentYear && month > currentMonth)) {
                return;
            }

            if (!monthlyData[key]) {
                monthlyData[key] = {
                    date: dateStr,
                    price: entry[1],
                    day: day,
                    distance: Math.abs(day - targetDay)
                };
                return;
            }

            const currentDistance = Math.abs(day - targetDay);
            if (currentDistance < monthlyData[key].distance) {
                monthlyData[key] = {
                    date: dateStr,
                    price: entry[1],
                    day: day,
                    distance: currentDistance
                };
            }
        });

        const result = Object.values(monthlyData)
            .sort((a, b) => new Date(a.date) - new Date(b.date))
            .map(item => [item.date, item.price]);

        return result.slice(-12);
    }

    function getTotalData() {
        const yearlyData = {};
        data.forEach(entry => {
            const dateStr = entry[0];
            const date = new Date(dateStr);
            if (isNaN(date)) return;

            const year = date.getFullYear();
            if (!yearlyData[year]) {
                yearlyData[year] = [dateStr, entry[1]];
            }
        });

        return Object.values(yearlyData);
    }

    document.querySelectorAll(".dropdown-item").forEach(item => {
        item.addEventListener("click", function (event) {
            event.preventDefault();
            let selectedRange = this.textContent.trim();

            let timeButton = document.getElementById("time");
            let iconHTML = timeButton.querySelector("svg").outerHTML;
            timeButton.innerHTML = `${iconHTML} ${selectedRange}`;
            updateChart(selectedRange);
        });
    });
});