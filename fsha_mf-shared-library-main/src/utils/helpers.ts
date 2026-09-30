export function isEmptyValue(v: unknown): boolean {
  return (
    v === null || v === undefined || v === 'null' || (typeof v === 'string' && v.trim() === '')
  );
}
