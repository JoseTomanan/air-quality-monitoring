let map;
const markerMap = {};
let lastClickedLatLng = null;

document.addEventListener('DOMContentLoaded', () => {
  map = L.map('map').setView([14.650983264532163, 121.06718461639298], 16);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  map.on('click', (e) => {
    const { lat, lng } = e.latlng;
    lastClickedLatLng = e.latlng;
    L.popup()
      .setLatLng(e.latlng)
      .setContent(`
        <div>
            <p><strong>Clicked location:</strong></p>
            <p>Latitude: ${lat.toFixed(4)}</p>
            <p>Longitude: ${lng.toFixed(4)}</p>
            <button 
            onclick="addMarkerFromClick()" 
            class="mt-2 px-2 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
            >
            Add Marker Here
            </button>
        </div>
        `)
      .openOn(map);
  });

  document.getElementById('information').addEventListener('submit', (e) => {
    const name = document.getElementById('form-name').value.trim();
    const lat = parseFloat(document.getElementById('form-lat').value);
    const lng = parseFloat(document.getElementById('form-lng').value);

    if (!isNaN(lat) && !isNaN(lng)) {
      createMarker(lat, lng, name);
    }

    // Let HTMX handle form submission
  });
});

window.addMarkerFromClick = function () {
  if (lastClickedLatLng) {
    const name = prompt("Enter a name for this marker:", "My Marker");
    if (name !== null) {
      const { lat, lng } = lastClickedLatLng;
      createMarker(lat, lng, name.trim());
      map.closePopup();
    }
  }
};

window.deleteMarker = function (id) {
  const marker = markerMap[id];
  if (marker) {
    map.removeLayer(marker);
    delete markerMap[id];
  }
  const entry = document.getElementById(`marker-${id}`);
  if (entry) {
    entry.remove();
  }
};

function createMarker(lat, lng, name) {
  const marker = L.marker([lat, lng]).addTo(map);
  const id = marker._leaflet_id;
  const safeName = name || "Unnamed Marker";

  marker.bindPopup(`
    <strong>${safeName}</strong><br>
    (${lat.toFixed(4)}, ${lng.toFixed(4)})<br>
    <button 
        onclick="deleteMarker(${id})" 
        class="mt-2 px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600 transition">
    Delete Marker
    </button>
  `);

  marker.on('click', () => marker.openPopup());
  markerMap[id] = marker;

  addMarkerToList(id, lat, lng, safeName);
}

function addMarkerToList(id, lat, lng, name) {
  const list = document.getElementById("markerList");
  const entry = document.createElement("div");
  entry.className = "marker-entry";
  entry.id = `marker-${id}`;
  entry.innerHTML = `
    <strong>${name}</strong><br>
    Latitude: ${lat.toFixed(4)}<br>
    Longitude: ${lng.toFixed(4)}<br>
    <button 
        onclick="deleteMarker(${id})" 
        class="mt-2 px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600 transition">
    Delete Marker
    </button>
  `;
  list.appendChild(entry);
}
