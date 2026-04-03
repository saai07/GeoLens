"use client";

import { useState } from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/cjs/styles/prism";
import { AuditResponse } from "@/types/audit";

export default function JsonLdViewer({ data }: { data: AuditResponse }) {
  const [copied, setCopied] = useState(false);
  const json = JSON.stringify(data.recommended_schema, null, 2);

  function handleCopy() {
    navigator.clipboard.writeText(json).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  }

  return (
    <section className="space-y-3">
      <div className="flex items-center justify-between">
        <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider">
          Recommended JSON-LD Schema
        </h2>
        <button
          onClick={handleCopy}
          aria-label="Copy JSON-LD to clipboard"
          className="text-xs border border-gray-200 px-3 py-1.5 rounded-lg hover:bg-gray-50 transition text-gray-600"
        >
          {copied ? "Copied!" : "Copy"}
        </button>
      </div>

      <div className="rounded-xl overflow-hidden border border-gray-800 text-sm">
        <SyntaxHighlighter
          language="json"
          style={oneDark}
          customStyle={{ margin: 0, padding: "1.25rem", fontSize: "0.8rem", lineHeight: "1.6" }}
        >
          {json}
        </SyntaxHighlighter>
      </div>

      <p className="text-xs text-gray-400">
        Paste this inside a{" "}
        <code className="bg-gray-100 px-1 py-0.5 rounded text-gray-600">
          {"<script type=\"application/ld+json\">"}
        </code>{" "}
        tag in your page&apos;s <code className="bg-gray-100 px-1 py-0.5 rounded text-gray-600">&lt;head&gt;</code>.
      </p>
    </section>
  );
}
