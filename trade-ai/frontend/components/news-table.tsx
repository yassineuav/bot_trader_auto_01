"use client";

import useSWR from "swr";
import axios from "axios";

const fetcher = (url: string) => axios.get(url).then((res) => res.data);

export default function NewsTable() {
  const { data } = useSWR("/api/news", fetcher);
  const articles = data ?? [];
  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900 p-4">
      <table className="w-full text-left text-sm">
        <thead className="text-slate-400">
          <tr>
            <th>Title</th>
            <th>Source</th>
            <th>Published</th>
            <th>Sentiment</th>
          </tr>
        </thead>
        <tbody>
          {articles.map((article: any) => (
            <tr key={article.id} className="border-t border-slate-800">
              <td className="py-2">{article.title}</td>
              <td className="py-2">{article.source}</td>
              <td className="py-2">{new Date(article.published_at).toLocaleString()}</td>
              <td className="py-2">
                {article.sentiments?.[0]?.label ?? "pending"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
