"use client";

import { useState } from "react";
import useSWR from "swr";
import axios from "axios";

const fetcher = (url: string) => axios.get(url).then((res) => res.data);

export default function BacktestPanel() {
  const [jobId, setJobId] = useState<string | null>(null);
  const { data } = useSWR(jobId ? `/api/backtests/${jobId}` : null, fetcher, {
    refreshInterval: 3000,
  });

  const runBacktest = async () => {
    const response = await axios.post("/api/backtests", {
      symbol: "SPY",
      mode: "hybrid",
    });
    setJobId(response.data.job_id);
  };

  return (
    <div className="space-y-4 rounded-lg border border-slate-800 bg-slate-900 p-4">
      <button
        onClick={runBacktest}
        className="rounded bg-sky-500 px-4 py-2 text-sm font-semibold text-white hover:bg-sky-400"
      >
        Run Backtest
      </button>
      {jobId && (
        <div className="rounded border border-slate-800 p-4">
          <p className="text-sm text-slate-400">Job ID: {jobId}</p>
          <pre className="mt-2 whitespace-pre-wrap text-xs">
            {JSON.stringify(data ?? { status: "pending" }, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
