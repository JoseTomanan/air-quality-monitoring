export async function fetchPoints() {
  const response = await fetch('/points');

  if (!response.ok)
      throw new Error("Failed to fetch points");
  
  return response.json(); // Should be array of { name, lat, lng }
}

// TODO
// : Populate map with fetched points
// : can use createMarker for this?
