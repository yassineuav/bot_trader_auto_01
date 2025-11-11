import { backendFetch } from "../../../../lib/server-api";

export async function GET() {
  const data = await backendFetch("/api/signals/latest/");
  return Response.json(data);
}
