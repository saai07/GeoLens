"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function HomePage() {
  const router = useRouter();
  const [url, setUrl] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const trimmed = url.trim();
    if (!trimmed) return;

    let finalUrl = trimmed;
    if (!finalUrl.startsWith("http://") && !finalUrl.startsWith("https://")) {
      finalUrl = "https://" + finalUrl;
    }

    try {
      new URL(finalUrl);
    } catch {
      setError("Please enter a valid URL.");
      return;
    }

    setError("");
    setLoading(true);
    sessionStorage.setItem("geolens_url", finalUrl);
    router.push("/audit/loading");
  }

  function prefill() {
    setUrl("https://stripe.com");
    setError("");
  }

  return (
    <main className="min-h-screen flex flex-col items-center justify-center px-6">
      <div className="w-full max-w-2xl space-y-10 text-center">
        {/* Logo */}
        <div className="space-y-3">
          <div className="inline-flex items-center gap-2">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none" aria-hidden="true">
              <circle cx="16" cy="16" r="14" stroke="#000" strokeWidth="2" />
              <circle cx="16" cy="16" r="7" stroke="#000" strokeWidth="2" />
              <line x1="16" y1="2" x2="16" y2="30" stroke="#000" strokeWidth="2" />
              <line x1="2" y1="16" x2="30" y2="16" stroke="#000" strokeWidth="2" />
            </svg>
            <span className="text-2xl font-semibold tracking-tight">GeoLens</span>
          </div>
          <p className="text-gray-500 text-lg">See your website through an AI&apos;s eyes</p>
        </div>

        {/* Input form */}
        <form onSubmit={handleSubmit} className="space-y-3">
          <div className="flex gap-2">
            <label htmlFor="url-input" className="sr-only">Website URL</label>
            <input
              id="url-input"
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://yourwebsite.com"
              disabled={loading}
              className="flex-1 border border-gray-200 rounded-lg px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={loading}
              aria-label="Run GEO audit"
              className="bg-black text-white px-6 py-3 rounded-lg text-base font-medium hover:bg-gray-800 transition whitespace-nowrap disabled:opacity-50 flex items-center gap-2"
            >
              {loading && (
                <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
              )}
              {loading ? "Starting..." : "Run Audit"}
            </button>
          </div>

          {error && <p className="text-red-500 text-sm text-left" role="alert">{error}</p>}

          <p className="text-sm text-gray-400">
            Try an example:{" "}
            <button
              type="button"
              onClick={prefill}
              disabled={loading}
              className="text-gray-600 underline underline-offset-2 hover:text-black transition"
            >
              stripe.com
            </button>
          </p>
        </form>
      </div>
    </main>
  );
}
