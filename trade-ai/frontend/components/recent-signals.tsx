"use client";

import useSWR from "swr";
import axios from "axios";

const fetcher = (url: string) => axios.get(url).then((res) => res.data);

export default function RecentSignals() {
  const { data } = useSWR("/api/signals/latest", fetcher);
  const signals = data ?? [];
  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900 p-4">
      <h2 className="text-lg font-semibold">Recent Signals</h2>
      <table className="mt-4 w-full text-left text-sm">
        <thead className="text-slate-400">
          <tr>
            <th>Symbol</th>
            <th>Direction</th>
            <th>Source</th>
            <th>Confidence</th>
          </tr>
        </thead>
        <tbody>
          {signals.map((signal: any) => (
            <tr key={signal.id} className="border-t border-slate-800">
              <td className="py-2">{signal.symbol}</td>
              <td className="py-2 capitalize">{signal.direction}</td>
              <td className="py-2 capitalize">{signal.source}</td>
              <td className="py-2">{signal.confidence_pct}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
