import type { DayResponse } from '../../api/client';
import NutrientSummary from './NutrientSummary';

interface DailySummaryProps {
  day: DayResponse | null;
}

export default function DailySummary({ day }: DailySummaryProps) {
  if (!day) return null;
  return (
    <section className="daily-summary" aria-label="Target progress">
      <NutrientSummary label="Calories" unit="kcal" summary={day.summary.calories} tone="calorie-tone" />
      <NutrientSummary label="Protein" unit="g" summary={day.summary.protein} tone="protein-tone" />
    </section>
  );
}