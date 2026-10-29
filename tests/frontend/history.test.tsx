import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';

import App from '../../src/frontend/src/App';
import { api, type DayResponse } from '../../src/frontend/src/api/client';

function localDate(offset = 0): string {
  const date = new Date();
  date.setDate(date.getDate() + offset);
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
}

function emptyDay(date: string): DayResponse {
  return {
    date,
    has_entries: false,
    meals: [],
    summary: {
      calories: { intake: '0.00', target: '2000.00', remaining: '2000.00', excess: '0.00', progress_percent: '0.0' },
      protein: { intake: '0.00', target: '50.00', remaining: '50.00', excess: '0.00', progress_percent: '0.0' },
    },
  };
}

beforeEach(() => {
  vi.spyOn(api, 'getDay').mockImplementation(async (date) => emptyDay(date));
  vi.spyOn(api, 'getTargets').mockResolvedValue({ calories: '2000.00', protein: '50.00' });
});

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

describe('historical date selection', () => {
  it('defaults to today and prevents selecting a future date', async () => {
    render(<App />);
    const control = await screen.findByLabelText('View date');

    expect((control as HTMLInputElement).value).toBe(localDate());
    expect((control as HTMLInputElement).max).toBe(localDate());
  });

  it('loads only the selected previous date and renders its empty state', async () => {
    render(<App />);
    const previousDate = localDate(-1);
    const control = await screen.findByLabelText('View date');
    fireEvent.change(control, { target: { value: previousDate } });

    await waitFor(() => expect(api.getDay).toHaveBeenLastCalledWith(previousDate));
    expect(await screen.findByText('No meals recorded')).toBeTruthy();
    expect(screen.getByText('0.00 / 2000.00 kcal')).toBeTruthy();
    expect(screen.getByText('0.00 / 50.00 g')).toBeTruthy();
  });
});
