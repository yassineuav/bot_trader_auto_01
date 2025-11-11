"use client";

import useSWR from "swr";
import axios from "axios";

const fetcher = (url: string) => axios.get(url).then((res) => res.data);

export default function PositionsTable() {
  const { data } = useSWR("/api/positions", fetcher);
  const positions = data ?? [];
  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900 p-4">
      <table className="w-full text-left text-sm">
        <thead className="text-slate-400">
          <tr>
            <th>Symbol</th>
            <th>Side</th>
            <th>Qty</th>
            <th>Avg Price</th>
            <th>PNL %</th>
          </tr>
        </thead>
        <tbody>
          {positions.map((position: any) => (
            <tr key={position.id} className="border-t border-slate-800">
              <td className="py-2">{position.symbol}</td>
              <td className="py-2 capitalize">{position.side}</td>
              <td className="py-2">{position.qty}</td>
              <td className="py-2">{position.avg_price}</td>
              <td className="py-2">{position.pnl_pct ?? "--"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
