const BASE_URL = process.env.BACKEND_URL || "http://backend:8000";

export async function GET() {
  const res = await fetch(`${BASE_URL}/api/configs/`, { cache: "no-store" });
  const data = await res.json();
  return Response.json(data);
}

export async function PATCH(request: Request) {
  const body = await request.json();
  const res = await fetch(`${BASE_URL}/api/configs/${body.key}/`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ value_json: JSON.parse(body.value) }),
  });
  if (!res.ok) {
    return new Response("Failed to update", { status: res.status });
  }
  return Response.json(await res.json());
}
