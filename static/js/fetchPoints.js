export async function fetchPoints() {
  const response = await fetch('/api/points'); // Replace with your actual endpoint
  if (!response.ok) throw new Error("Failed to fetch points");
  return response.json(); // Should be array of { name, lat, lng }
}
