import { backendFetch } from "../../../../lib/server-api";

export async function GET() {
  try {
    const account = await backendFetch("/api/account/");
    
    if (!account) {
      return Response.json(
        { error: "Failed to fetch account data" },
        { status: 503 }
      );
    }

    return Response.json({
      account_value: account.account_value ?? 0,
      cash: account.cash ?? 0,
      buying_power: account.buying_power ?? 0,
      equity: account.equity ?? 0,
      account_number: account.account_number,
      status: account.status,
    });
  } catch (error) {
    console.error("Error fetching account:", error);
    return Response.json(
      { error: "Failed to fetch account data" },
      { status: 503 }
    );
  }
}
