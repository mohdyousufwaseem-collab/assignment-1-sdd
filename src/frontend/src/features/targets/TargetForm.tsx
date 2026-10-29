import { useEffect, useState, type FormEvent } from 'react';
import type { Targets } from '../../api/client';

interface TargetFormProps {
  targets: Targets | null;
  errors: Record<string, string>;
  saving: boolean;
  onSave: (targets: Targets) => Promise<void>;
}

export default function TargetForm({ targets, errors, saving, onSave }: TargetFormProps) {
  const [values, setValues] = useState<Targets>({ calories: '2000.00', protein: '50.00' });

  useEffect(() => {
    if (targets) setValues(targets);
  }, [targets]);

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    void onSave(values);
  }

  return (
    <section className="target-form-panel" aria-labelledby="target-form-title">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">DAILY GOALS</p>
          <h2 id="target-form-title">Targets</h2>
        </div>
      </div>
      <form className="target-form" onSubmit={submit}>
        <label className="field">
          <span>Calories <em>kcal / day</em></span>
          <input
            inputMode="decimal"
            required
            value={values.calories}
            onChange={(event) => setValues((current) => ({ ...current, calories: event.target.value }))}
            aria-invalid={Boolean(errors.calories)}
          />
          {errors.calories && <small className="field-error">{errors.calories}</small>}
        </label>
        <label className="field">
          <span>Protein <em>g / day</em></span>
          <input
            inputMode="decimal"
            required
            value={values.protein}
            onChange={(event) => setValues((current) => ({ ...current, protein: event.target.value }))}
            aria-invalid={Boolean(errors.protein)}
          />
          {errors.protein && <small className="field-error">{errors.protein}</small>}
        </label>
        <button className="button button-secondary" type="submit" disabled={saving}>
          {saving ? 'Saving…' : 'Save targets'}
        </button>
      </form>
      <p className="target-disclaimer">Generic defaults are not personalized nutrition advice.</p>
    </section>
  );
}