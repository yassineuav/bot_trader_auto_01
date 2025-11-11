"use client";

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
      account_number: "N/A",
      status: "error",
    };
  });

interface AccountData {
  account_value: number;
  cash: number;
  buying_power: number;
  equity: number;
  account_number: string;
  status: string;
}

export default function AccountDetails() {
  const { data, isLoading } = useSWR("/api/account", fetcher);
  
  const account: AccountData = data ?? {
    account_value: 0,
    cash: 0,
    buying_power: 0,
    equity: 0,
    account_number: "N/A",
    status: "unknown",
  };

  if (isLoading) {
    return <div className="text-slate-400">Loading account details...</div>;
  }

  const details = [
    { label: "Account Value", value: `$${account.account_value.toFixed(2)}` },
    { label: "Cash Available", value: `$${account.cash.toFixed(2)}` },
    { label: "Buying Power", value: `$${account.buying_power.toFixed(2)}` },
    { label: "Equity", value: `$${account.equity.toFixed(2)}` },
    { label: "Account Number", value: account.account_number },
    { label: "Status", value: account.status },
  ];

  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900 p-6">
      <h2 className="mb-4 text-xl font-semibold">Account Details</h2>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {details.map((item) => (
          <div key={item.label} className="border-l-2 border-slate-700 pl-4">
            <p className="text-sm text-slate-400">{item.label}</p>
            <p className="mt-1 text-lg font-semibold text-slate-100">{item.value}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
