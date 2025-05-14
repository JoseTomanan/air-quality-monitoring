/**
 * Fetches observation points from backend and populates map
 * @param {L.Map} map - Leaflet map instance
 * @param {Function} createMarker - Function to add a marker on the map
 */
export async function fetchPoints(map, createMarker) {
  const response = await fetch('/points');

  if (!response.ok)
    throw new Error("Failed to fetch points");

  const points = await response.json(); // Array of ObservationPoint from backend

  points.forEach(point => {
    createMarker(point.latitude, point.longitude, point.location_name, point.device_id);
  });
}
