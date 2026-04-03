import { AuditResponse } from "@/types/audit";
import MetricCard from "./MetricCard";

export default function MetricGrid({ data }: { data: AuditResponse }) {
  const metrics = data.metrics;
  const lastRowCount = metrics.length % 3;

  return (
    <section className="space-y-3">
      <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider">Metric Breakdown</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-3">
        {metrics.map((metric, i) => {
          const isLastRow = i >= metrics.length - lastRowCount;
          const span = isLastRow && lastRowCount === 2 ? "lg:col-span-3" : "lg:col-span-2";

          return (
            <div key={metric.metric} className={`sm:col-span-1 ${span}`}>
              <MetricCard metric={metric} />
            </div>
          );
        })}
      </div>
    </section>
  );
}
