import { backendFetch } from "@/lib/server-api";

export async function GET() {
  try {
    const account = await backendFetch("/api/account/");
    
    if (!account) {
      return Response.json(
        {
          account_value: 0,
          cash: 0,
          buying_power: 0,
          equity: 0,
          account_number: "N/A",
          status: "unavailable",
        },
        { status: 200 }
      );
    }

    return Response.json({
      account_value: account.account_value ?? 0,
      cash: account.cash ?? 0,
      buying_power: account.buying_power ?? 0,
      equity: account.equity ?? 0,
      account_number: account.account_number ?? "N/A",
      status: account.status ?? "unknown",
    });
  } catch (error) {
    console.error("Error fetching account:", error);
    return Response.json(
      {
        account_value: 0,
        cash: 0,
        buying_power: 0,
        equity: 0,
        account_number: "N/A",
        status: "error",
      },
      { status: 200 }
    );
  }
}
