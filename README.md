# 💈 ChatBotBarber

<p align="center">
  <strong>Sistema inteligente de gestión y agendamiento de citas para barberías</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-Vite-61DAFB?style=for-the-badge&logo=react" alt="React">
  <img src="https://img.shields.io/badge/TypeScript-Frontend-3178C6?style=for-the-badge&logo=typescript" alt="TypeScript">
  <img src="https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql" alt="PostgreSQL">
</p>

---

## 📌 Descripción

**ChatBotBarber** es una aplicación web desarrollada para facilitar la gestión y agendamiento de citas en una barbería.

El sistema permite administrar la información relacionada con **usuarios, servicios, especialistas, agendas, disponibilidades y citas**, ofreciendo una experiencia organizada tanto para los clientes como para el personal encargado de la barbería.

La aplicación está compuesta por un **backend desarrollado con FastAPI y Python**, un **frontend desarrollado con React + Vite + TypeScript** y una **base de datos PostgreSQL**, administrada mediante **pgAdmin**.

El proyecto busca reducir la gestión manual de las citas, mejorar la organización de los horarios y evitar problemas como la **doble reserva de un mismo horario**.

---

# 🏗️ Arquitectura del proyecto

ChatBotBarber utiliza diferentes enfoques arquitectónicos para organizar sus componentes:

```text
                         ┌──────────────────────┐
                         │      CLIENTE         │
                         │   Navegador Web      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       FRONTEND       │
                         │  React + Vite + TS   │
                         └──────────┬───────────┘
                                    │
                              HTTP / REST API
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       BACKEND        │
                         │   FastAPI + Python   │
                         │                      │
                         │   Presentación       │
                         │        ↓             │
                         │   Negocio            │
                         │        ↓             │
                         │   Datos              │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      PostgreSQL      │
                         │       + pgAdmin      │
                         └──────────────────────┘
```

---

# ⚙️ Backend

El backend de **ChatBotBarber** fue desarrollado utilizando **Python y FastAPI**, implementando una **arquitectura monolítica de 3 capas**.

Esta arquitectura permite separar las responsabilidades del sistema en diferentes niveles, facilitando el mantenimiento, organización y evolución del proyecto.

### 🔹 Capa de presentación

Gestiona la entrada y salida de información mediante las rutas desarrolladas con **FastAPI** y la validación de datos utilizando **Pydantic**.

Se encarga de recibir las solicitudes HTTP, validar la información y enviar las respuestas correspondientes.

### 🔹 Capa de negocio

Procesa las reglas operativas de la barbería, incluyendo la creación y gestión de agendas, validación de disponibilidades, cálculo de información relacionada con las citas y cambios de estado.

Además, se implementan bloqueos de concurrencia mediante:

```sql
FOR UPDATE
```

Esto permite reducir el riesgo de que dos usuarios puedan reservar simultáneamente el mismo horario.

### 🔹 Capa de acceso a datos

Se encarga de la comunicación con **PostgreSQL** mediante **SQLAlchemy**, utilizando modelos ORM para representar las tablas de la base de datos.

Esta separación permite mantener una estructura organizada y facilita futuras modificaciones en el acceso a los datos.

---

# 📂 Estructura del Backend

```text
backend/
│
├── config/
│   └── ...
│
├── controllers/
│   └── ...
│
├── models/
│   └── ...
│
├── routes/
│   └── ...
│
├── schema/
│   └── ...
│
├── utils/
│   └── ...
│
└── main.py
```

### 📁 `config/`

**Configuración y conexión a la base de datos.**

Gestiona la conexión con PostgreSQL mediante SQLAlchemy y centraliza configuraciones importantes del proyecto.

### 📁 `controllers/`

**Lógica de negocio.**

Contiene las reglas principales del sistema, como:

* Validación de disponibilidades.
* Gestión de agendas.
* Gestión de citas.
* Cálculo de precios.
* Cambio de estados.
* Ejecución de operaciones relacionadas con la base de datos.

### 📁 `models/`

**Modelos ORM.**

Representa las tablas de PostgreSQL mediante clases de Python utilizando SQLAlchemy.

### 📁 `routes/`

**Capa de presentación.**

Define los endpoints de la API y recibe las peticiones HTTP realizadas por el frontend.

Entre las operaciones se encuentran:

```text
GET
POST
PUT
DELETE
```

### 📁 `schema/`

**Esquemas Pydantic / DTOs.**

Define la estructura de los datos que recibe y devuelve la API, realizando validaciones para evitar información incompleta o incorrecta.

### 📁 `utils/`

**Funciones auxiliares.**

Contiene funciones reutilizables para tareas como:

* Formateo de fechas.
* Organización de agendas.
* Estructuración de respuestas JSON.
* Funciones auxiliares del sistema.

---

# 🎨 Frontend

El frontend de **ChatBotBarber** fue desarrollado utilizando:

* ⚛️ **React**
* ⚡ **Vite**
* 🔷 **TypeScript**

Se implementó una arquitectura modular orientada a componentes, permitiendo reutilizar elementos de la interfaz y mantener una separación clara entre las diferentes responsabilidades.

La aplicación utiliza **React Context API** para la gestión de información global y TypeScript para garantizar un tipado seguro durante el desarrollo.

---

# 📂 Estructura del Frontend

```text
frontend/
│
├── assets/
│   └── ...
│
├── components/
│   └── ...
│
├── context/
│   └── ...
│
├── interfaces/
│   └── ...
│
├── pages/
│   └── ...
│
├── routes/
│   └── ...
│
├── services/
│   └── ...
│
└── main.tsx
```

### 📁 `assets/`

**Recursos estáticos.**

Contiene imágenes, fuentes, iconos y otros recursos gráficos utilizados por la aplicación.

### 📁 `components/`

**Componentes reutilizables.**

Contiene elementos independientes de la interfaz como:

* Botones.
* Formularios.
* Modales.
* Barras de navegación.
* Tablas.
* Otros componentes visuales.

### 📁 `context/`

**Gestión del estado global.**

Utiliza **React Context API** para centralizar información compartida por diferentes partes de la aplicación, como la sesión del usuario.

### 📁 `interfaces/`

**Contratos y tipos TypeScript.**

Define las estructuras utilizadas por la aplicación, por ejemplo:

```text
Usuario
Agenda
Servicio
Cita
```

Esto permite mantener consistencia en el manejo de los datos.

### 📁 `pages/`

**Vistas principales.**

Contiene las páginas que forman parte de la aplicación, incluyendo las diferentes interfaces disponibles para los usuarios.

### 📁 `routes/`

**Control de navegación.**

Gestiona la navegación entre las diferentes vistas y permite controlar el acceso a determinadas secciones de acuerdo con los permisos del usuario.

### 📁 `services/`

**Comunicación con el Backend.**

Contiene las funciones encargadas de realizar las solicitudes HTTP hacia la API desarrollada con FastAPI.

---

# 🗄️ Base de datos

ChatBotBarber utiliza **PostgreSQL** como sistema gestor de base de datos.

La base de datos se administra mediante **pgAdmin**, permitiendo realizar tareas como:

* Creación y modificación de tablas.
* Administración de relaciones.
* Inserción y consulta de información.
* Gestión de restricciones.
* Verificación de datos.
* Administración general de la base de datos.

La comunicación entre el backend y PostgreSQL se realiza mediante **SQLAlchemy**.

```text
React + TypeScript
        │
        │ HTTP
        ▼
     FastAPI
        │
        │ SQLAlchemy
        ▼
   PostgreSQL
        ▲
        │
      pgAdmin
```

---

# 🧰 Tecnologías utilizadas

| Tecnología    | Uso                                               |
| ------------- | ------------------------------------------------- |
| 🐍 Python     | Lenguaje del backend                              |
| 🚀 FastAPI    | Framework para la API REST                        |
| 📦 Pydantic   | Validación y estructuración de datos              |
| 🔗 SQLAlchemy | ORM y acceso a PostgreSQL                         |
| ⚛️ React      | Desarrollo de la interfaz                         |
| ⚡ Vite        | Entorno de desarrollo y construcción del frontend |
| 🔷 TypeScript | Tipado estático del frontend                      |
| 🐘 PostgreSQL | Sistema gestor de base de datos                   |
| 🛠️ pgAdmin   | Administración de PostgreSQL                      |
| 🌐 REST API   | Comunicación entre frontend y backend             |

---

# ✨ Funcionalidades principales

### 👤 Gestión de usuarios

Permite administrar la información de los usuarios y controlar el acceso al sistema mediante diferentes roles.

### 💈 Gestión de servicios

Permite administrar los servicios ofrecidos por la barbería, incluyendo información como nombre, descripción y precio.

### 📅 Gestión de agendas

Permite organizar las agendas de los especialistas y controlar los horarios disponibles.

### 🕐 Disponibilidad de horarios

El sistema permite consultar los horarios disponibles antes de realizar una reserva.

### 📌 Agendamiento de citas

Los clientes pueden seleccionar la información necesaria para realizar una cita, incluyendo:

```text
Servicio
   ↓
Especialista
   ↓
Fecha
   ↓
Hora
   ↓
Confirmación
```

### 🔒 Control de concurrencia

Se implementan mecanismos de bloqueo utilizando `FOR UPDATE` para ayudar a prevenir la doble reserva de un mismo horario cuando existen solicitudes simultáneas.

### 🔄 Gestión de estados

Las citas pueden manejar diferentes estados de acuerdo con el flujo definido por el sistema.

---

# 🔄 Flujo general de una cita

```text
┌──────────────┐
│    INICIO    │
└──────┬───────┘
       ↓
┌─────────────────────┐
│ Agendar una cita    │
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│ Seleccionar servicio│
└─────────┬───────────┘
          ↓
┌──────────────────────┐
│ Seleccionar          │
│ especialista         │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Consultar             │
│ disponibilidad        │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Seleccionar fecha     │
│ y hora                │
└──────────┬───────────┘
           ↓
      ¿Disponible?
       ↙       ↘
     NO         SÍ
     ↓           ↓
Mostrar        Registrar
otros horarios   cita
                   ↓
              Programada
                   ↓
                 FIN
```

---

# 🚀 Instalación y ejecución

## 📋 Requisitos

Antes de ejecutar el proyecto se recomienda tener instalado:

* 🐍 Python 3.x
* 📦 Node.js
* 🐘 PostgreSQL
* 🛠️ pgAdmin
* 📁 Git

---

## 🔙 Ejecutar Backend

Ingresar a la carpeta del backend:

```bash
cd backend
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar el servidor:

```bash
python -m uvicorn main:app --reload
```

El backend estará disponible normalmente en:

```text
http://127.0.0.1:8000
```

La documentación interactiva de FastAPI puede consultarse en:

```text
http://127.0.0.1:8000/docs
```

---

## 🎨 Ejecutar Frontend

Ingresar a la carpeta del frontend:

```bash
cd frontend
```

Instalar las dependencias:

```bash
npm install
```

Ejecutar el proyecto:

```bash
npm run dev
```

Vite mostrará en la terminal la dirección local donde estará disponible la aplicación.

---

# 🔐 Configuración

Antes de ejecutar el backend es necesario configurar los datos de conexión a PostgreSQL.

Ejemplo:

```env
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/chatbotbarber
```

> ⚠️ Las credenciales reales no deben almacenarse directamente en el repositorio. Se recomienda utilizar variables de entorno y mantener los archivos `.env` fuera del control de versiones.

---

# 🌐 Comunicación entre Frontend y Backend

El frontend se comunica con la API mediante solicitudes HTTP.

Ejemplo de configuración:

```typescript
const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1"
});
```

La comunicación permite realizar operaciones como:

```text
Frontend
   │
   ├── GET    → Consultar información
   ├── POST   → Crear registros
   ├── PUT    → Actualizar registros
   └── DELETE → Eliminar registros
          │
          ▼
       FastAPI
          │
          ▼
     PostgreSQL
```

---

# 📁 Estructura general del proyecto

```text
ChatBotBarber/
│
├── backend/
│   ├── config/
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   ├── schema/
│   ├── utils/
│   └── main.py
│
├── frontend/
│   ├── assets/
│   ├── components/
│   ├── context/
│   ├── interfaces/
│   ├── pages/
│   ├── routes/
│   ├── services/
│   └── main.tsx
│
├── database/
│   └── scripts.sql
│
├── README.md
└── .gitignore
```

---

# 🧩 Principios de desarrollo

Durante el desarrollo de ChatBotBarber se tuvieron en cuenta diferentes principios para mantener una estructura organizada:

* 📌 Separación de responsabilidades.
* ♻️ Reutilización de componentes.
* 🔒 Validación de información.
* 🧱 Modularidad.
* 📐 Tipado estático.
* 🔗 Separación entre frontend y backend.
* 🗄️ Organización de acceso a datos.
* 🚦 Control de estados.
* 🔐 Protección de información sensible.

---

# 🎯 Objetivo del proyecto

El objetivo de **ChatBotBarber** es proporcionar una solución tecnológica que permita mejorar la gestión de citas de una barbería, facilitando la organización de los horarios, servicios y especialistas.

Mediante la integración de **React, TypeScript, FastAPI, Python y PostgreSQL**, se construyó una aplicación estructurada y escalable que permite centralizar los procesos relacionados con el agendamiento y administración de citas.

---

# 👨‍💻 Proyecto

**ChatBotBarber**

> Sistema web para la gestión y agendamiento de citas en una barbería.

### Tecnologías principales

**Frontend:** React + Vite + TypeScript
**Backend:** Python + FastAPI
**Base de datos:** PostgreSQL
**Administrador de BD:** pgAdmin
**ORM:** SQLAlchemy

---

<p align="center">

### 💈 ChatBotBarber

**Tecnología para una mejor gestión de tu barbería.**

</p>

<p align="center">
  <strong>🚀 Desarrollado como proyecto formativo</strong>
</p>
