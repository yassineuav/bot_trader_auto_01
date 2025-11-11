import { backendFetch } from "../../../lib/server-api";

export async function GET() {
  const data = await backendFetch("/api/articles/");
  return Response.json(data);
}
