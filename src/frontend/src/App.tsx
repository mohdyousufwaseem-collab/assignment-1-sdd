import { useCallback, useEffect, useState } from 'react';
import { ApiRequestError, api, type DayResponse, type Meal, type MealInput } from './api/client';
import CalendarDateControl from './features/summary/CalendarDateControl';
import DailyIntake from './features/summary/DailyIntake';
import DailySummary from './features/summary/DailySummary';
import MealForm from './features/meals/MealForm';
import MealList from './features/meals/MealList';
import TargetForm from './features/targets/TargetForm';

function localToday(): string {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

export default function App() {
  const [selectedDate, setSelectedDate] = useState(localToday);
  const [day, setDay] = useState<DayResponse | null>(null);
  const [targets, setTargets] = useState<{ calories: string; protein: string } | null>(null);
  const [editingMeal, setEditingMeal] = useState<Meal | null>(null);
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [targetErrors, setTargetErrors] = useState<Record<string, string>>({});
  const [requestError, setRequestError] = useState('');
  const [notice, setNotice] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [savingTargets, setSavingTargets] = useState(false);

  const loadDay = useCallback(async (date: string) => {
    setLoading(true);
    setRequestError('');
    try {
      setDay(await api.getDay(date));
    } catch (error) {
      setRequestError(error instanceof Error ? error.message : 'The day could not be loaded.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadDay(selectedDate);
  }, [loadDay, selectedDate]);

  useEffect(() => {
    api.getTargets()
      .then(setTargets)
      .catch((error: unknown) => setRequestError(error instanceof Error ? error.message : 'Targets could not be loaded.'));
  }, []);

  async function saveMeal(values: MealInput) {
    setSaving(true);
    setRequestError('');
    setFieldErrors({});
    setNotice('');
    try {
      if (editingMeal) {
        await api.updateMeal(editingMeal.id, values);
        setNotice('Meal updated.');
      } else {
        await api.createMeal(values);
        setNotice('Meal saved.');
      }
      setEditingMeal(null);
      setSelectedDate(values.date);
      if (values.date === selectedDate) {
        await loadDay(values.date);
      }
    } catch (error) {
      if (error instanceof ApiRequestError && error.code === 'validation_failed') {
        setFieldErrors(error.fields);
        setRequestError(error.message);
      } else {
        setRequestError(error instanceof Error ? error.message : 'The meal could not be saved.');
      }
    } finally {
      setSaving(false);
    }
  }

  async function deleteMeal(meal: Meal) {
    setRequestError('');
    setNotice('');
    try {
      await api.deleteMeal(meal.id);
      setNotice('Meal deleted.');
      if (editingMeal?.id === meal.id) {
        setEditingMeal(null);
      }
      await loadDay(selectedDate);
    } catch (error) {
      setRequestError(error instanceof Error ? error.message : 'The meal could not be deleted.');
    }
  }

  async function saveTargets(values: { calories: string; protein: string }) {
    setSavingTargets(true);
    setTargetErrors({});
    setRequestError('');
    setNotice('');
    try {
      const savedTargets = await api.replaceTargets(values);
      setTargets(savedTargets);
      setNotice('Targets saved.');
      await loadDay(selectedDate);
    } catch (error) {
      if (error instanceof ApiRequestError && error.code === 'validation_failed') {
        setTargetErrors(error.fields);
        setRequestError(error.message);
      } else {
        setRequestError(error instanceof Error ? error.message : 'Targets could not be saved.');
      }
    } finally {
      setSavingTargets(false);
    }
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand-mark" aria-hidden="true">CT</div>
        <div>
          <p className="eyebrow">LOCAL FOOD DIARY</p>
          <h1>Calorie &amp; Nutrition Tracker</h1>
        </div>
        <div className="today-label">
          <span className="status-dot" />
          <span>Stored on this device</span>
        </div>
      </header>

      {requestError && <div className="notice notice-error" role="alert">{requestError}</div>}
      {notice && !requestError && <div className="notice notice-success" role="status">{notice}</div>}

      <div className="dashboard-grid">
        <section className="main-column" aria-label="Daily meal diary">
          <CalendarDateControl date={selectedDate} maxDate={localToday()} onChange={setSelectedDate} />
          <DailyIntake day={day} loading={loading} selectedDate={selectedDate} />
          <DailySummary day={day} />
          <MealList
            meals={day?.meals ?? []}
            loading={loading}
            onEdit={setEditingMeal}
            onDelete={deleteMeal}
          />
        </section>

        <aside className="form-column">
          <TargetForm targets={targets} errors={targetErrors} saving={savingTargets} onSave={saveTargets} />
          <MealForm
            selectedDate={selectedDate}
            editingMeal={editingMeal}
            fieldErrors={fieldErrors}
            saving={saving}
            onSave={saveMeal}
            onCancel={() => {
              setEditingMeal(null);
              setFieldErrors({});
            }}
          />
        </aside>
      </div>

      <footer className="app-footer">
        <span>Calorie values in kcal</span>
        <span>Protein values in grams</span>
      </footer>
    </main>
  );
}
