interface CalendarDateControlProps {
  date: string;
  maxDate: string;
  onChange: (date: string) => void;
}

export default function CalendarDateControl({ date, maxDate, onChange }: CalendarDateControlProps) {
  return (
    <label className="date-control">
      <span>View date</span>
      <input
        aria-label="View date"
        type="date"
        value={date}
        max={maxDate}
        onChange={(event) => onChange(event.target.value)}
      />
    </label>
  );
}
