"use client";

import useSWR from "swr";
import axios from "axios";

const fetcher = (url: string) => 
  axios.get(url).then((res) => res.data).catch((err) => {
    console.error("Fetch error:", err);
    return { pnlToday: 0, openPositions: 0, signals: 0 };
  });

export default function SummaryCards() {
  const { data } = useSWR("/api/dashboard/kpis", fetcher);
  const kpis = data ?? { pnlToday: 0, openPositions: 0, signals: 0 };
  return (
    <div className="grid gap-4 md:grid-cols-3">
      {[
        { label: "PNL Today", value: `$${kpis.pnlToday.toFixed?.(2) ?? 0}` },
        { label: "Open Positions", value: kpis.openPositions },
        { label: "Signals (24h)", value: kpis.signals },
      ].map((item) => (
        <div key={item.label} className="rounded-lg border border-slate-800 bg-slate-900 p-4">
          <p className="text-sm text-slate-400">{item.label}</p>
          <p className="mt-2 text-2xl font-bold">{item.value}</p>
        </div>
      ))}
    </div>
  );
}
