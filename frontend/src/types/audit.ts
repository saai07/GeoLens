export interface MetricResult {
  metric: string;
  score: number;
  max_score: number;
  status: "pass" | "partial" | "fail";
  detail: string;
}

export interface AuditResponse {
  url: string;
  geo_score: number;
  geo_grade: "A" | "B" | "C" | "D" | "F";
  metrics: MetricResult[];
  recommendations: string[];
  recommended_schema: Record<string, unknown>;
  page_title: string;
  page_description: string;
  page_headings: { level: string; text: string }[];
  page_image: string;
}
