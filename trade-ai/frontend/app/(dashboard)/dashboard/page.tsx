import { Suspense } from "react";
import SummaryCards from "../../../components/summary-cards";
import AccountDetails from "../../../components/account-details";
import RecentSignals from "../../../components/recent-signals";

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Dashboard</h1>
      <Suspense fallback={<div>Loading KPIs...</div>}>
        <SummaryCards />
      </Suspense>
      <Suspense fallback={<div>Loading account details...</div>}>
        <AccountDetails />
      </Suspense>
      <Suspense fallback={<div>Loading signals...</div>}>
        <RecentSignals />
      </Suspense>
    </div>
  );
}
