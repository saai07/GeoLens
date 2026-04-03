import { MetricResult } from "@/types/audit";

const STATUS_STYLES: Record<string, { badge: string; bar: string }> = {
  pass: { badge: "bg-green-50 text-green-700 border-green-200", bar: "bg-green-500" },
  partial: { badge: "bg-yellow-50 text-yellow-700 border-yellow-200", bar: "bg-yellow-400" },
  fail: { badge: "bg-red-50 text-red-600 border-red-200", bar: "bg-red-400" },
};

export default function MetricCard({ metric }: { metric: MetricResult }) {
  const pct = Math.round((metric.score / metric.max_score) * 100);
  const styles = STATUS_STYLES[metric.status] ?? STATUS_STYLES.fail;

  return (
    <div className="border border-gray-100 rounded-xl p-5 space-y-3 hover:border-gray-200 transition">
      {/* Header */}
      <div className="flex items-start justify-between gap-2">
        <span className="text-sm font-medium text-gray-900">{metric.metric}</span>
        <span className={`text-xs font-medium px-2 py-0.5 rounded-full border ${styles.badge} capitalize flex-shrink-0`}>
          {metric.status}
        </span>
      </div>

      {/* Score */}
      <div className="text-2xl font-bold">
        {metric.score}
        <span className="text-sm font-normal text-gray-400 ml-1">/ {metric.max_score}</span>
      </div>

      {/* Progress bar */}
      <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full ${styles.bar} transition-all duration-500`}
          style={{ width: `${pct}%` }}
        />
      </div>

      {/* Detail */}
      <p className="text-xs text-gray-400 leading-relaxed">{metric.detail}</p>
    </div>
  );
}
