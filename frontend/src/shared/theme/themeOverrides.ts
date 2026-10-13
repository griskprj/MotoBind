import type { GlobalThemeOverrides } from 'naive-ui'
import { tokens } from './tokens'

export const themeOverrides: GlobalThemeOverrides = {
  common: {
    primaryColor: tokens.colorPrimary,
    primaryColorHover: tokens.colorPrimaryHover,
    primaryColorPressed: tokens.colorPrimaryPressed,
    primaryColorSuppl: tokens.colorPrimarySuppl,

    successColor: tokens.colorSuccess,
    successColorHover: tokens.colorSuccessHover,
    warningColor: tokens.colorWarning,
    warningColorHover: tokens.colorWarningHover,
    errorColor: tokens.colorError,
    errorColorHover: tokens.colorErrorHover,
    infoColor: tokens.colorInfo,

    borderRadius: tokens.radiusMd,
    borderRadiusSmall: tokens.radiusSm,

    fontFamily: tokens.fontFamily,
    fontFamilyMono: tokens.fontFamilyMono,
  },

  Card: {
    borderRadius: tokens.radiusLg,
  },

  Button: {
    borderRadiusMedium: tokens.radiusMd,
  },

  Input: {
    borderRadius: tokens.radiusMd,
    boxShadowFocus: 'none',
    borderFocus: `1px solid ${tokens.colorPrimary}`,
    borderHover: `1px solid ${tokens.colorPrimaryHover}`,
  },
}

export const darkThemeOverrides: GlobalThemeOverrides = {
  common: {
    bodyColor: tokens.darkBg,
    cardColor: tokens.darkSurface,
    modalColor: tokens.darkSurface,
    popoverColor: tokens.darkSurface,
    tableColor: tokens.darkSurface,
    inputColor: tokens.darkBgSecondary,

    borderColor: tokens.darkBorder,
    dividerColor: tokens.darkBorder,

    textColorBase: tokens.darkText,
    textColor1: tokens.darkText,
    textColor2: tokens.darkTextSecondary,
    textColor3: tokens.darkTextMuted,

    hoverColor: tokens.darkSurfaceHover,
  },
}
