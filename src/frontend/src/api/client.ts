export type MealCategory = 'Breakfast' | 'Lunch' | 'Dinner' | 'Snack';

export interface MealInput {
  name: string;
  category: MealCategory;
  date: string;
  quantity: string;
  calories_per_serving: string;
  protein_per_serving: string;
}

export interface Meal extends MealInput {
  id: number;
}

export interface TargetsInput {
  calories: string;
  protein: string;
}

export type Targets = TargetsInput;

export interface NutrientSummary {
  intake: string;
  target: string;
  remaining: string;
  excess: string;
  progress_percent: string;
}

export interface DayResponse {
  date: string;
  has_entries: boolean;
  meals: Meal[];
  summary: {
    calories: NutrientSummary;
    protein: NutrientSummary;
  };
}

interface ErrorPayload {
  error?: {
    code?: string;
    message?: string;
    fields?: Record<string, string>;
  };
}

export class ApiRequestError extends Error {
  constructor(
    message: string,
    readonly status: number,
    readonly code: string,
    readonly fields: Record<string, string> = {},
  ) {
    super(message);
    this.name = 'ApiRequestError';
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(path, {
      ...init,
      headers: {
        ...(init?.body ? { 'Content-Type': 'application/json' } : {}),
        ...init?.headers,
      },
    });
  } catch {
    throw new ApiRequestError('The local service could not be reached.', 0, 'unavailable');
  }

  if (!response.ok) {
    const payload = (await response.json().catch(() => ({}))) as ErrorPayload;
    throw new ApiRequestError(
      payload.error?.message ?? 'The request could not be completed.',
      response.status,
      payload.error?.code ?? 'request_failed',
      payload.error?.fields ?? {},
    );
  }

  if (response.status === 204) {
    return undefined as T;
  }
  return (await response.json()) as T;
}

export const api = {
  getDay: (date: string) => request<DayResponse>(`/api/days/${encodeURIComponent(date)}`),
  createMeal: (meal: MealInput) =>
    request<Meal>('/api/meals', { method: 'POST', body: JSON.stringify(meal) }),
  updateMeal: (id: number, meal: MealInput) =>
    request<Meal>(`/api/meals/${id}`, { method: 'PUT', body: JSON.stringify(meal) }),
  deleteMeal: (id: number) => request<void>(`/api/meals/${id}`, { method: 'DELETE' }),
  getTargets: () => request<Targets>('/api/targets'),
  replaceTargets: (targets: TargetsInput) =>
    request<Targets>('/api/targets', { method: 'PUT', body: JSON.stringify(targets) }),
};