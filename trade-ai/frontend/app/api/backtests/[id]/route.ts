import { backendFetch } from "../../../../lib/server-api";

export async function GET(_: Request, { params }: { params: { id: string } }) {
  try {
    const data = await backendFetch(`/api/backtest/${params.id}/`);
    return Response.json(data);
  } catch (error) {
    return new Response("Not ready", { status: 202 });
  }
}
