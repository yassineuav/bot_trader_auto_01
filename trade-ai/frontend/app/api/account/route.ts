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
          day_trading_buying_power: 0,
          last_equity: 0,
          account_number: "N/A",
          status: "unavailable",
          multiplier: 1,
          shorting_enabled: false,
        },
        { status: 200 }
      );
    }

    return Response.json({
      account_value: account.account_value ?? 0,
      cash: account.cash ?? 0,
      buying_power: account.buying_power ?? 0,
      equity: account.equity ?? 0,
      day_trading_buying_power: account.day_trading_buying_power ?? 0,
      last_equity: account.last_equity ?? 0,
      account_number: account.account_number ?? "N/A",
      status: account.status ?? "unknown",
      multiplier: account.multiplier ?? 1,
      shorting_enabled: account.shorting_enabled ?? false,
    });
  } catch (error) {
    console.error("Error fetching account:", error);
    return Response.json(
      {
        account_value: 0,
        cash: 0,
        buying_power: 0,
        equity: 0,
        day_trading_buying_power: 0,
        last_equity: 0,
        account_number: "N/A",
        status: "error",
        multiplier: 1,
        shorting_enabled: false,
      },
      { status: 200 }
    );
  }
}
