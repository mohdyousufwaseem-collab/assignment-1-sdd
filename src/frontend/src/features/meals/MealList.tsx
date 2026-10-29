import type { Meal } from '../../api/client';

interface MealListProps {
  meals: Meal[];
  loading: boolean;
  onEdit: (meal: Meal) => void;
  onDelete: (meal: Meal) => Promise<void>;
}

export default function MealList({ meals, loading, onEdit, onDelete }: MealListProps) {
  return (
    <section className="meal-list-panel" aria-labelledby="meal-list-title">
      <div className="panel-heading meal-list-heading">
        <div>
          <p className="eyebrow">MEALS FOR SELECTED DATE</p>
          <h2 id="meal-list-title">Meals</h2>
        </div>
        <span className="entry-count">{loading ? 'Loading' : `${meals.length} ${meals.length === 1 ? 'entry' : 'entries'}`}</span>
      </div>
      {loading ? (
        <p className="list-message">Loading saved meals…</p>
      ) : meals.length === 0 ? (
        <div className="empty-meals">
          <span className="empty-mark" aria-hidden="true">+</span>
          <div>
            <h3>No meals recorded</h3>
            <p>Your saved meals will appear here.</p>
          </div>
        </div>
      ) : (
        <ul className="meal-list">
          {meals.map((meal) => (
            <li className="meal-row" key={meal.id}>
              <div className="meal-category-mark" aria-hidden="true">{meal.category.slice(0, 1)}</div>
              <div className="meal-description">
                <strong>{meal.name}</strong>
                <span>{meal.category} · {meal.quantity} servings</span>
              </div>
              <div className="meal-nutrition">
                <strong>{meal.calories_per_serving} kcal</strong>
                <span>{meal.protein_per_serving} g protein / serving</span>
              </div>
              <div className="meal-actions">
                <button className="text-action" type="button" onClick={() => onEdit(meal)} aria-label={`Edit ${meal.name}`}>Edit</button>
                <button className="text-action text-danger" type="button" onClick={() => void onDelete(meal)} aria-label={`Delete ${meal.name}`}>Delete</button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}