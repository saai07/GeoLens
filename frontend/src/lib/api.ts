import { AuditResponse } from "@/types/audit";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function runAudit(url: string): Promise<AuditResponse> {
  const res = await fetch(`${API_URL}/audit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err?.detail ?? `Audit failed (HTTP ${res.status})`);
  }

  return res.json() as Promise<AuditResponse>;
}
