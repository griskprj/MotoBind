import { describe, expect, it, vi } from 'vitest'
import formatDate from './DateFormatter'

describe('DateFormatter', () => {
  it('returns em dash for null', () => {
    expect(formatDate(null)).toBe('—')
  })

  it('returns em dash for undefined', () => {
    expect(formatDate(undefined)).toBe('—')
  })

  it('returns em dash for empty string', () => {
    expect(formatDate('')).toBe('—')
  })

  it('returns em dash for invalid date string', () => {
    expect(formatDate('not-a-date')).toBe('—')
  })

  it('formats ISO date string', () => {
    const result = formatDate('2026-09-20')
    expect(result).toContain('20')
    expect(result).toContain('2026')
  })

  it('formats Date object', () => {
    const date = new Date(2026, 8, 20)
    const result = formatDate(date)
    expect(result).toContain('20')
    expect(result).toContain('2026')
  })

  it('returns em dash for invalid Date object', () => {
    expect(formatDate(new Date('invalid'))).toBe('—')
  })

  it('does not throw on unexpected types', () => {
    expect(() => formatDate(12345)).not.toThrow()
    expect(() => formatDate({})).not.toThrow()
    expect(() => formatDate([])).not.toThrow()
  })
})