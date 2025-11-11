"use client";

import { useState } from "react";
import useSWR from "swr";
import axios from "axios";

const fetcher = (url: string) => 
  axios.get(url).then((res) => res.data).catch((err) => {
    console.error("Fetch error:", err);
    return {
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
    };
  });

interface AccountData {
  account_value: number;
  cash: number;
  buying_power: number;
  equity: number;
  day_trading_buying_power: number;
  last_equity: number;
  account_number: string;
  status: string;
  multiplier: number;
  shorting_enabled: boolean;
}

export default function AccountDetails() {
  const { data, isLoading, mutate } = useSWR("/api/account", fetcher, {
    refreshInterval: 30000, // Refresh every 30 seconds
    revalidateOnFocus: true,
  });
  
  const [isRefreshing, setIsRefreshing] = useState(false);

  const account: AccountData = data ?? {
    account_value: 0,
    cash: 0,
    buying_power: 0,
    equity: 0,
    day_trading_buying_power: 0,
    last_equity: 0,
    account_number: "N/A",
    status: "unknown",
    multiplier: 1,
    shorting_enabled: false,
  };

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await mutate();
    setIsRefreshing(false);
  };

  // Calculate unrealized profit/loss
  const unrealizedPnL = account.account_value - account.last_equity;
  const pnlPercentage = account.last_equity > 0 
    ? ((unrealizedPnL / account.last_equity) * 100).toFixed(2)
    : 0;

  // Determine status color
  const getStatusColor = (status: string) => {
    switch (status?.toLowerCase()) {
      case "active":
        return "text-green-400";
      case "not_configured":
        return "text-yellow-400";
      case "error":
      case "unavailable":
        return "text-red-400";
      default:
        return "text-slate-400";
    }
  };

  // Determine PnL color
  const getPnLColor = (pnl: number) => {
    if (pnl > 0) return "text-green-400";
    if (pnl < 0) return "text-red-400";
    return "text-slate-400";
  };

  const details = [
    { label: "Account Number", value: account.account_number, highlight: false },
    { label: "Status", value: account.status, highlight: true, colorClass: getStatusColor(account.status) },
    { label: "Account Value", value: `$${account.account_value.toFixed(2)}`, highlight: true },
    { label: "Cash Available", value: `$${account.cash.toFixed(2)}`, highlight: false },
    { label: "Buying Power", value: `$${account.buying_power.toFixed(2)}`, highlight: false },
    { label: "Day Trading Buying Power", value: `$${account.day_trading_buying_power.toFixed(2)}`, highlight: false },
    { label: "Equity", value: `$${account.equity.toFixed(2)}`, highlight: true },
    { label: "Unrealized P&L", value: `$${unrealizedPnL.toFixed(2)} (${pnlPercentage}%)`, highlight: true, colorClass: getPnLColor(unrealizedPnL) },
  ];

  if (isLoading) {
    return (
      <div className="rounded-lg border border-slate-800 bg-slate-900 p-6">
        <div className="text-slate-400">Loading account details...</div>
      </div>
    );
  }

  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900 p-6">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-xl font-semibold">Alpaca Account Details</h2>
        <button
          onClick={handleRefresh}
          disabled={isRefreshing}
          className="rounded px-3 py-1 text-sm bg-slate-700 hover:bg-slate-600 disabled:opacity-50 transition-colors"
        >
          {isRefreshing ? "Refreshing..." : "Refresh"}
        </button>
      </div>
      
      {account.status === "not_configured" && (
        <div className="mb-4 p-3 bg-yellow-900/20 border border-yellow-700 rounded text-yellow-400 text-sm">
          ⚠️ Alpaca API credentials not configured. Please add ALPACA_API_KEY and ALPACA_API_SECRET to your environment.
        </div>
      )}
      
      {(account.status === "error" || account.status === "unavailable") && (
        <div className="mb-4 p-3 bg-red-900/20 border border-red-700 rounded text-red-400 text-sm">
          ❌ Unable to fetch account data. Please check your API credentials and connection.
        </div>
      )}

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {details.map((item) => (
          <div 
            key={item.label} 
            className={`border-l-2 pl-4 ${
              item.highlight ? "border-blue-500 bg-slate-800/50 p-4 rounded" : "border-slate-700"
            }`}
          >
            <p className="text-sm text-slate-400">{item.label}</p>
            <p className={`mt-1 text-lg font-semibold text-slate-100 ${item.colorClass || ""}`}>
              {item.value}
            </p>
          </div>
        ))}
      </div>

      <div className="mt-4 text-xs text-slate-500">
        Last updated: {new Date().toLocaleTimeString()}
      </div>
    </div>
  );
}
