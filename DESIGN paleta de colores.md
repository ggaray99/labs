---
name: consulte. — Visual Identity System v1.0
domain: consulte.app
core:
  cobalt: '#0047AB'        # primario, ancla del sistema
  cobalt-dark: '#00327D'   # hover, pressed
  ink: '#0B1C30'           # texto principal, Deep Slate
  paper: '#FFFFFF'         # base
  bg-tint: '#F8F9FF'       # Mist, superficie sutil
  sky: '#4DA3FF'           # info, datos
cobalt-ramp:
  '50':  '#F2F5FC'
  '100': '#DCE5F4'
  '200': '#A8C0E8'
  '300': '#5E8DD6'
  '400': '#2E6BC4'
  '500': '#0047AB'         # ★ marca
  '600': '#00327D'
  '700': '#001F4F'
  '800': '#00112D'
slate-ramp:
  '50':  '#F4F6FA'
  '100': '#E5E9F0'
  '200': '#CBD2DD'
  '300': '#A2AEBE'
  '400': '#6F7E92'
  '500': '#4A5A6E'
  '600': '#324358'
  '700': '#1F3147'
  '900': '#0B1C30'         # ★ ink
status:
  success: '#1E9E63'
  warning: '#D68419'
  error:   '#C8362F'
  info:    '#4DA3FF'
vertical-tints:
  salud:     '#5BB89A'     # Mint sereno
  legal:     '#3D4F8F'     # Indigo profundo
  contable:  '#8C7344'     # Bronce mate
  coaching:  '#D88061'     # Coral cálido
  creativos: '#7D5E94'     # Plum editorial
  bienestar: '#8A9F7E'     # Sage tierra
typography:
  display:
    fontFamily: Manrope
    fontWeight: '600'
    fontSize: 84px
    lineHeight: 82px
    letterSpacing: -0.035em
  h1:
    fontFamily: Manrope
    fontWeight: '500'
    fontSize: 56px
    lineHeight: 60px
    letterSpacing: -0.02em
  h2:
    fontFamily: Manrope
    fontWeight: '500'
    fontSize: 40px
    lineHeight: 44px
    letterSpacing: -0.015em
  h3:
    fontFamily: Manrope
    fontWeight: '500'
    fontSize: 28px
    lineHeight: 34px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Manrope
    fontWeight: '400'
    fontSize: 20px
    lineHeight: 30px
    letterSpacing: '0'
  body-md:
    fontFamily: Manrope
    fontWeight: '400'
    fontSize: 16px
    lineHeight: 25px
    letterSpacing: '0'
  body-sm:
    fontFamily: Manrope
    fontWeight: '400'
    fontSize: 14px
    lineHeight: 21px
    letterSpacing: '0'
  label:
    fontFamily: JetBrains Mono
    fontWeight: '500'
    fontSize: 13px
    lineHeight: 16px
    letterSpacing: 0.14em
    case: UPPERCASE
  code:
    fontFamily: JetBrains Mono
    fontWeight: '400'
    fontSize: 14px
    lineHeight: 22px
    letterSpacing: '0'
rounded:
  '4': 0.25rem   # inputs, labels, swatches
  '6': 0.375rem  # botones, cards chicos
  '8': 0.5rem    # cards mayores
  '12': 0.75rem  # mockups, contenedores
  full: 9999px   # avatars
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
shadows:
  card-float: '0 30px 80px -40px rgba(11,28,48,.25)'
  next-slot:  '0 4px 18px -10px rgba(0,71,171,.25)'
---

## Brand & Style
Identidad visual completa de **consulte.** (`consulte.app`), SaaS horizontal para profesionales independientes que vende landing pública + agenda online + onboarding rápido en un solo lugar.

La personalidad es "Professional Clarity meets High-Tech Precision": confianza institucional + velocidad de SaaS moderno. Sereno, eficiente, técnicamente impecable, con calidez justa para no sentirse frío. El sistema funciona pareja para salud, legal, contable, coaching, consultoría y creativos — la identidad core NO se lee gremial.

## Logo
- **Glyph** (canónico): marco cobalto 68×68 con segmento horizontal interior. Master en `core/static/brand/logo.svg`.
- **Variante sólida** (favicon ≤32px, avatar): rect fill cobalto + corte horizontal blanco. `core/static/brand/logo-solid.svg`.
- **Wordmark:** `consulte.` lowercase, Manrope **600**, letter-spacing **-0.045em**.
  - Palabra en `--cobalt` (`#0047AB`).
  - Punto final en `--ink` (`#0B1C30`) — nodo separado para teñirlo distinto.
- **Lockup horizontal:** partial reutilizable en `templates/core/_brand_lockup.html`. Acepta `iso_size`, `text_size` y `invert`.
- **Clearspace** = mitad de la altura del isotipo. **Min** lockup horizontal: 80px. **Min** isotipo outline: 20px. **Min** favicon sólido: 16px.

## Colors
- **Cobalto es la marca.** Nunca lo abandones en el producto base, dashboard, emails ni favicon.
- **Vertical tints (`vertical-tints`)** son **opt-in** y aplican únicamente al accent de la landing pública del profesional (`/p/{slug}`): CTA de booking, hover de slot, badge de modalidad. NO al producto.
- **Surfaces:** `--paper` (`#FFFFFF`) base, `--bg-tint` (`#F8F9FF`) para diferenciar secciones, `--slate-50` (`#F4F6FA`) para niveles más profundos. Depth por tonal layering, no por sombras pesadas.
- **Estados** (`status`) tienen tinte propio + contraparte light para fondos: success usa verde `#1E9E63` con fondo `#E6F4EC`, etc.

## Typography
**Manrope** (todo el sistema) + **JetBrains Mono** (labels uppercase, timestamps, IDs, código). Único pairing aprobado — sin serifs ni display fonts adicionales.

- Labels con `font-family: 'JetBrains Mono'`, `font-weight: 500`, `text-transform: uppercase`, `letter-spacing: 0.14em`.
- Headlines con tracking negativo (`-0.035em` display, `-0.02em` h1) y weight 500-600.
- Body 400, line-height generoso (1.5-1.6).

Carga en `templates/base.html`:
```html
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@200;300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

## Spacing, geometry & elevation
- **Border radius:** 4px (inputs, labels, swatches), 6px (botones, cards chicos), 8px (cards mayores), 12px (mockups, contenedores), 50% (avatars).
- **Borders:** 1px sólido `--slate-100` por defecto. Acento: borde izquierdo 3px de color (`cobalt`, estado o vertical-tint) sobre fondo claro.
- **Sombras:** minimal. Card flotante destacada `--shadow-card-float`. Próximo turno `--shadow-next-slot`. No usar sombras dramáticas.
- **Depth** por tonal layering: `#FFFFFF` → `#F8F9FF` → `#F4F6FA`. O glassmorphism muy sutil (95% opacidad, 12px backdrop blur) para dropdowns/modales.

## Components
- **Botón primario:** fondo `--cobalt`, texto blanco, radius 6px. Hover → `--cobalt-dark`.
- **Botón outline:** transparent + border 1px `--slate-200`. Hover → bg `--slate-50`, border `--slate-300`.
- **Inputs:** fondo `--slate-50`, border 1px `--slate-200`, radius 4px. Focus → border `--cobalt` + ring 2px `--cobalt-50`.
- **Chips/badges:** uppercase, JetBrains Mono 500, fondo tinte sutil del estado.
- **Cards:** fondo blanco, border 1px `--slate-100`, sin sombra salvo hover/destacado.
- **Slots de booking:** radius 6px. Hover → fondo `--cobalt-50`, border `--cobalt`. Activo → fondo del color (cobalto o vertical-tint), texto blanco, weight 600.

## Usos prohibidos del logo
- No rotar ni deformar proporciones.
- No aplicar gradientes ni colores fuera del sistema.
- No agregar sombras u outlines.
- No usar sobre fondos saturados o de bajo contraste.
- No sustituir el wordmark ni capitalizar — siempre lowercase, incluyendo el dominio.
- No usar outline en favicons ≤32px (usar variante sólida).
