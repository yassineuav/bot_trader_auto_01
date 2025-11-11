import { backendFetch } from "@/lib/server-api";

export async function GET() {
  try {
    const orders = await backendFetch("/api/orders/");
    const positions = await backendFetch("/api/positions/");
    const orderList = Array.isArray(orders) ? orders : [];
    const positionList = Array.isArray(positions) ? positions : [];
    const pnlToday = orderList.reduce((acc: number, order: any) => acc + Number(order.avg_fill_price || 0), 0);
    return Response.json({
      pnlToday,
      openPositions: positionList.length,
      signals: orderList.length,
    });
  } catch (error) {
    console.error("Error fetching KPIs:", error);
    return Response.json(
      { pnlToday: 0, openPositions: 0, signals: 0 },
      { status: 200 }
    );
  }
}
