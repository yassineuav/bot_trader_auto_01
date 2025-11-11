import OrdersTable from "../../../components/orders-table";

export default function OrdersPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Orders</h1>
      <OrdersTable />
    </div>
  );
}
