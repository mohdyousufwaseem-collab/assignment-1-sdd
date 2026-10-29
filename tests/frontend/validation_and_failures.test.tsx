import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';

import App from '../../src/frontend/src/App';
import { ApiRequestError, api, type DayResponse } from '../../src/frontend/src/api/client';

const sampleDay: DayResponse = {
  date: '2026-10-28',
  has_entries: true,
  meals: [
    {
      id: 1,
      name: 'Toast',
      category: 'Breakfast',
      date: '2026-10-28',
      quantity: '1.00',
      calories_per_serving: '100.00',
      protein_per_serving: '4.00',
    },
  ],
  summary: {
    calories: { intake: '100.00', target: '2000.00', remaining: '1900.00', excess: '0.00', progress_percent: '5.0' },
    protein: { intake: '4.00', target: '50.00', remaining: '46.00', excess: '0.00', progress_percent: '8.0' },
  },
};

beforeEach(() => {
  vi.spyOn(api, 'getDay').mockResolvedValue(sampleDay);
  vi.spyOn(api, 'getTargets').mockResolvedValue({ calories: '2000.00', protein: '50.00' });
});

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

describe('confirmed UI state on failed writes', () => {
  it('shows field validation feedback and keeps the saved meal list', async () => {
    vi.spyOn(api, 'createMeal').mockRejectedValue(
      new ApiRequestError('One or more fields are invalid.', 422, 'validation_failed', {
        quantity: 'Must be between 0.01 and 100.00.',
      }),
    );
    render(<App />);

    expect(await screen.findByText('Toast')).toBeTruthy();
    fireEvent.change(screen.getByLabelText(/Quantity/), { target: { value: '0' } });
    fireEvent.click(screen.getByRole('button', { name: 'Add meal' }));

    expect(await screen.findByText('Must be between 0.01 and 100.00.')).toBeTruthy();
    expect(screen.getByText('Toast')).toBeTruthy();
    expect(api.getDay).toHaveBeenCalledTimes(1);
  });

  it('does not replace the displayed meal after an edit persistence failure', async () => {
    vi.spyOn(api, 'updateMeal').mockRejectedValue(
      new ApiRequestError('The change could not be saved.', 500, 'persistence_failed'),
    );
    render(<App />);

    expect(await screen.findByText('Toast')).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: 'Edit Toast' }));
    fireEvent.change(screen.getByLabelText(/Quantity/), { target: { value: '2.00' } });
    fireEvent.click(screen.getByRole('button', { name: 'Save changes' }));

    expect(await screen.findByText('The change could not be saved.')).toBeTruthy();
    expect(screen.getByText(/1\.00 servings/)).toBeTruthy();
    expect(api.getDay).toHaveBeenCalledTimes(1);
  });

  it('retains the confirmed targets after a failed target update', async () => {
    vi.spyOn(api, 'replaceTargets').mockRejectedValue(
      new ApiRequestError('The change could not be saved.', 500, 'persistence_failed'),
    );
    render(<App />);

    expect(await screen.findByText('Toast')).toBeTruthy();
    fireEvent.change(screen.getByRole('textbox', { name: /kcal \/ day/ }), { target: { value: '1800.00' } });
    fireEvent.click(screen.getByRole('button', { name: 'Save targets' }));

    expect(await screen.findByText('The change could not be saved.')).toBeTruthy();
    await waitFor(() => expect(api.getTargets).toHaveBeenCalledTimes(1));
    expect(screen.getByText('100.00 / 2000.00 kcal')).toBeTruthy();
  });
});
