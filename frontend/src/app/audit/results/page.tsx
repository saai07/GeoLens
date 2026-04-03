"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { AuditResponse } from "@/types/audit";
import ScoreHero from "@/components/ScoreHero";
import MetricGrid from "@/components/MetricGrid";
import JsonLdViewer from "@/components/JsonLdViewer";
import RecommendationList from "@/components/RecommendationList";
import PageSnapshot from "@/components/PageSnapshot";
import ExportButton from "@/components/ExportButton";
import Skeleton from "@/components/ui/Skeleton";

function ResultsSkeleton() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-8 space-y-12">
      {/* Score hero skeleton */}
      <div className="flex flex-col items-center gap-4 py-8">
        <Skeleton className="w-36 h-36 rounded-full" />
        <Skeleton className="w-48 h-8" />
      </div>

      {/* Metric grid skeleton */}
      <div className="space-y-3">
        <Skeleton className="w-40 h-4" />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-3">
          {[...Array(5)].map((_, i) => (
            <div key={i} className={`sm:col-span-1 ${i >= 3 ? "lg:col-span-3" : "lg:col-span-2"}`}>
              <div className="border border-gray-100 rounded-xl p-5 space-y-3">
                <Skeleton className="w-32 h-4" />
                <Skeleton className="w-16 h-8" />
                <Skeleton className="w-full h-1.5" />
                <Skeleton className="w-full h-3" />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recommendations skeleton */}
      <div className="space-y-3">
        <Skeleton className="w-48 h-4" />
        {[...Array(3)].map((_, i) => (
          <Skeleton key={i} className="w-full h-16" />
        ))}
      </div>
    </div>
  );
}

export default function ResultsPage() {
  const router = useRouter();
  const [data, setData] = useState<AuditResponse | null>(null);

  useEffect(() => {
    const raw = sessionStorage.getItem("geolens_result");
    if (!raw) {
      router.replace("/");
      return;
    }
    setData(JSON.parse(raw) as AuditResponse);
  }, [router]);

  if (!data) {
    return (
      <main className="min-h-screen bg-white">
        <header className="border-b border-gray-100 sticky top-0 bg-white/80 backdrop-blur-sm z-10">
          <div className="max-w-5xl mx-auto px-6 py-3 flex items-center justify-between">
            <div className="flex items-center gap-2 text-sm text-gray-500">
              <svg width="16" height="16" viewBox="0 0 32 32" fill="none" aria-hidden="true">
                <circle cx="16" cy="16" r="14" stroke="currentColor" strokeWidth="2" />
                <circle cx="16" cy="16" r="7" stroke="currentColor" strokeWidth="2" />
                <line x1="16" y1="2" x2="16" y2="30" stroke="currentColor" strokeWidth="2" />
                <line x1="2" y1="16" x2="30" y2="16" stroke="currentColor" strokeWidth="2" />
              </svg>
              <span className="font-semibold">GeoLens</span>
            </div>
            <Skeleton className="w-24 h-8" />
          </div>
        </header>
        <ResultsSkeleton />
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-white">
      {/* Top bar */}
      <header className="border-b border-gray-100 sticky top-0 bg-white/80 backdrop-blur-sm z-10">
        <div className="max-w-5xl mx-auto px-6 py-3 flex items-center justify-between">
          <button
            onClick={() => router.push("/")}
            className="flex items-center gap-2 text-sm text-gray-500 hover:text-black transition"
            aria-label="Back to home"
          >
            <svg width="16" height="16" viewBox="0 0 32 32" fill="none" aria-hidden="true">
              <circle cx="16" cy="16" r="14" stroke="currentColor" strokeWidth="2" />
              <circle cx="16" cy="16" r="7" stroke="currentColor" strokeWidth="2" />
              <line x1="16" y1="2" x2="16" y2="30" stroke="currentColor" strokeWidth="2" />
              <line x1="2" y1="16" x2="30" y2="16" stroke="currentColor" strokeWidth="2" />
            </svg>
            <span className="font-semibold">GeoLens</span>
          </button>

          <div className="flex items-center gap-3">
            <span className="text-xs text-gray-400 hidden sm:block truncate max-w-xs">{data.url}</span>
            <ExportButton data={data} />
          </div>
        </div>
      </header>

      {/* Content */}
      <div className="max-w-5xl mx-auto px-6 py-8 space-y-12">
        <ScoreHero data={data} />
        <MetricGrid data={data} />
        <RecommendationList data={data} />
        <JsonLdViewer data={data} />
        <PageSnapshot data={data} />

        {/* New audit button */}
        <div className="text-center pb-8">
          <button
            onClick={() => router.push("/")}
            className="text-sm text-gray-400 hover:text-black underline underline-offset-4 transition"
          >
            ← Run another audit
          </button>
        </div>
      </div>
    </main>
  );
}
