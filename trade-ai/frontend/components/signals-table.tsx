"use client";

import useSWR from "swr";
import axios from "axios";

const fetcher = (url: string) => axios.get(url).then((res) => res.data);

export default function SignalsTable() {
  const { data } = useSWR("/api/signals", fetcher);
  const signals = data ?? [];
  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900 p-4">
      <table className="w-full text-left text-sm">
        <thead className="text-slate-400">
          <tr>
            <th>Symbol</th>
            <th>Direction</th>
            <th>Source</th>
            <th>Confidence</th>
            <th>Created</th>
          </tr>
        </thead>
        <tbody>
          {signals.map((signal: any) => (
            <tr key={signal.id} className="border-t border-slate-800">
              <td className="py-2">{signal.symbol}</td>
              <td className="py-2 capitalize">{signal.direction}</td>
              <td className="py-2 capitalize">{signal.source}</td>
              <td className="py-2">{signal.confidence_pct}%</td>
              <td className="py-2">{new Date(signal.created_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
