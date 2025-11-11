import { backendFetch } from "../../../lib/server-api";

export async function POST(request: Request) {
  const body = await request.json();
  const res = await fetch(`${process.env.BACKEND_URL || "http://backend:8000"}/api/backtest/run/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    return new Response("Failed to trigger backtest", { status: res.status });
  }
  const data = await res.json();
  return Response.json(data);
}
