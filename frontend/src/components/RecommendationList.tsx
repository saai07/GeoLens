import { AuditResponse } from "@/types/audit";

export default function RecommendationList({ data }: { data: AuditResponse }) {
  return (
    <section className="space-y-3">
      <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider">
        Top Recommendations
      </h2>
      <div className="space-y-3">
        {data.recommendations.map((rec, i) => (
          <div key={i} className="flex gap-4 border border-gray-100 rounded-xl p-4 hover:border-gray-200 transition">
            {/* Priority number */}
            <div className="flex-shrink-0 w-7 h-7 rounded-full bg-black text-white flex items-center justify-center text-xs font-bold">
              {i + 1}
            </div>

            {/* Text */}
            <p className="text-sm text-gray-700 leading-relaxed pt-0.5">{rec}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
