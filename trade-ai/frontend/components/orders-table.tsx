"use client";

import useSWR from "swr";
import axios from "axios";

const fetcher = (url: string) => axios.get(url).then((res) => res.data);

export default function OrdersTable() {
  const { data } = useSWR("/api/orders", fetcher);
  const orders = data ?? [];
  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900 p-4">
      <table className="w-full text-left text-sm">
        <thead className="text-slate-400">
          <tr>
            <th>Symbol</th>
            <th>Status</th>
            <th>Qty</th>
            <th>Avg Fill</th>
            <th>Created</th>
          </tr>
        </thead>
        <tbody>
          {orders.map((order: any) => (
            <tr key={order.id} className="border-t border-slate-800">
              <td className="py-2">{order.symbol}</td>
              <td className="py-2 capitalize">{order.status}</td>
              <td className="py-2">{order.qty}</td>
              <td className="py-2">{order.avg_fill_price}</td>
              <td className="py-2">{new Date(order.created_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
