"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { runAudit } from "@/lib/api";

const STEPS = [
  { label: "Fetching page", duration: 1200 },
  { label: "Analyzing structure", duration: 2000 },
  { label: "Generating schema", duration: 1800 },
];

export default function LoadingPage() {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState(0);
  const [error, setError] = useState("");
  const [auditUrl, setAuditUrl] = useState("");

  useEffect(() => {
    const url = sessionStorage.getItem("geolens_url");
    if (!url) {
      router.replace("/");
      return;
    }

    setAuditUrl(url);

    // Animate steps while the API call runs in parallel
    let step = 0;
    const advance = () => {
      if (step < STEPS.length - 1) {
        step++;
        setCurrentStep(step);
        setTimeout(advance, STEPS[step].duration);
      }
    };
    setTimeout(advance, STEPS[0].duration);

    // Actual API call
    runAudit(url)
      .then((result) => {
        sessionStorage.setItem("geolens_result", JSON.stringify(result));
        router.push("/audit/results");
      })
      .catch((err: Error) => {
        setError(err.message || "Audit failed. Please try again.");
      });
  }, [router]);

  if (error) {
    return (
      <main className="min-h-screen flex flex-col items-center justify-center px-6 text-center">
        <div className="max-w-md space-y-4">
          <p className="text-red-500 font-medium">{error}</p>
          <button
            onClick={() => router.push("/")}
            className="text-sm text-gray-500 underline underline-offset-2 hover:text-black"
          >
            ← Try another URL
          </button>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen flex flex-col items-center justify-center px-6">
      <div className="w-full max-w-sm space-y-10 text-center">
        <div className="space-y-1">
          <h1 className="text-xl font-semibold">Running GEO Audit</h1>
          <p className="text-sm text-gray-400">
            {auditUrl}
          </p>
        </div>

        <div className="space-y-4">
          {STEPS.map((step, i) => {
            const isDone = i < currentStep;
            const isActive = i === currentStep;

            return (
              <div key={step.label} className="flex items-center gap-3 text-left">
                {/* Icon */}
                <div className="w-6 h-6 flex items-center justify-center flex-shrink-0">
                  {isDone ? (
                    <svg className="text-black" width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <circle cx="8" cy="8" r="8" fill="black" />
                      <path d="M4.5 8l2.5 2.5 4.5-4.5" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  ) : isActive ? (
                    <div className="w-4 h-4 border-2 border-black border-t-transparent rounded-full animate-spin" />
                  ) : (
                    <div className="w-4 h-4 rounded-full border-2 border-gray-200" />
                  )}
                </div>

                {/* Label */}
                <span className={`text-sm ${isDone ? "text-black" : isActive ? "text-black font-medium" : "text-gray-300"}`}>
                  {step.label}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </main>
  );
}
