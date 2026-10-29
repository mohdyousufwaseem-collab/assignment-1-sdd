import { useEffect, useState, type FormEvent } from 'react';
import type { Meal, MealCategory, MealInput } from '../../api/client';

interface MealFormProps {
  selectedDate: string;
  editingMeal: Meal | null;
  fieldErrors: Record<string, string>;
  saving: boolean;
  onSave: (meal: MealInput) => Promise<void>;
  onCancel: () => void;
}

const categories: MealCategory[] = ['Breakfast', 'Lunch', 'Dinner', 'Snack'];

function defaultValues(date: string): MealInput {
  return {
    name: '',
    category: 'Breakfast',
    date,
    quantity: '1.00',
    calories_per_serving: '',
    protein_per_serving: '',
  };
}

export default function MealForm({
  selectedDate,
  editingMeal,
  fieldErrors,
  saving,
  onSave,
  onCancel,
}: MealFormProps) {
  const [values, setValues] = useState<MealInput>(() => defaultValues(selectedDate));

  useEffect(() => {
    if (editingMeal) {
      setValues({
        name: editingMeal.name,
        category: editingMeal.category,
        date: editingMeal.date,
        quantity: editingMeal.quantity,
        calories_per_serving: editingMeal.calories_per_serving,
        protein_per_serving: editingMeal.protein_per_serving,
      });
    } else {
      setValues(defaultValues(selectedDate));
    }
  }, [editingMeal, selectedDate]);

  function update<K extends keyof MealInput>(field: K, value: MealInput[K]) {
    setValues((current) => ({ ...current, [field]: value }));
  }

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    void onSave(values);
  }

  return (
    <section className="meal-form-panel" aria-labelledby="meal-form-title">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">MEAL ENTRY</p>
          <h2 id="meal-form-title">{editingMeal ? 'Edit meal' : 'Add a meal'}</h2>
        </div>
        <span className="form-step">01 / 01</span>
      </div>

      <form className="meal-form" onSubmit={submit} noValidate>
        <label className="field field-wide">
          <span>Food name</span>
          <input
            autoComplete="off"
            maxLength={120}
            required
            value={values.name}
            onChange={(event) => update('name', event.target.value)}
            aria-invalid={Boolean(fieldErrors.name)}
            aria-describedby={fieldErrors.name ? 'meal-name-error' : undefined}
            placeholder="e.g. Oatmeal with berries"
          />
          {fieldErrors.name && <small className="field-error" id="meal-name-error">{fieldErrors.name}</small>}
        </label>

        <label className="field">
          <span>Meal</span>
          <select required value={values.category} onChange={(event) => update('category', event.target.value as MealCategory)}>
            {categories.map((category) => <option key={category}>{category}</option>)}
          </select>
          {fieldErrors.category && <small className="field-error">{fieldErrors.category}</small>}
        </label>

        <label className="field">
          <span>Date</span>
          <input
            type="date"
            required
            value={values.date}
            onChange={(event) => update('date', event.target.value)}
            aria-invalid={Boolean(fieldErrors.date)}
          />
          {fieldErrors.date && <small className="field-error">{fieldErrors.date}</small>}
        </label>

        <label className="field">
          <span>Quantity <em>servings</em></span>
          <input
            inputMode="decimal"
            required
            value={values.quantity}
            onChange={(event) => update('quantity', event.target.value)}
            aria-invalid={Boolean(fieldErrors.quantity)}
          />
          {fieldErrors.quantity && <small className="field-error">{fieldErrors.quantity}</small>}
        </label>

        <label className="field">
          <span>Calories <em>kcal / serving</em></span>
          <input
            inputMode="decimal"
            required
            value={values.calories_per_serving}
            onChange={(event) => update('calories_per_serving', event.target.value)}
            aria-invalid={Boolean(fieldErrors.calories_per_serving)}
          />
          {fieldErrors.calories_per_serving && <small className="field-error">{fieldErrors.calories_per_serving}</small>}
        </label>

        <label className="field field-wide">
          <span>Protein <em>g / serving</em></span>
          <input
            inputMode="decimal"
            required
            value={values.protein_per_serving}
            onChange={(event) => update('protein_per_serving', event.target.value)}
            aria-invalid={Boolean(fieldErrors.protein_per_serving)}
          />
          {fieldErrors.protein_per_serving && <small className="field-error">{fieldErrors.protein_per_serving}</small>}
        </label>

        <div className="form-actions field-wide">
          <button className="button button-primary" type="submit" disabled={saving}>
            {saving ? 'Saving…' : editingMeal ? 'Save changes' : 'Add meal'}
          </button>
          {editingMeal && <button className="button button-quiet" type="button" onClick={onCancel}>Cancel</button>}
        </div>
      </form>
    </section>
  );
}