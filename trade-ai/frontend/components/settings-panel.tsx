"use client";

import { useState } from "react";
import useSWR from "swr";
import axios from "axios";

const fetcher = (url: string) => axios.get(url).then((res) => res.data);

export default function SettingsPanel() {
  const { data, mutate } = useSWR("/api/config", fetcher);
  const [saving, setSaving] = useState(false);

  const updateConfig = async (key: string, value: string) => {
    setSaving(true);
    await axios.patch("/api/config", { key, value });
    await mutate();
    setSaving(false);
  };

  return (
    <div className="space-y-4 rounded-lg border border-slate-800 bg-slate-900 p-4">
      <h2 className="text-lg font-semibold">Strategy Controls</h2>
      <div className="space-y-2 text-sm text-slate-300">
        {data?.map((item: any) => (
          <div key={item.id} className="flex items-center justify-between">
            <span>{item.key}</span>
            <button
              onClick={() => updateConfig(item.key, JSON.stringify(item.value_json))}
              className="rounded border border-slate-700 px-3 py-1 text-xs hover:bg-slate-800"
              disabled={saving}
            >
              Save
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
