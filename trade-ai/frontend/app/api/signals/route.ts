import { backendFetch } from "../../../lib/server-api";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const symbol = searchParams.get("symbol");
  const query = symbol ? `?symbol=${symbol}` : "";
  const data = await backendFetch(`/api/signals/${query}`);
  return Response.json(data);
}
