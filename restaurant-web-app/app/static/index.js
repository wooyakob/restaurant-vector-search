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
                                  <p>${result.content}</p>
                                  <p><strong>Address:</strong> ${result.location && result.location.address ? result.location.address : 'N/A'}</p>
                                  <p><strong>Phone:</strong> ${result.phone || 'N/A'}</p>
                                  <p><strong>Price:</strong> ${result.price || 'N/A'}</p>
                                  <p><strong>Website:</strong> <a href="${result.url}" target="_blank">${result.url}</a></p>`;
                
                // For specific Lat, Lon: <p><strong>Location:</strong> ${result.location && result.location.lat != null && result.location.lon != null ? `Lat: ${result.location.lat}, Lon: ${result.location.lon}` : 'N/A'}</p>

                if (result.location && result.location.embedUrl) {
                    const iframe = document.createElement("iframe");
                    iframe.width = "400";
                    iframe.height = "200";
                    iframe.style.border = "0";
                    iframe.loading = "lazy";
                    iframe.allowFullscreen = true;
                    iframe.referrerPolicy = "no-referrer-when-downgrade";
                    iframe.src = result.location.embedUrl;
                    card.appendChild(iframe);
                }
                resultsDiv.appendChild(card);
            });
        } else {
            resultsDiv.innerHTML = "<p>No results found.</p>";
        }
    });

    const input = document.getElementById("query");
    const span = document.createElement("span");
    span.style.visibility = "hidden";
    span.style.position = "absolute";
    span.style.whiteSpace = "pre";

    span.style.font = getComputedStyle(input).font;
    document.body.appendChild(span);

    function autoResize() {
        span.textContent = input.value || input.placeholder;
        const newWidth = span.offsetWidth + 20;
        input.style.width = newWidth + "px";
    }

    input.addEventListener("input", autoResize);
    autoResize();
});