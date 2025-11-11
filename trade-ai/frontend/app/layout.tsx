import "../globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Trade AI Dashboard",
  description: "Monitor AI-driven trading strategies",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="h-full">
      <body className="min-h-screen bg-slate-950 text-slate-100">{children}</body>
    </html>
  );
}
