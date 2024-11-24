document.getElementById('searchButton').addEventListener('click', async () => {
    // Collect search parameters
    const restaurantName = document.getElementById('restaurantName').value;
    const restaurantStyle = document.getElementById('restaurantStyle').value;
    const vegetarian = document.getElementById('vegetarian').checked;

    // Construct query parameters
    const queryParams = new URLSearchParams();
    if (restaurantName) queryParams.append('restaurant_name', restaurantName);
    if (restaurantStyle) queryParams.append('restaurant_style', restaurantStyle);
    if (vegetarian) queryParams.append('vegetarian', true);

    // Fetch search results from API
    try {
        const response = await fetch(`http://127.0.0.1:5000/search?${queryParams.toString()}`);
        const data = await response.json();

        // Render results
        const resultsDiv = document.getElementById('restaurantResults');
        resultsDiv.innerHTML = ''; // Clear previous results

        if (data.length > 0) {
            data.forEach(restaurant => {
                const div = document.createElement('div');
                div.className = 'restaurant-card';
                div.innerHTML = `
                    <h3>${restaurant.name}</h3>
                    <p>Style: ${restaurant.style}</p>
                    <p>Vegetarian: ${restaurant.vegetarian ? 'Yes' : 'No'}</p>
                    <p>Delivery: ${restaurant.delivery ? 'Available' : 'Unavailable'}</p>
                `;
                resultsDiv.appendChild(div);
            });
        } else {
            resultsDiv.innerHTML = '<p>No results found</p>';
        }
    } catch (error) {
        console.error('Error fetching search results:', error);
        alert('Failed to fetch search results. Please try again.');
    }
});
