from json import load
from os import path


def generate_html_from_json(json_file, output_file):
    with open(json_file) as f:
        data = load(f)

    # Calculate average coordinates
    total_latitude = 0
    total_longitude = 0
    num_items = len(data)
    if num_items > 0:
        for user_id, user_data in data.items():
            total_latitude += user_data["coordinates_average"]["latitude"]
            total_longitude += user_data["coordinates_average"]["longitude"]

        average_latitude = total_latitude / num_items
        average_longitude = total_longitude / num_items
    else:
        # Handle the case where there are no items in the data
        average_latitude = 0
        average_longitude = 0

    # Generate JavaScript code for average coordinates
    average_coordinates_js = f"var map = L.map('map').setView([{average_latitude}, {average_longitude}], 2);\n"

    # Generate JavaScript code for points
    points_js = "var points = [\n"
    for user_id, user_data in data.items():
        username = user_data["username"].replace("'", "&apos;").replace("\\", "&#92;") if user_data["username"] else ""
        first_name = (
            user_data["first_name"].replace("'", "&apos;").replace("\\", "&#92;") if user_data["first_name"] else ""
        )
        last_name = (
            user_data["last_name"].replace("'", "&apos;").replace("\\", "&#92;") if user_data["last_name"] else ""
        )
        phone = user_data["phone"] or ""
        coordinates = user_data["coordinates_average"]
        latitude = coordinates["latitude"]
        longitude = coordinates["longitude"]
        image_url = f"avatars/{user_id}-{user_data['username'] or '.no_avatar'}.jpg"
        if path.exists("./" + image_url):
            image_url = "../" + image_url
        else:
            image_url = "../avatars/.no_avatar.jpg"
        name = f"{first_name} {last_name}"
        coordinates_text = f"<br> • latitude: {latitude}<br> • longitude: {longitude}"
        datetime = user_data["coordinates"][0][2] if user_data["coordinates"] else ""
        points_js += f"\t{{ coordinates: [{latitude}, {longitude}], imageUrl: '{image_url}', name: '{name}', username: '{username}', phone: '{phone}', coordinates_text: '{coordinates_text}', datetime: '{datetime}' }},\n"
    points_js += "];\n"

    # Generate HTML content
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Local Map</title>
    <link rel="stylesheet" href="../leaflet/leaflet.css" />
    <link rel="stylesheet" href="../leaflet/css/main.css" />
    <link rel="stylesheet" href="../leaflet/css/MarkerCluster.css" />
    <link rel="stylesheet" href="../leaflet/css/MarkerCluster.Default.css" />
        <style>
        .rounded-marker-icon {{
            border-radius: 50%;
            overflow: hidden;
            border: 5px solid white;
        }}

        .image-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%; /* Adjust as needed */
        }}
    </style>
</head>
<body>
    <div id="map-container">
        <div id="map"></div>
    </div>
    <div id="sidebar">
        <div id="stats-total" class="sidebar-stats">Total points: {num_items}</div>
        <div id="stats-visible" class="sidebar-stats">Visible points: 0</div>
    </div>

    <script src="../leaflet/leaflet.js"></script>
    <script src="../leaflet/js/leaflet.markercluster.js"></script>
    <script>
        {average_coordinates_js}
        {points_js}

        // Initialize marker cluster group
        var markers = L.markerClusterGroup();

        // Function to update statistics
        function updateStats() {{
            document.getElementById('stats-total').textContent = "Total points: " + points.length;
            var visibleCount = Array.from(document.querySelectorAll('.sidebar-item')).filter(function(item) {{
                return item.style.display !== 'none';
            }}).length;
            document.getElementById('stats-visible').textContent = "Visible points: " + visibleCount;
        }}

        points.forEach(function(point, index) {{
            var imageUrl = point.imageUrl; // Avatar image URL

            // Create a custom icon with the avatar image
            var customIcon = L.icon({{
                iconUrl: imageUrl,
                iconSize: [50, 50],  // Adjust the icon size as needed
                iconAnchor: [25, 50], // Adjust the icon anchor point if necessary
                popupAnchor: [5, -50], // Adjust the popup anchor point if necessary
                className: 'rounded-marker-icon' // Apply the custom CSS class
            }});

            // Create a marker with the custom icon
            var marker = L.marker(point.coordinates, {{icon: customIcon}});

            // Define the popup content
            var popupContent = '<div><p><b>' + point.name + '</b><br>Username: <a target="_blank" href="https://t.me/' + point.username + '">' + point.username + '</a></br>Phone: ' + point.phone + '<br>Coordinates:' + point.coordinates_text + '<br>Date: ' + point.datetime + '</p><div class="image-container"><img class="rounded-marker-icon" src="' + imageUrl + '"></div></div>';

            // Bind the popup content to the marker
            marker.bindPopup(popupContent);

            // Add the marker to the markers cluster group
            markers.addLayer(marker);

            // Create sidebar item
            var sidebarItem = document.createElement('div');
            sidebarItem.className = 'sidebar-item';
            sidebarItem.innerHTML = "<img src='" + imageUrl + "' width='40px' class=sidebar_item_img_span> <span class=sidebar_item_img_span>" + point.name + "<br>Username: <a target='_blank' href='https://t.me/" + point.username + "'>" + point.username + "</a>";
            sidebarItem.setAttribute('data-lat', point.coordinates[0]);
            sidebarItem.setAttribute('data-lng', point.coordinates[1]);

            // Highlight corresponding marker on map when sidebar item is hovered over
            sidebarItem.addEventListener('mouseover', function() {{
                marker.openPopup();
                document.querySelectorAll('.sidebar-item').forEach(function(item) {{
                    item.classList.remove('active');
                }});
                this.classList.add('active');
            }});

            sidebar.appendChild(sidebarItem);
        }});

        // Highlight corresponding sidebar item when marker is hovered over on the map
        document.getElementById('map').addEventListener('mouseover', function() {{
            document.querySelectorAll('.sidebar-item').forEach(function(item) {{
                item.classList.remove('active');
            }});
        }});

        // Filter sidebar items based on visible map bounds
        map.on('moveend', function() {{
            var bounds = map.getBounds();
            document.querySelectorAll('.sidebar-item').forEach(function(item) {{
                var lat = parseFloat(item.getAttribute('data-lat'));
                var lng = parseFloat(item.getAttribute('data-lng'));
                var isVisible = bounds.contains([lat, lng]);
                item.style.display = isVisible ? 'block' : 'none';
            }});
            updateStats(); // Update statistics on moveend event
        }});

        // Initially update statistics
        updateStats();

        L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);
        map.addLayer(markers);

    </script>
</body>
</html>
"""
    # Write HTML content to output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)


# Usage example:
# generate_html_from_json("./reports-json/_combined_data.json", "./reports-html/_combined_data.html")
