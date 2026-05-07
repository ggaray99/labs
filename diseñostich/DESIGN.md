---
name: Clinical Clarity
colors:
  surface: '#f7f9fb'
  surface-dim: '#d8dadc'
  surface-bright: '#f7f9fb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f4f6'
  surface-container: '#eceef0'
  surface-container-high: '#e6e8ea'
  surface-container-highest: '#e0e3e5'
  on-surface: '#191c1e'
  on-surface-variant: '#434655'
  inverse-surface: '#2d3133'
  inverse-on-surface: '#eff1f3'
  outline: '#737686'
  outline-variant: '#c3c6d7'
  surface-tint: '#0053db'
  primary: '#004ac6'
  on-primary: '#ffffff'
  primary-container: '#2563eb'
  on-primary-container: '#eeefff'
  inverse-primary: '#b4c5ff'
  secondary: '#006a61'
  on-secondary: '#ffffff'
  secondary-container: '#86f2e4'
  on-secondary-container: '#006f66'
  tertiary: '#515659'
  on-tertiary: '#ffffff'
  tertiary-container: '#696e71'
  on-tertiary-container: '#edf1f5'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dbe1ff'
  primary-fixed-dim: '#b4c5ff'
  on-primary-fixed: '#00174b'
  on-primary-fixed-variant: '#003ea8'
  secondary-fixed: '#89f5e7'
  secondary-fixed-dim: '#6bd8cb'
  on-secondary-fixed: '#00201d'
  on-secondary-fixed-variant: '#005049'
  tertiary-fixed: '#dfe3e7'
  tertiary-fixed-dim: '#c3c7cb'
  on-tertiary-fixed: '#171c1f'
  on-tertiary-fixed-variant: '#43474b'
  background: '#f7f9fb'
  on-background: '#191c1e'
  surface-variant: '#e0e3e5'
typography:
  h1:
    fontFamily: Manrope
    fontSize: 40px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  h2:
    fontFamily: Manrope
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.25'
    letterSpacing: -0.01em
  h3:
    fontFamily: Manrope
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.05em
  stats-display:
    fontFamily: Manrope
    fontSize: 48px
    fontWeight: '800'
    lineHeight: '1'
    letterSpacing: -0.03em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
  container-max: 1440px
  gutter: 24px
---

## Brand & Style

This design system is engineered for the high-stakes environment of healthcare, where cognitive load must be minimized and trust is paramount. The brand personality is **composed, precise, and empathetic**. It avoids the sterility of traditional medical software by introducing warmth through soft geometry and organic accent colors.

The design style is **Modern Corporate Minimalism**. It prioritizes a clear information hierarchy using ample whitespace and modular containment. By leveraging a "Soft-UI" approach—combining flat surfaces with very subtle, diffused shadows—the system achieves a sense of depth that guides the eye without distracting the user from critical patient data.

## Colors

The palette is anchored in "Professional Blue" (#2563eb) to evoke stability and authority. "Soft Teal" (#0d9488) serves as a secondary accent, used primarily for health-positive actions, growth indicators, or specialized clinical modules.

The neutral scale is weighted heavily toward "Clean Whites" and cool grays to maintain a high-contrast, sterile feel that ensures legibility. Semantic colors for errors and successes are slightly desaturated to remain harmonious with the professional tone, ensuring they alert the professional without causing unnecessary alarm.

## Typography

This design system utilizes a dual-font strategy. **Manrope** is used for headings and data displays to provide a modern, refined, and slightly more geometric character that feels premium. **Inter** is used for all body copy, inputs, and labels due to its exceptional legibility in dense data environments.

Line heights are intentionally generous to prevent "text-crowding," which is common in medical records. For critical numeric data, use the `stats-display` style to ensure key vitals are immediately identifiable.

## Layout & Spacing

The system employs a **12-column fixed grid** for desktop dashboards, transitioning to a fluid model for tablets. A strict 4px base unit governs all dimensions.

Modular sections (cards) should use `lg` (24px) padding to maintain the "warm and accessible" feel. Grouped form elements should use `sm` (8px) spacing, while distinct clinical sections within a page should be separated by `xl` (40px) to provide clear mental breaks between different categories of information.

## Elevation & Depth

Visual hierarchy is achieved through **Tonal Layering** and **Ambient Shadows**. The background layer is the Neutral `f8fafc`. Secondary containers (sidebars, utility panels) use pure white `ffffff` with a subtle 1px border in a light gray.

Primary interaction objects, such as patient cards or diagnostic modals, use an "Ambient Lift" shadow: 
- `box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);`
This creates a soft, tactile depth that makes elements feel interactive without appearing "heavy" or cluttered.

## Shapes

The design system uses a **Rounded** language to soften the clinical nature of the interface. 
- Standard components (buttons, inputs): `0.5rem` (8px).
- Containers and Cards: `1rem` (16px).
- Modals and large feature sections: `1.5rem` (24px).

This progressive rounding ensures that larger surfaces feel approachable while smaller interactive elements remain precise and professional.

## Components

**Buttons:** Primary buttons use a solid #2563eb fill with white text. Secondary buttons use a teal #0d9488 outline or subtle tint. Ghost buttons are reserved for utility actions.

**Inputs:** Field backgrounds should be white with a 1px border. On focus, the border transitions to Primary Blue with a soft 3px outer glow (halo). Labels must always be visible above the field.

**Chips/Tags:** Used for patient status (e.g., "Stable", "Critical"). These utilize the secondary teal or semantic colors with a 10% opacity background and a 100% opacity text for high readability without visual noise.

**Cards:** The core building block. Every card must have a consistent 16px corner radius and a subtle ambient shadow. Use cards to modularize patient vitals, history, and prescriptions.

**Data Tables:** Minimize borders; use zebra-striping with the neutral color for row distinction. Header text should use the `label-caps` typography style for clarity.

**Additional Recommended Components:** 
- *Vital Sign Sparklines:* Small, simplified charts for immediate trend recognition.
- *Status Indicator Dots:* To show real-time connectivity or patient urgency.
- *Timeline View:* A vertical modular list for patient history.