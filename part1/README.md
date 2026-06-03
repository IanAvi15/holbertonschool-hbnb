# HBnB Evolution

A simplified AirBnB-like application built as part of the Holberton School curriculum. This repository covers **Part 1: Technical Documentation** — the architectural blueprint that guides all implementation phases.

---

## Table of Contents

- [Project Description](#project-description)
- [Architecture Overview](#architecture-overview)
- [Entities and Business Rules](#entities-and-business-rules)
- [Documentation Structure](#documentation-structure)
- [Diagrams](#diagrams)
- [Repository Structure](#repository-structure)
- [Authors](#authors)

---

## Project Description

HBnB Evolution allows users to:

- **Register and manage accounts** — sign up, update profile information, and be flagged as administrators
- **List properties** — create places with a title, description, price, and GPS coordinates, and attach amenities to them
- **Leave reviews** — rate and comment on places they have visited
- **Browse places** — query the full listing with optional filters (price, location, etc.)

---

## Architecture Overview

The application follows a **three-layer architecture** with layers communicating through a **Facade pattern**:

```
┌────────────────────────────────────────┐
│          Presentation Layer            │
│   REST API · Services · Endpoints      │
└──────────────────┬─────────────────────┘
                   │  Facade Pattern
┌──────────────────▼─────────────────────┐
│         Business Logic Layer           │
│   User · Place · Review · Amenity      │
└──────────────────┬─────────────────────┘
                   │  Database Operations
┌──────────────────▼─────────────────────┐
│           Persistence Layer            │
│   Repository · ORM · Database          │
└────────────────────────────────────────┘
```

| Layer | Responsibility |
|---|---|
| **Presentation** | Parse HTTP requests, authenticate tokens, serialize responses |
| **Business Logic** | Enforce domain rules, manage entity relationships |
| **Persistence** | Store and retrieve data; abstract the database engine |

The **Facade** is a single service interface that the presentation layer calls exclusively — it never directly touches models or the database. This keeps each layer independently testable and decoupled.

---

## Entities and Business Rules

All entities extend `BaseModel`, which provides:

- `id` — UUID, unique per object
- `created_at` — timestamp set on creation
- `updated_at` — timestamp updated on every save
- `save()` — persists the object
- `to_dict()` — serializes to a plain dictionary for API responses

### User

| Attribute | Type | Notes |
|---|---|---|
| `first_name` | string | required |
| `last_name` | string | required |
| `email` | string | unique across all users |
| `password` | string | stored hashed, never plain text |
| `is_admin` | boolean | defaults to `False` |

Operations: `register()`, `update_profile()`, `delete()`

### Place

| Attribute | Type | Notes |
|---|---|---|
| `title` | string | required |
| `description` | string | optional |
| `price` | float | must be > 0 |
| `latitude` | float | range −90 to 90 |
| `longitude` | float | range −180 to 180 |
| `owner` | User | FK to the creating user |
| `amenities` | list[Amenity] | many-to-many |

Operations: `create()`, `update()`, `delete()`, `list()`

### Review

| Attribute | Type | Notes |
|---|---|---|
| `rating` | int | 1 to 5 inclusive |
| `comment` | string | free text |
| `place` | Place | FK to the reviewed place |
| `user` | User | FK to the reviewing user |

Rules: one user may leave at most one review per place.

Operations: `create()`, `update()`, `delete()`, `list_by_place()`, `list_by_user()`

### Amenity

| Attribute | Type | Notes |
|---|---|---|
| `name` | string | e.g. "Wi-Fi", "Pool" |
| `description` | string | optional detail |

Operations: `create()`, `update()`, `delete()`, `list()`

---

## Documentation Structure

Part 1 delivers four UML artifacts:

### 1 — High-Level Package Diagram

Shows the three layers, the components inside each, and the Facade + database-operations channels connecting them.

### 2 — Business Logic Class Diagram

Full UML class diagram with:
- `BaseModel` as the parent of all four entities
- Attributes with names and types
- Methods per class
- Inheritance arrows (dashed, hollow triangle)
- Associations: User owns Place (1→*), Place has Amenities (*→*), Review references Place and User

### 3 — Sequence Diagrams (4 flows)

| Flow | Endpoint | Auth required |
|---|---|---|
| User registration | `POST /api/users` | No |
| Place creation | `POST /api/places` | Yes (JWT) |
| Review submission | `POST /api/places/{id}/reviews` | Yes (JWT) |
| Fetch list of places | `GET /api/places` | No |

Each diagram shows: Client → API → Facade → Model → DB, with return arrows and `[alt]` frames for error cases (401, 404, 409, 422).

### 4 — Compiled Technical Document

All diagrams plus explanatory notes, design decisions, and HTTP status code conventions gathered in `part1/hbnb_part1_documentation.md`.

---

## Repository Structure

```
holbertonschool-hbnb/
└── part1/
    ├── README.md                        ← this file
    └── hbnb_part1_documentation.md     ← full technical document
```

Parts 2 and 3 will add the implementation directories once the documentation phase is complete.

---

## Design Decisions

**UUID primary keys** — prevent enumeration attacks in API URLs and allow future horizontal scaling without ID collisions.

**Facade pattern** — a single entry point into the business logic layer keeps the API thin, business rules centralized, and each layer independently unit-testable.

**Password hashing** — passwords are hashed (bcrypt or Argon2) inside `User.register()` before any persistence call; the plain text value is never stored or logged.

**Empty-list vs. 404** — a filtered `GET /api/places` with no results returns `200 OK []`, not 404. The resource (the collection) exists; it is simply empty.

**Many-to-many (Place ↔ Amenity)** — modeled as `Place.amenities: list[Amenity]` in the business logic layer. The join table `place_amenities` will be introduced in Part 3 with SQLAlchemy.

---

## Authors

Ian Aviles (https://github.com/IanAvi15)