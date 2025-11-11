import { backendFetch } from "../../../lib/server-api";

export async function GET() {
  const data = await backendFetch("/api/positions/");
  return Response.json(data);
}
