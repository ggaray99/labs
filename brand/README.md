# Handoff: Consulte — Visual Identity System v1.0

## Overview
Sistema de identidad visual completo para **Consulte** (dominio: `consulte.app`), SaaS horizontal para profesionales independientes que combina landing pública, agenda online y onboarding rápido en una sola plataforma.

El paquete cubre logotipo, paleta, tipografía, iconografía abstracta para verticales, y 8 aplicaciones (landing pública, landing del profesional `/p/{slug}`, dashboard, email transaccional, OG image, avatar/favicon, tarjeta digital y social share).

## About the Design Files
Los archivos de este bundle son **referencias de diseño construidas en HTML** — prototipos que muestran la apariencia e intención de la marca, no código de producción para copiar directamente.

La tarea es **recrear estas vistas en el entorno de tu codebase** (Next.js, Astro, Remix, SwiftUI, etc.) usando sus patrones establecidos. Si no hay codebase aún, elegir el framework más adecuado al producto e implementar ahí. Los SVGs del logotipo, glifos y mockups pueden extraerse directamente del HTML como referencia exacta.

## Fidelity
**High-fidelity (hifi).** Todos los valores — colores, tipografías, tamaños, spacing, border-radius — están definidos exactamente. Recreá pixel-perfect.

## Files
- `Brand Book.html` — Brand book navegable de 24 slides (1920×1080). Abrir en el navegador, navegar con flechas.
- `deck-stage.js` — Web component que da scaling/navegación al brand book. No es entregable de producto.

---

## Logo System

### Dirección recomendada: **Glyph (#5)**
Marco cobalto cuadrado con segmento horizontal interior. Universal para todos los verticales. Master SVG:

```svg
<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
  <rect x="6" y="6" width="68" height="68" rx="8" fill="none" stroke="#0047AB" stroke-width="10"/>
  <rect x="22" y="36" width="36" height="8" fill="#0047AB"/>
</svg>
```

Variante sólida (para favicon ≤32px y avatar):
```svg
<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
  <rect x="6" y="6" width="68" height="68" rx="8" fill="#0047AB"/>
  <rect x="22" y="36" width="36" height="8" fill="#fff"/>
</svg>
```

### Wordmark
- Family: **Manrope** (Google Fonts)
- Weight: **600** (SemiBold)
- Letter-spacing: **-0.045em**
- Case: **lowercase**, siempre
- Final period: `.` en color **Deep Slate `#0B1C30`** (mientras la palabra es Cobalt `#0047AB`)
- Markup: `<span>consulte<span class="dot">.</span></span>` — el punto es un nodo separado para teñirlo distinto

### Lockups (6 oficiales)
| # | Lockup | Uso |
|---|---|---|
| 01 | Horizontal | Default. Header, footer, firmas. Iso 80×80 + wordmark a la derecha, gap 18px. |
| 02 | Vertical | Tarjeta, packaging. Iso 100×100, wordmark debajo. |
| 03 | Isotipo solo | Avatar, favicon, app icon. |
| 04 | Monocromo negro | 1 tinta, documentos legales. `#0B1C30`. |
| 05 | Invertido sobre cobalto | OG, hero, redes. Stroke `#fff`. |
| 06 | Favicon sólido | 16/32/64px. Sin outline, fondo cobalto pleno con corte interior blanco. |

### Clearspace y tamaños mínimos
- **Clearspace** = `x/2` donde `x` = altura del isotipo
- Min lockup horizontal: **80px** de ancho
- Min isotipo (outline): **20px**
- Min favicon (sólido): **16px**

### Usos prohibidos
- No rotar
- No deformar proporciones
- No aplicar gradientes ni colores fuera del sistema
- No agregar sombras u outlines
- No sobre fondos saturados o de bajo contraste
- No sustituir el wordmark ni capitalizar

---

## Design Tokens

### Colors

#### Core
```css
--cobalt:        #0047AB;  /* primario, ancla del sistema */
--cobalt-dark:   #00327D;  /* hover, pressed */
--ink:           #0B1C30;  /* texto principal, Deep Slate */
--paper:         #FFFFFF;  /* base */
--bg-tint:       #F8F9FF;  /* Mist, superficie sutil */
--sky:           #4DA3FF;  /* info, datos */
```

#### Cobalt ramp
```css
--cobalt-50:  #F2F5FC;
--cobalt-100: #DCE5F4;
--cobalt-200: #A8C0E8;
--cobalt-300: #5E8DD6;
--cobalt-400: #2E6BC4;
--cobalt-500: #0047AB;  /* ★ marca */
--cobalt-600: #00327D;
--cobalt-700: #001F4F;
--cobalt-800: #00112D;
```

#### Slate ramp (neutrales)
```css
--slate-50:  #F4F6FA;
--slate-100: #E5E9F0;
--slate-200: #CBD2DD;
--slate-300: #A2AEBE;
--slate-400: #6F7E92;
--slate-500: #4A5A6E;
--slate-600: #324358;
--slate-700: #1F3147;
--slate-900: #0B1C30;  /* ★ ink */
```

#### Estados semánticos
```css
--success: #1E9E63;
--warning: #D68419;
--error:   #C8362F;
--info:    #4DA3FF;
```

#### Vertical tints (opt-in, solo en `/p/{slug}`)
```css
--v-salud:     #5BB89A;  /* Mint sereno */
--v-legal:     #3D4F8F;  /* Indigo profundo */
--v-contable:  #8C7344;  /* Bronce mate */
--v-coaching:  #D88061;  /* Coral cálido */
--v-creativos: #7D5E94;  /* Plum editorial */
--v-bienestar: #8A9F7E;  /* Sage tierra */
```

**Regla crítica:** Los tints son **opt-in** y aplican únicamente al accent de la landing pública del profesional (CTA de booking, hover de slot, badge de modalidad). El producto, dashboard, emails y favicon siempre son cobalto.

---

### Typography

#### Familias
- **Manrope** (Google Fonts, pesos 200/300/400/500/600/700/800) — todo
- **JetBrains Mono** (Google Fonts, pesos 400/500/600) — datos, IDs, timestamps, labels uppercase, código

#### Escala
| Token | Family | Weight | Size | Line | Tracking | Uso |
|---|---|---|---|---|---|---|
| `display` | Manrope | 600 | 84px | 82px | -0.035em | Hero, slides cover |
| `h1` | Manrope | 500 | 56px | 60px | -0.020em | Página, hero secundario |
| `h2` | Manrope | 500 | 40px | 44px | -0.015em | Sección |
| `h3` | Manrope | 500 | 28px | 34px | -0.010em | Subsección, card title |
| `body-lg` | Manrope | 400 | 20px | 30px | 0 | Hero subhead, bajadas |
| `body-md` | Manrope | 400 | 16px | 25px | 0 | Texto corrido |
| `body-sm` | Manrope | 400 | 14px | 21px | 0 | Caption, helper |
| `label` | JetBrains Mono | 500 | 13px | 16px | 0.14em + UPPER | Eyebrows, metadata |
| `code` | JetBrains Mono | 400 | 14px | 22px | 0 | Timestamps, IDs |

---

### Spacing & geometry
- **Border radius**: 4px (inputs, labels, swatches), 6px (botones, cards chicos), 8px (cards mayores), 12px (mockups, contenedores), 50% (avatars).
- **Borders**: 1px sólido. Color por defecto `--slate-100`. Acento: borde izquierdo 3px de color (`cobalt`, estado o tint vertical) sobre fondo claro.
- **Sombras**: minimal. La única recurrente: `0 30px 80px -40px rgba(11,28,48,.25)` para cards flotantes destacadas. Para próximo turno: `0 4px 18px -10px rgba(0,71,171,.25)`. No usar sombras dramáticas.
- **Depth**: por tonal layering (`#FFFFFF` → `#F8F9FF` → `#F4F6FA`) o glassmorphism muy sutil, no por sombras pesadas.

---

## Screens / Views

Cada slide del brand book corresponde a una pantalla o aplicación. Referenciar el archivo HTML para extraer SVGs, copy exacto y medidas.

### 1. Landing pública — `consulte.app`
**Slide 17 del brand book**

- **Header**: padding 20px 56px, border-bottom 1px `--slate-100`. Logo lockup horizontal (iso 28×28 + wordmark 22px), nav (`Producto · Para quién · Precios · Recursos`), `Iniciar sesión` en `--slate-700`, CTA `Empezar gratis` en cobalto.
- **Hero**: grid 1.1fr 1fr, gap 48px, padding 64px 56px.
  - Eyebrow chip cobalto con dot: `● v1.0 · Disponible`
  - Headline 64/63 SemiBold `-0.03em`: "Tu landing,<br>tu agenda<br>y tu alta."
  - Subhead 18px `--slate-500`, max 480px
  - CTAs: primario cobalto, secundario outline `--slate-200`
  - Trust badges 13px `--slate-400`: "✓ Setup en 4 minutos · ✓ Sin tarjeta · ✓ Cobrás desde el día 1"
  - Hero artwork: calendar grid (7 columnas, celdas `aspect-ratio:1`, mezcla de blanco/cobalt-100/cobalt) + card flotante con turno destacado.
- **Vertical strip**: padding 32px 56px sobre `--bg-tint`, label centrado "Para profesionales independientes en", grilla de 6 verticales con iconos abstractos (ver Iconografía).

### 2. Landing del profesional — `/p/{slug}`
**Slide 18 del brand book**

- Slim header 14px, breadcrumb mono con dominio completo.
- Grid 1.1fr 1fr.
  - **Izquierda (perfil)**: avatar circular 88×88 con gradiente del tint vertical, eyebrow mono con título profesional + matrícula, nombre h2 32px, bio body 18px, grid 2×2 de meta-cards (`Modalidad`, `Duración`, `Idioma`, `Honorarios`) sobre `--slate-50`.
  - **Derecha (booking)**: fondo `--bg-tint`, padding 56px 48px, fecha mono, grid 3×N de slot-buttons, slot seleccionado en color del tint vertical, summary card blanca con CTA del color del tint, footer mono "powered by consulte.".

### 3. Dashboard / App — `app.consulte.app/agenda`
**Slide 19 del brand book**

- Top nav 14px 32px: logo lockup + separador 1px + tabs (active = chip `--cobalt-50`/`--cobalt`).
- Grid 280px 1fr 360px.
  - Sidebar (`--slate-50`): vista (Hoy/Semana/Mes/Cancelados) con contadores mono, resumen mensual card blanca.
  - Timeline central: rows `60px 1fr` con tiempo en mono `--slate-400` y card con `border-left:3px solid`. Próximo turno destacado en `--cobalt-50` + `border-left:--cobalt` + sombra suave.
  - Right pane: detalle del próximo turno.

### 4. Email transaccional
**Slide 20 del brand book**

- Header cobalto 24px 32px, lockup invertido blanco.
- Body padding 36px 40px.
  - Eyebrow mono cobalto "TURNO CONFIRMADO"
  - Headline 26px SemiBold con saludo
  - Datos del turno en card `--bg-tint` border `--cobalt-100` con tipografía monoespaciada alineada por columnas (labels `--slate-400`, valores `--ink`)
  - CTA cobalto inline-block
  - Footer 12px `--slate-400`, matrícula + dirección + "powered by consulte."
- **Regla**: nada de imágenes decorativas, gradientes ni emojis.

### 5. OG Image — 1200×630
**Slide 21 del brand book**

- Fondo cobalto pleno.
- Grilla decorativa: `linear-gradient(#fff 1px, transparent 1px), linear-gradient(90deg, #fff 1px, transparent 1px)` 80px, opacity 6%.
- Top-left: lockup invertido (iso 48×48 + wordmark 32px blanco).
- Top-right: mono `--white 60%` "consulte.app · v1.0".
- Bottom: headline 96px SemiBold `-0.035em` (max 980px) + bajada 18px + CTA-flag mono "→ EMPEZAR GRATIS".
- Safe area 80px en todos los bordes.

### 6. Avatar redes
**Slide 22 del brand book**

- Círculo cobalto sólido con glyph blanco centrado al 44% del diámetro.
- Tamaños: 400 (master), 200, 96.

### 7. Favicon
**Slide 22 del brand book**

- Variante sólida (rect fill cobalto + corte horizontal blanco). No usar outline en ≤32px.
- Set: 16, 32, 48, 64, 96, 128.

### 8. Tarjeta digital (vCard)
**Slide 23 del brand book**

- Phone frame 320×600 radio 36, padding interior 14.
- Top 200px cobalto con avatar 80×80 desbordando -40px.
- Datos en mono 12px alineados con labels en `--slate-400`.
- CTAs: agendar (cobalto sólido), guardar contacto (outline).

### 9. Social share dinámico
**Slide 23 del brand book**

- OG variante para `/p/{slug}` con avatar circular blanco, eyebrow mono con título + ciudad, headline 38px SemiBold `"Agendá con {Nombre}"`, marca consulte top-right.
- Por vertical: fondo cobalto se reemplaza por el tint vertical correspondiente.

---

## Interactions & Behavior

- **Hover botones primarios**: background `--cobalt-dark` (`#00327D`).
- **Hover botones outline**: background `--slate-50`, border `--slate-300`.
- **Hover slots de booking**: fondo `--cobalt-50`, border `--cobalt`.
- **Slot activo**: fondo color (`--cobalt` o tint vertical), texto blanco, font-weight 600.
- **Animaciones**: transiciones 150–200ms `ease-out` en bg/border/color de inputs y botones. Sin animaciones de entrada elaboradas. Sin parallax. Sin micro-interacciones cosméticas.

## State Management
Decisiones de producto (booking flow, multi-step onboarding, autenticación) están fuera del scope de identidad. Lo cubrirá un handoff de producto separado.

## Assets
Todos los SVGs (logotipo, glifos verticales) están inline en `Brand Book.html` — se extraen literalmente. No hay imágenes externas. Fonts vienen de Google Fonts (Manrope + JetBrains Mono).

```html
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@200;300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

## Notas finales
- **Cobalto es la marca.** Nunca lo abandones en el producto base. Los tints viven solo en `/p/{slug}`.
- **Nada de iconografía gremial literal.** Sin estetoscopios, balanzas, calculadoras, lápices, cámaras. Los 6 glifos abstractos del slide 16 son canónicos.
- **Manrope + JetBrains Mono** es el único pairing aprobado. No agregar serifs ni display fonts.
- **Lowercase** en el wordmark, siempre, incluyendo el dominio.
