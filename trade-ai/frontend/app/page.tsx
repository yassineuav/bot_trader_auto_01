import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4">
      <h1 className="text-4xl font-bold">Trade AI Control Center</h1>
      <p className="text-slate-300">Manage sentiment-driven options strategies.</p>
      <Link
        href="/dashboard"
        className="rounded bg-sky-500 px-4 py-2 font-semibold text-white hover:bg-sky-400"
      >
        Enter Dashboard
      </Link>
    </main>
  );
}
