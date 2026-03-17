export default function MetricCard({ title, value }: { title: string; value: number }) {
  return (
    <article className="metric-card">
      <span>{title}</span>
      <strong>{value}</strong>
    </article>
  );
}
