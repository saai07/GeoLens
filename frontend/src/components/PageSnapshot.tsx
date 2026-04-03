import { AuditResponse } from "@/types/audit";

const LEVEL_STYLES: Record<string, string> = {
  h1: "font-semibold text-gray-900",
  h2: "font-medium text-gray-700 pl-3",
  h3: "text-gray-500 pl-6",
};

export default function PageSnapshot({ data }: { data: AuditResponse }) {
  const { page_title, page_description, page_headings, url } = data;

  return (
    <section className="space-y-3">
      <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider">
        Page Snapshot
      </h2>
      <div className="border border-gray-100 rounded-xl p-5 space-y-4">
        {/* URL */}
        <div className="space-y-1">
          <p className="text-xs text-gray-400 uppercase tracking-wider">Audited URL</p>
          <p className="text-sm text-blue-600 truncate">{url}</p>
        </div>

        {/* Title */}
        {page_title && (
          <div className="space-y-1">
            <p className="text-xs text-gray-400 uppercase tracking-wider">Page Title</p>
            <p className="text-sm text-gray-900">{page_title}</p>
          </div>
        )}

        {/* Meta description */}
        {page_description && (
          <div className="space-y-1">
            <p className="text-xs text-gray-400 uppercase tracking-wider">Meta Description</p>
            <p className="text-sm text-gray-600 leading-relaxed">{page_description}</p>
          </div>
        )}

        {/* Headings */}
        {page_headings.length > 0 && (
          <div className="space-y-1">
            <p className="text-xs text-gray-400 uppercase tracking-wider">
              Heading Structure ({page_headings.length} headings)
            </p>
            <div className="space-y-1 max-h-48 overflow-y-auto pr-1">
              {page_headings.slice(0, 20).map((h, i) => (
                <p key={i} className={`text-sm ${LEVEL_STYLES[h.level] ?? "text-gray-500 pl-6"}`}>
                  <span className="text-xs text-gray-300 mr-2 font-mono">{h.level.toUpperCase()}</span>
                  {h.text}
                </p>
              ))}
              {page_headings.length > 20 && (
                <p className="text-xs text-gray-300 pl-3">+{page_headings.length - 20} more…</p>
              )}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
