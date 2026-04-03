export default function Skeleton({ className = "" }: { className?: string }) {
  return (
    <div
      className={`animate-pulse bg-gray-100 rounded-lg ${className}`}
      role="status"
      aria-label="Loading"
    />
  );
}
