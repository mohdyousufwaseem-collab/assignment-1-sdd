import type { DayResponse } from '../../api/client';

interface DailyIntakeProps {
  day: DayResponse | null;
  loading: boolean;
  selectedDate: string;
}

function NutrientTotal({ label, value, unit, tone }: { label: string; value: string; unit: string; tone: string }) {
  return (
    <div className={`intake-stat ${tone}`}>
      <span className="stat-label">{label}</span>
      <div className="stat-value">{value}<small>{unit}</small></div>
    </div>
  );
}

export default function DailyIntake({ day, loading, selectedDate }: DailyIntakeProps) {
  const formattedDate = new Intl.DateTimeFormat('en', {
    weekday: 'long', month: 'long', day: 'numeric', year: 'numeric',
    timeZone: 'UTC',
  }).format(new Date(`${selectedDate}T00:00:00Z`));

  return (
    <section className="daily-intake" aria-labelledby="daily-intake-title">
      <div className="daily-date-row">
        <div>
          <p className="eyebrow">DAILY INTAKE</p>
          <h2 id="daily-intake-title">{formattedDate}</h2>
        </div>
        <span className="date-badge">
          {loading ? 'LOADING' : day?.has_entries ? 'IN PROGRESS' : 'NO ENTRIES'}
        </span>
      </div>
      <div className="intake-stats" aria-live="polite">
        <NutrientTotal label="Calories" value={loading ? '—' : day?.summary.calories.intake ?? '0.00'} unit="kcal" tone="calorie-tone" />
        <NutrientTotal label="Protein" value={loading ? '—' : day?.summary.protein.intake ?? '0.00'} unit="g" tone="protein-tone" />
      </div>
      {!loading && day && (
        <p className="target-note">
          Current targets: {day.summary.calories.target} kcal · {day.summary.protein.target} g protein
        </p>
      )}
    </section>
  );
}