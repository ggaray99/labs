# CLYRA MVP1 — Mejora de Landing Pública del Profesional

## Objetivo

Modificar la página pública del profesional para que no sea solo una pantalla de reserva de turno, sino una landing profesional orientada a conversión.

La landing debe ayudar al paciente a:
1. Entender quién es el profesional.
2. Confiar en él.
3. Conocer su modalidad de atención.
4. Reservar un turno fácilmente.

---

## Cambio principal

Actualmente la URL pública del profesional muestra directamente:

- Nombre
- Especialidad
- Dirección
- Botón “Reservar turno”

Esto debe evolucionar a una mini landing profesional.

---

## Nueva estructura de la página pública

La URL pública debe mantener el formato actual:

```txt
/p/<slug-profesional>/
```

Ejemplo:

```txt
/p/guillermo-garay/
```

---

## Secciones requeridas

### 1. Hero principal

Debe ser la primera sección visible.

Contenido:

- Avatar o foto del profesional
- Nombre completo
- Especialidad
- Frase corta de valor
- Modalidad de atención
- Botón principal: `Reservar turno`

Ejemplo visual/conceptual:

```txt
Guillermo Garay
Psicología

Atención personalizada para ansiedad, estrés y bienestar emocional.

Presencial en CABA · Online

[Reservar turno]
```

El botón debe llevar a la sección de reserva dentro de la misma página usando anchor:

```txt
#reservar-turno
```

---

### 2. Bloque de confianza

Agregar una sección breve con datos rápidos.

Campos posibles:

- Atención presencial
- Atención online
- Acepta obra social
- Atiende particular
- Ubicación
- Turnos disponibles

Ejemplo:

```txt
✓ Atención presencial y online
✓ Obras sociales y particulares
✓ Turnos simples desde la web
```

No sobrecargar esta sección.

---

### 3. Sobre el profesional

Agregar una sección con una descripción breve del profesional.

Debe salir desde un campo editable del modelo del profesional.

Ejemplo:

```txt
Acompaño a personas que buscan mejorar su bienestar emocional, trabajar la ansiedad, el estrés y construir herramientas para su vida cotidiana.
```

Si el profesional no cargó biografía, mostrar un texto genérico según especialidad.

---

### 4. Especialidades / motivos frecuentes de consulta

Agregar una sección opcional con chips o cards simples.

Ejemplos:

```txt
Ansiedad
Estrés
Autoestima
Terapia individual
Orientación vocacional
```

Estos datos pueden venir inicialmente de un campo texto o lista simple.

Si no hay datos cargados, ocultar la sección.

---

### 5. Reserva de turno

Reutilizar el flujo actual de reserva, pero moverlo más abajo en la página.

Debe estar dentro de una sección con id:

```html
<section id="reservar-turno">
```

Título sugerido:

```txt
Reservá tu turno
```

Mantener:

- Selección de día
- Selección de horario
- Formulario de datos del paciente
- Confirmación del turno

---

## Campos a agregar al modelo del profesional

Agregar o validar que existan estos campos:

```python
tagline = models.CharField(max_length=255, blank=True)
bio = models.TextField(blank=True)
attention_mode = models.CharField(max_length=100, blank=True)
accepts_insurance = models.BooleanField(default=False)
accepts_private = models.BooleanField(default=True)
profile_image = models.ImageField(upload_to="professionals/", blank=True, null=True)
common_reasons = models.TextField(blank=True)
```

Notas:

- `tagline`: frase corta de valor.
- `bio`: descripción profesional.
- `attention_mode`: ejemplo `Presencial`, `Online`, `Presencial y online`.
- `common_reasons`: por ahora puede ser texto separado por comas.
- No hacer una estructura compleja todavía.

---

## Comportamiento esperado si faltan datos

La landing no debe romperse si faltan campos.

Fallbacks:

- Si no hay foto, usar avatar con inicial.
- Si no hay tagline, mostrar:

```txt
Atención profesional personalizada.
```

- Si no hay bio, mostrar:

```txt
Espacio de atención profesional orientado a brindar acompañamiento y seguimiento personalizado.
```

- Si no hay modalidad, no mostrar esa línea.
- Si no hay motivos frecuentes, ocultar esa sección.

---

## Diseño esperado

Estilo:

- Profesional
- Minimalista
- Claro
- Mucho espacio en blanco
- Responsive mobile-first

Evitar:

- Muchas cards innecesarias
- Textos largos
- Estética médica antigua
- Demasiados colores

Colores sugeridos:

```txt
Primario: azul/violeta actual
Fondo: #F8FAFC
Texto: #111827
Texto secundario: #6B7280
Bordes: #E5E7EB
```

---

## Layout sugerido

Desktop:

```txt
[Hero con información]      [Card de reserva rápida o CTA]
[Confianza]
[Sobre el profesional]
[Motivos frecuentes]
[Reservar turno]
```

Mobile:

```txt
Hero
CTA
Confianza
Sobre
Motivos
Reserva
```

---

## Requerimientos técnicos

1. Crear o modificar el template público actual del profesional.
2. Mantener la URL existente.
3. Mantener la lógica actual de reserva de turnos.
4. Reutilizar el formulario actual del paciente.
5. Agregar migración para los nuevos campos del profesional.
6. Actualizar admin/formulario interno para que el profesional pueda editar:
   - tagline
   - bio
   - modalidad
   - acepta obra social
   - acepta particular
   - motivos frecuentes
   - foto de perfil

---

## Criterios de aceptación

La tarea se considera terminada cuando:

- La página pública parece una landing profesional, no solo un formulario.
- El botón principal lleva a la sección de reserva.
- Se pueden mostrar nombre, especialidad, bio, tagline, modalidad y ubicación.
- El flujo actual de reserva sigue funcionando.
- La página funciona aunque falten campos.
- Se ve bien en desktop y mobile.
- El profesional puede editar los nuevos datos desde el panel/admin.

---

## Importante

No agregar todavía:

- Pagos
- Login de paciente
- Historia clínica avanzada
- IA
- Reseñas públicas
- Integración con WhatsApp
- Multi-profesional / clínicas

Este cambio es solo para mejorar la landing pública del profesional dentro del MVP1.
