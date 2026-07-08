// Design.MD White Label — Tokens JavaScript
// Generado automáticamente desde component-manifest.json
// Uso: import { tokens } from './tokens.js'

export const semanticTokens = {
  space_1: '4px', // Separación mínima icono-texto
  space_2: '8px', // Interno compacto
  space_3: '12px', // Interno de controles
  space_4: '16px', // Padding estándar
  space_5: '24px', // Entre bloques
  space_6: '32px', // Entre secciones
  radius_sm: '6px', // Badges, inputs pequeños
  radius_md: '10px', // Botones, inputs
  radius_lg: '16px', // Tarjetas, modales
  radius_pill: '999px', // Pills, avatares
  motion_fast: '120ms', // Hover, focus
  motion_base: '240ms', // Aparición, expansión
};

export const brandTokens = {
  "promptea": {
    "dark": {
      "bg": "#0B0E11",
      "surface": "#14181D",
      "text": "#E8ECF1",
      "muted": "#9AA5B1",
      "action": "#7CE83A",
      "on-action": "#0B0E11",
      "focus": "#7CE83A",
      "danger": "#F87171",
      "success": "#4ADE80",
      "border": "#2A3138"
    },
    "light": {
      "bg": "#FFFFFF",
      "surface": "#F4F6F8",
      "text": "#1A2027",
      "muted": "#5A6572",
      "action": "#2E7D0F",
      "on-action": "#FFFFFF",
      "focus": "#2E7D0F",
      "danger": "#B91C1C",
      "success": "#15803D",
      "border": "#D7DDE3"
    }
  },
  "nova": {
    "dark": {
      "bg": "#0D0B14",
      "surface": "#171322",
      "text": "#ECE9F4",
      "muted": "#A49DB8",
      "action": "#A78BFA",
      "on-action": "#0D0B14",
      "focus": "#A78BFA",
      "danger": "#F87171",
      "success": "#4ADE80",
      "border": "#2E2840"
    },
    "light": {
      "bg": "#FFFFFF",
      "surface": "#F6F4FB",
      "text": "#1D1830",
      "muted": "#5D5674",
      "action": "#6D28D9",
      "on-action": "#FFFFFF",
      "focus": "#6D28D9",
      "danger": "#B91C1C",
      "success": "#15803D",
      "border": "#DDD8EA"
    }
  },
  "ocean": {
    "dark": {
      "bg": "#081018",
      "surface": "#0F1B26",
      "text": "#E6EEF5",
      "muted": "#8FA3B5",
      "action": "#38BDF8",
      "on-action": "#081018",
      "focus": "#38BDF8",
      "danger": "#F87171",
      "success": "#4ADE80",
      "border": "#22323F"
    },
    "light": {
      "bg": "#FFFFFF",
      "surface": "#F2F7FB",
      "text": "#122130",
      "muted": "#4E6478",
      "action": "#0369A1",
      "on-action": "#FFFFFF",
      "focus": "#0369A1",
      "danger": "#B91C1C",
      "success": "#15803D",
      "border": "#D3E0EA"
    }
  }
};

export default {
  semantic: semanticTokens,
  brands: brandTokens,
};
