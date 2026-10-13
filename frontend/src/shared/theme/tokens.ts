/**
 * Дизайн-токены MotoBind.
 * Источник истины — tokens.scss.
 */

export const tokens = {
  colorPrimary: '#7C5CFC',
  colorPrimaryHover: '#6B4AE8',
  colorPrimaryPressed: '#5A3BD4',
  colorPrimarySuppl: '#7C5CFC',

  colorSuccess: '#18A66A',
  colorSuccessHover: '#128455',
  colorWarning: '#D88919',
  colorWarningHover: '#B56F0F',
  colorError: '#D94A4A',
  colorErrorHover: '#B93636',
  colorInfo: '#3E82D7',

  // Тёмная тема
  darkBg: '#0D1117',
  darkBgSecondary: '#111820',
  darkSurface: '#151B23',
  darkSurfaceHover: '#202832',
  darkBorder: '#2A333F',
  darkText: '#F1F3F5',
  darkTextSecondary: '#9AA5B1',
  darkTextMuted: '#6F7A87',

  // Светлая тема
  lightBg: '#F5F6F8',
  lightBgSecondary: '#EEF0F3',
  lightSurface: '#FFFFFF',
  lightSurfaceHover: '#F0F2F5',
  lightBorder: '#DDE1E7',
  lightText: '#171B21',
  lightTextSecondary: '#66707D',
  lightTextMuted: '#929BA7',

  // Радиусы
  radiusSm: '6px',
  radiusMd: '10px',
  radiusLg: '16px',

  // Шрифт
  fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif",
  fontFamilyMono: "'Courier New', ui-monospace, monospace",
} as const
