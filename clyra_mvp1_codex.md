# CLYRA — MVP 1 para desarrollo

## Objetivo del producto

Construir un MVP simple para que un profesional de salud pueda crear su consultorio online en pocos minutos, compartir una landing pública y recibir reservas de turnos. Además, debe poder cargar turnos manuales, registrar pacientes, obra social e información clínica básica.

El foco del MVP 1 es validar si los profesionales usan el link público, reciben turnos y gestionan su agenda desde CLYRA.

---

## Principios del MVP

- Simple antes que completo.
- El médico debe tener su consultorio online listo en menos de 2 minutos.
- La landing pública debe estar disponible automáticamente.
- No incluir funciones complejas como IA, pagos, videollamadas o métricas avanzadas.
- Priorizar una experiencia limpia, profesional y rápida.

---

## Alcance MVP 1

### Incluido

1. Alta de profesional / consultorio.
2. Generación automática de landing pública.
3. Reserva de turnos online desde la landing.
4. Agenda privada para el profesional.
5. Alta manual de turnos.
6. Alta y listado básico de pacientes.
7. Registro de obra social del paciente.
8. Campo simple para dejar asentada información clínica básica.
9. Link público y QR para compartir.

### Excluido por ahora

1. Historia clínica avanzada.
2. Diagnósticos estructurados.
3. IA.
4. Cobros online.
5. Videollamadas.
6. Multi-profesional / centros médicos.
7. Métricas avanzadas.
8. Notificaciones automáticas por WhatsApp o email.
9. Login de paciente con contraseña.

---

## Flujo general

### 1. Landing inicial de CLYRA

Pantalla pública para captar profesionales.

Debe incluir:

- Nombre del producto: CLYRA.
- Mensaje principal: `Tu consultorio online listo en minutos.`
- Subtítulo: `Creá tu página profesional, compartí tu link y empezá a recibir turnos.`
- CTA principal: `Crear mi consultorio`.

Acción del CTA:

- Llevar a `/setup`.

---

### 2. Setup del profesional

Ruta sugerida: `/setup`

Formulario simple de alta del consultorio.

Campos:

- `professional_name` — Nombre completo del profesional.
- `specialty` — Especialidad.
- `email` — Email del profesional.
- `phone` — Teléfono / WhatsApp.
- `address` — Dirección o modalidad de atención.
- `bio` — Breve descripción profesional.
- `working_days` — Días de atención.
- `start_time` — Hora de inicio.
- `end_time` — Hora de fin.
- `appointment_duration_minutes` — Duración estándar del turno.

Al guardar:

- Crear profesional.
- Generar slug público a partir del nombre, por ejemplo: `dr-juan-perez`.
- Redirigir a `/dashboard`.
- Mostrar mensaje: `Tu consultorio ya está online.`
- Mostrar URL pública: `/p/{slug}`.

---

### 3. Dashboard privado

Ruta sugerida: `/dashboard`

Debe ser una pantalla simple con 3 bloques principales.

#### Bloque 1: Agenda del día

Mostrar turnos próximos.

Campos visibles:

- Hora.
- Nombre del paciente.
- Motivo de consulta.
- Estado del turno.

Acciones:

- `Agregar turno`.
- `Ver paciente`.
- `Cancelar turno`.

#### Bloque 2: Link público

Mostrar:

- URL pública del consultorio.
- Botón `Copiar link`.
- Botón o sección para mostrar QR.

#### Bloque 3: Pacientes

Mostrar últimos pacientes registrados.

Acciones:

- `Nuevo paciente`.
- `Ver pacientes`.

---

### 4. Landing pública del profesional

Ruta sugerida: `/p/{slug}`

Esta es la página que el profesional comparte con pacientes.

Debe mostrar:

- Nombre del profesional.
- Especialidad.
- Bio corta.
- Dirección o modalidad de atención.
- Botón principal: `Reservar turno`.

Al hacer clic en reservar turno:

- Mostrar horarios disponibles.
- El paciente selecciona un día y horario.
- Luego completa datos básicos.

---

### 5. Reserva de turno por paciente

Formulario público.

Campos del paciente:

- `first_name` — Nombre.
- `last_name` — Apellido.
- `phone` — Teléfono.
- `email` — Email.
- `health_insurance` — Obra social.
- `health_insurance_plan` — Plan de obra social.
- `health_insurance_number` — Número de afiliado.
- `reason` — Motivo de consulta.

Al confirmar:

- Crear o actualizar paciente si ya existe por teléfono o email.
- Crear turno asociado al profesional y al paciente.
- Mostrar pantalla de confirmación.

Texto de confirmación:

`Tu turno fue reservado correctamente. El profesional podrá contactarte si necesita confirmar información adicional.`

---

### 6. Alta manual de turno

Desde dashboard privado.

Ruta sugerida: `/dashboard/appointments/new`

Uso:

Para turnos que llegan por WhatsApp, email, llamada o presencial.

Campos:

- Buscar paciente existente por nombre, teléfono o email.
- Crear paciente nuevo si no existe.
- Fecha.
- Hora.
- Motivo.
- Estado del turno.

Estados posibles:

- `scheduled`
- `confirmed`
- `cancelled`
- `completed`

---

### 7. Pacientes

Ruta sugerida: `/dashboard/patients`

Listado simple de pacientes.

Columnas:

- Nombre completo.
- Teléfono.
- Email.
- Obra social.
- Último turno.

Acciones:

- Ver detalle.
- Editar.
- Crear nuevo paciente.

---

### 8. Detalle del paciente

Ruta sugerida: `/dashboard/patients/{id}`

Debe mostrar:

#### Datos personales

- Nombre.
- Apellido.
- Teléfono.
- Email.
- Dirección.

#### Cobertura médica

- Obra social.
- Plan.
- Número de afiliado.

#### Información clínica básica

No hacer una historia clínica compleja todavía. Solo un campo simple para notas clínicas.

Campos:

- `clinical_notes` — Texto libre.

Ejemplos de uso:

- Antecedentes relevantes.
- Observaciones del profesional.
- Notas de evolución simples.
- Indicaciones dadas al paciente.

Importante:

- Debe quedar claro en UI que es una nota clínica básica, no una historia clínica avanzada.

---

## Modelo de datos sugerido

### Tabla: professionals

```sql
CREATE TABLE professionals (
    id UUID PRIMARY KEY,
    professional_name VARCHAR(255) NOT NULL,
    specialty VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(50),
    address VARCHAR(255),
    bio TEXT,
    slug VARCHAR(255) NOT NULL UNIQUE,
    working_days VARCHAR(255),
    start_time TIME,
    end_time TIME,
    appointment_duration_minutes INT DEFAULT 30,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### Tabla: patients

```sql
CREATE TABLE patients (
    id UUID PRIMARY KEY,
    professional_id UUID NOT NULL REFERENCES professionals(id),
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    email VARCHAR(255),
    address VARCHAR(255),
    health_insurance VARCHAR(255),
    health_insurance_plan VARCHAR(255),
    health_insurance_number VARCHAR(255),
    clinical_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### Tabla: appointments

```sql
CREATE TABLE appointments (
    id UUID PRIMARY KEY,
    professional_id UUID NOT NULL REFERENCES professionals(id),
    patient_id UUID NOT NULL REFERENCES patients(id),
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    reason TEXT,
    status VARCHAR(50) DEFAULT 'scheduled',
    source VARCHAR(50) DEFAULT 'online',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Valores posibles para `source`:

- `online`
- `manual`
- `whatsapp`
- `email`
- `phone`

---

## Reglas de negocio MVP 1

### Creación de profesional

- El slug debe generarse automáticamente desde el nombre.
- Si el slug ya existe, agregar un número al final.
- Ejemplo: `dr-juan-perez-2`.

### Reserva de turnos

- No permitir dos turnos para el mismo profesional en la misma fecha y hora.
- Mostrar solo horarios dentro del rango de atención definido.
- La duración del turno sale de `appointment_duration_minutes`.

### Pacientes

- Si el paciente reserva con un teléfono ya existente para ese profesional, actualizar sus datos en lugar de duplicarlo.
- Si no existe, crear paciente nuevo.

### Notas clínicas

- Solo el profesional puede ver y editar `clinical_notes`.
- Las notas clínicas no deben verse en la landing pública ni en la confirmación del paciente.

---

## Diseño UI

Estilo general:

- Minimalista.
- Profesional.
- Mucho espacio en blanco.
- Evitar exceso de cards.
- Priorizar velocidad y claridad.

Paleta sugerida:

- Fondo: blanco o gris muy claro.
- Primario: azul, violeta suave o verde salud.
- Texto: negro / gris oscuro.

Componentes clave:

- Botones claros.
- Formularios cortos.
- Tablas simples.
- Estados visibles para turnos.

---

## Orden de desarrollo sugerido

### Etapa 1 — Base del proyecto

1. Crear proyecto web.
2. Configurar base de datos.
3. Crear modelos/tablas.
4. Crear layout base.
5. Crear rutas principales.

Rutas mínimas:

- `/`
- `/setup`
- `/dashboard`
- `/p/{slug}`

---

### Etapa 2 — Alta de profesional

1. Crear formulario de setup.
2. Guardar profesional.
3. Generar slug.
4. Redirigir a dashboard.
5. Mostrar link público.

Prueba:

- Crear un profesional.
- Verificar que se genera la URL pública.

---

### Etapa 3 — Landing pública

1. Leer profesional por slug.
2. Mostrar datos públicos.
3. Mostrar botón de reserva.
4. Crear formulario de reserva.

Prueba:

- Acceder a `/p/{slug}`.
- Completar reserva.
- Confirmar que se crea paciente y turno.

---

### Etapa 4 — Agenda privada

1. Mostrar turnos del profesional.
2. Crear turno manual.
3. Cambiar estado de turno.
4. Cancelar turno.

Prueba:

- Crear turno online.
- Crear turno manual.
- Ver ambos en agenda.

---

### Etapa 5 — Pacientes

1. Crear listado de pacientes.
2. Crear detalle de paciente.
3. Editar datos básicos.
4. Editar obra social.
5. Editar notas clínicas.

Prueba:

- Crear paciente desde reserva online.
- Editar obra social.
- Agregar nota clínica.
- Confirmar que la nota no aparece públicamente.

---

## Criterios de aceptación

El MVP 1 está listo cuando:

1. Un profesional puede crear su consultorio.
2. Se genera una landing pública automáticamente.
3. Un paciente puede reservar un turno desde esa landing.
4. El turno aparece en el dashboard del profesional.
5. El profesional puede cargar turnos manuales.
6. El profesional puede ver y editar pacientes.
7. El paciente tiene datos de obra social.
8. El profesional puede dejar notas clínicas básicas.
9. No se duplican turnos en el mismo horario.
10. La experiencia es simple y usable sin capacitación.

---

## Pendientes para MVP 2

1. QR para alta rápida de paciente.
2. Login mágico del paciente sin contraseña.
3. Recordatorios automáticos.
4. Confirmación de turno por WhatsApp o email.
5. Historia clínica estructurada.
6. Archivos adjuntos.
7. Cobros online.
8. Métricas básicas.
9. Multi-profesional.
10. Integración con Google Calendar.

---

## Nota para Codex

Construir incrementalmente. No implementar todo de una vez.

Prioridad:

1. Setup profesional.
2. Landing pública.
3. Reserva online.
4. Dashboard de agenda.
5. Pacientes + obra social + nota clínica básica.

Mantener el código simple, modular y fácil de extender para MVP 2.
