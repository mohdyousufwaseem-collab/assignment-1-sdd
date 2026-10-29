import type { NutrientSummary as NutrientSummaryData } from '../../api/client';

interface NutrientSummaryProps {
  label: string;
  unit: string;
  summary: NutrientSummaryData;
  tone: 'calorie-tone' | 'protein-tone';
}

export default function NutrientSummary({ label, unit, summary, tone }: NutrientSummaryProps) {
  const progress = Number(summary.progress_percent);
  const difference = Number(summary.remaining) > 0
    ? `${summary.remaining} ${unit} remaining`
    : Number(summary.excess) > 0
      ? `${summary.excess} ${unit} over`
      : 'At target';

  return (
    <article className="nutrient-summary">
      <div className="nutrient-summary-heading">
        <strong>{label}</strong>
        <span>{summary.intake} / {summary.target} {unit}</span>
      </div>
      <div className="progress-track" role="progressbar" aria-label={`${label} progress`} aria-valuenow={progress} aria-valuemin={0} aria-valuemax={100}>
        <span className={`progress-fill ${tone}`} style={{ width: `${Math.min(progress, 100)}%` }} />
      </div>
      <div className="nutrient-summary-footer">
        <span>{difference}</span>
        <strong>{summary.progress_percent}%</strong>
      </div>
    </article>
  );
}