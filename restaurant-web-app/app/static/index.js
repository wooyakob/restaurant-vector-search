window.addEventListener("DOMContentLoaded", async () => {
    try {
        const response = await fetch("/api/restaurant_count");
        const data = await response.json();
        document.getElementById("restaurantCountDisplay").innerText = "Total Restaurants: " + data.count;
    } catch (error) {
        console.error("Error fetching restaurant count:", error);
        document.getElementById("restaurantCountDisplay").innerText = "Unable to load restaurant count.";
    }

    const form = document.getElementById("searchForm");
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const query = document.getElementById("query").value;
        const response = await fetch("/", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({ query })
        });
        const data = await response.json();
        const resultsDiv = document.getElementById("results");
        resultsDiv.innerHTML = "";
        if (data.results && data.results.length > 0) {
            data.results.forEach(result => {
                const card = document.createElement("div");
                card.className = "result-card";
                card.innerHTML = `<h2>${result.name}</h2>
                                  <p>${result.content}</p>`;
                resultsDiv.appendChild(card);
            });
        } else {
            resultsDiv.innerHTML = "<p>No results found.</p>";
        }
    });
});