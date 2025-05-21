import { fetchPoints } from "./fetchPoints.js";

let map;
const markerMap = {};
let lastClickedLatLng = null;

document.addEventListener('DOMContentLoaded', () => {
  map = L.map('map').setView([14.650983264532163, 121.06718461639298], 16);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  // Populate the map with points using the createMarker function defined below
  fetchPoints(map, createMarker);

  map.on('click', (e) => {
  const { lat, lng } = e.latlng;
  lastClickedLatLng = e.latlng;

  // Set values in the form
  document.getElementById('form-lat').value = lat.toFixed(6);
  document.getElementById('form-lng').value = lng.toFixed(6);

  // Optional: show popup just for feedback
  L.popup()
    .setLatLng(e.latlng)
    .setContent(`
      <div>
        <p>Selected:</p>
        <p>Lat: ${lat.toFixed(4)}</p>
        <p>Lng: ${lng.toFixed(4)}</p>
        // <p>→ Form fields updated below</p>
      </div>
    `)
    .openOn(map);
  });

  document.getElementById('information').addEventListener('submit', (e) => {
  const name = document.getElementById('form-name').value.trim();
  const lat = parseFloat(document.getElementById('form-lat').value);
  const lng = parseFloat(document.getElementById('form-lng').value);

  if (!isNaN(lat) && !isNaN(lng)) {
    createMarker(lat, lng, name);  // temporary marker without device_id
  }

  // Clear form fields
  document.getElementById('information').reset();

  // Let HTMX handle actual POST to server

  // Wait for HTMX to submit, then re-fetch points with real device_id
  setTimeout(() => {
    // Remove existing markers from map and sidebar
    Object.values(markerMap).forEach(marker => map.removeLayer(marker));
    Object.keys(markerMap).forEach(id => delete markerMap[id]);
    document.getElementById("markerList").innerHTML = '';

    // Re-fetch from server to get correct device_id
    fetchPoints(map, createMarker);
  }, 500); // small delay to allow server to store the point
});
});

/**
 * DEPRECATED
 */
window.addMarkerFromClick = function () {
  if (lastClickedLatLng) {
    const name = prompt("Enter a name for this observation point:", "New observation point");

    if (name !== null) {
      const { lat, lng } = lastClickedLatLng;
      createMarker(lat, lng, name.trim());
      map.closePopup();
    }
  }
};

/**
 * Delete marker inside server
 * @param {number} id 
 */
window.deleteMarker = async function (leafletId, deviceId) {
  if (deviceId !== null) {
    try {
      const response = await fetch("/delete_point", {
        method: "POST",
        headers: {
          "Content-Type": "application/json", // Set Content-Type to JSON
        },
        body: JSON.stringify({ device_id: deviceId }), // Send device_id as JSON
      });

      if (!response.ok) {
        alert("Failed to delete from server.");
        return;
      }

      // Optionally, show a success message
      const data = await response.json();
      alert(data.message);  // Example response from the server, like "Point successfully deleted."
    } catch (err) {
      console.error("Error deleting point:", err);
      alert("Error deleting point.");
      return;
    }
  }

  // Remove locally
  const marker = markerMap[leafletId];
  if (marker) {
    map.removeLayer(marker);
    delete markerMap[leafletId];
  }
  const entry = document.getElementById(`marker-${leafletId}`);
  if (entry) {
    entry.remove();
  }
};

/**
 * Add observation point details to map
 * @param {number} lat 
 * @param {number} lng 
 * @param {string} name 
 */
function createMarker(lat, lng, name, deviceId = null) {
  const marker = L.marker([lat, lng]).addTo(map);
  const leafletId = marker._leaflet_id;
  const safeName = name || "Unnamed observation point";

  let popupContent = `
    <strong>${safeName}</strong><br>
    (${lat.toFixed(4)}, ${lng.toFixed(4)})<br>
    ${deviceId ? `Device ID: ${deviceId}<br>` : ''}
  `;

  if (window.isUser != true){
    popupContent += `
      <button 
          onclick="deleteMarker(${leafletId}, ${deviceId})" 
          class="mt-2 px-2 bg-red-500 text-white rounded hover:bg-red-600 transition">
          Delete observation point
      </button>
    `;
  }

  // marker.bindPopup(`
  //   <strong>${safeName}</strong><br>
  //   (${lat.toFixed(4)}, ${lng.toFixed(4)})<br>
  //   ${deviceId ? `Device ID: ${deviceId}<br>` : ''}
  //   <button 
  //       onclick="deleteMarker(${leafletId}, ${deviceId})" 
  //       class="mt-2 px-2 bg-red-500 text-white rounded hover:bg-red-600 transition">
  //       Delete observation point
  //   </button>
  // `);
  marker.bindPopup(popupContent);

  marker.on('click', () => marker.openPopup());
  markerMap[leafletId] = marker;

  addMarkerToList(leafletId, lat, lng, safeName, deviceId);
}

/**
 * Append to local list (inside page) newly added observation point
 * @param {number} id 
 * @param {number} lat 
 * @param {number} lng 
 * @param {string} name 
 */
function addMarkerToList(id, lat, lng, name, deviceId = null) {
  const list = document.getElementById("markerList");
  const entry = document.createElement("div");

  entry.className = "marker-entry";
  entry.id = `marker-${id}`;

  const displayDeviceId = deviceId !== null ? deviceId : "(pending...)";

  const sensorInfoRow = deviceId !== null
    ? `<div class="flex items-center gap-2">
         <span>Device ID: ${displayDeviceId}</span>
         <a href="/points/${deviceId}" class="text-sm text-green-600 underline hover:text-green-800" target="_blank">View air data</a>
       </div>`
    : `<div>Device ID: ${displayDeviceId}</div>`;

  entry.innerHTML = window.isUser ? `
    <div class="border border-gray-500 rounded px-4 py-2 my-2">
      <span class="underline">${name}</span><br>
      ${sensorInfoRow}
      Latitude: ${lat.toFixed(4)}<br>
      Longitude: ${lng.toFixed(4)}<br>
    </div>
  `
  : `
    <div class="border border-gray-500 rounded px-4 py-2 my-2">
      <span class="underline">${name}</span><br>
      ${sensorInfoRow}
      Latitude: ${lat.toFixed(4)}<br>
      Longitude: ${lng.toFixed(4)}<br>
      <button 
        onclick="deleteMarker(${id}, ${deviceId})"
        class="mt-1 px-2 bg-red-500 text-white rounded hover:bg-red-600 transition">
          Delete observation point
      </button>
    </div>
  `
  ;
  list.appendChild(entry);
}

