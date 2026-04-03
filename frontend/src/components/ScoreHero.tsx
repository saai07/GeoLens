import { AuditResponse } from "@/types/audit";

const GRADE_COLORS: Record<string, { stroke: string; text: string; label: string }> = {
  A: { stroke: "#22c55e", text: "text-green-500", label: "Excellent GEO readiness" },
  B: { stroke: "#3b82f6", text: "text-blue-500", label: "Good GEO readiness" },
  C: { stroke: "#eab308", text: "text-yellow-500", label: "Moderate GEO readiness" },
  D: { stroke: "#f97316", text: "text-orange-500", label: "Poor GEO readiness" },
  F: { stroke: "#ef4444", text: "text-red-500", label: "Not GEO optimized" },
};

const RADIUS = 52;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS;

export default function ScoreHero({ data }: { data: AuditResponse }) {
  const { geo_score, geo_grade } = data;
  const config = GRADE_COLORS[geo_grade] ?? GRADE_COLORS["F"];
  const dashOffset = CIRCUMFERENCE * (1 - geo_score / 100);

  return (
    <div className="flex flex-col items-center gap-4 py-8">
      {/* Score ring */}
      <div className="relative w-36 h-36">
        <svg width="144" height="144" viewBox="0 0 144 144" className="-rotate-90">
          {/* Track */}
          <circle cx="72" cy="72" r={RADIUS} fill="none" stroke="#f3f4f6" strokeWidth="10" />
          {/* Progress */}
          <circle
            cx="72"
            cy="72"
            r={RADIUS}
            fill="none"
            stroke={config.stroke}
            strokeWidth="10"
            strokeLinecap="round"
            strokeDasharray={CIRCUMFERENCE}
            strokeDashoffset={dashOffset}
            className="transition-all duration-700 ease-out"
          />
        </svg>

        {/* Score label inside ring */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-3xl font-bold leading-none">{geo_score}</span>
          <span className="text-xs text-gray-400 mt-1">/ 100</span>
        </div>
      </div>

      {/* Grade badge */}
      <div className="flex items-center gap-3">
        <span className={`text-5xl font-bold ${config.text}`}>{geo_grade}</span>
        <div className="text-left">
          <p className="text-sm font-medium text-gray-900">GEO Grade</p>
          <p className="text-sm text-gray-400">{config.label}</p>
        </div>
      </div>
    </div>
  );
}
