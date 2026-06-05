# HBnB Evolution — Business Logic Layer: Class Diagram

## Diagram

```mermaid
classDiagram

%% ─── Base class ───────────────────────────────────────────────
class BaseModel {
    <<abstract>>
    +UUID4 id
    +DateTime created_at
    +DateTime updated_at
    +save() None
    +to_dict() dict
    +delete() None
}

%% ─── Core entities ────────────────────────────────────────────
class User {
    +String first_name
    +String last_name
    +String email
    -String password
    +Boolean is_admin
    +register() User
    +update_profile() None
    +hash_password() String
}

class Place {
    +String title
    +String description
    +Float price
    +Float latitude
    +Float longitude
    +User owner
    +List~Amenity~ amenities
    +list(filters) List
    +add_amenity(amenity) None
    +remove_amenity(amenity) None
}

class Review {
    +Integer rating
    +String comment
    +Place place
    +User user
    +list_by_place() List
    +list_by_user() List
    +validate_rating() Boolean
}

class Amenity {
    +String name
    +String description
    +list() List
    +validate_name() Boolean
}

%% ─── Inheritance (generalization) ─────────────────────────────
BaseModel <|-- User      : extends
BaseModel <|-- Place     : extends
BaseModel <|-- Review    : extends
BaseModel <|-- Amenity   : extends

%% ─── Associations ─────────────────────────────────────────────
User       "1"  --> "0..*" Place   : owns
Place      "0..*" *-- "0..*" Amenity : has (many-to-many)
Review     "0..*" --> "1"   Place   : for place
Review     "0..*" --> "1"   User    : by user
```

---

## Entity Descriptions

### BaseModel `«abstract»`

The root of every domain entity. Provides:

- `id` — a UUID4 generated on instantiation; globally unique across all tables.
- `created_at` / `updated_at` — audit timestamps. `updated_at` is refreshed automatically on every `save()` call.
- `save()` — flushes the object to the persistence layer.
- `to_dict()` — serializes the object to a plain dictionary for API responses.
- `delete()` — removes the record from the persistence layer.

No entity is ever stored without these fields.

---

### User

Represents both regular visitors and platform administrators.

| Attribute | Type | Constraint |
|---|---|---|
| `first_name` | str | required |
| `last_name` | str | required |
| `email` | str | unique across all users |
| `password` | str | stored **hashed** (private) |
| `is_admin` | bool | defaults to `False` |

Key methods:
- `register()` — validates uniqueness of email, calls `hash_password()`, persists the new user.
- `update_profile()` — updates mutable fields (name, email); re-hashes if password changes.
- `hash_password()` — private helper; applies bcrypt/Argon2. Never stores plain text.

---

### Place

A property listing owned by exactly one `User`.

| Attribute | Type | Constraint |
|---|---|---|
| `title` | str | required |
| `description` | str | optional |
| `price` | float | must be > 0 |
| `latitude` | float | −90 to +90 |
| `longitude` | float | −180 to +180 |
| `owner` | User | FK; set on creation |
| `amenities` | list[Amenity] | many-to-many |

Key methods:
- `list(filters)` — returns filtered and paginated listings.
- `add_amenity(amenity)` / `remove_amenity(amenity)` — manage the join table without exposing it directly.

---

### Review

A single rating + comment left by one `User` for one `Place`. Business rule: a user may submit at most one review per place.

| Attribute | Type | Constraint |
|---|---|---|
| `rating` | int | 1 to 5 inclusive |
| `comment` | str | free text |
| `place` | Place | FK; immutable after creation |
| `user` | User | FK; immutable after creation |

Key methods:
- `list_by_place()` — all reviews for a given place, newest first.
- `list_by_user()` — all reviews written by a given user.
- `validate_rating()` — enforces the 1–5 range before persistence.

---

### Amenity

A named feature (e.g. "Wi-Fi", "Pool") managed centrally and shared across many places.

| Attribute | Type | Constraint |
|---|---|---|
| `name` | str | unique |
| `description` | str | optional |

Key methods:
- `list()` — full catalogue of available amenities.
- `validate_name()` — prevents duplicate or empty names.

---

## Relationship Summary

| Relationship | Type | Multiplicity | Notes |
|---|---|---|---|
| `User / Place / Review / Amenity` → `BaseModel` | Generalization | 4 → 1 | All inherit id + timestamps |
| `User` → `Place` | Association | 1 to 0..* | A user owns zero or more places |
| `Place` ↔ `Amenity` | Composition | 0..* to 0..* | Many-to-many via join table `place_amenities` |
| `Review` → `Place` | Association | 0..* to 1 | Each review targets exactly one place |
| `Review` → `User` | Association | 0..* to 1 | Each review is authored by exactly one user |

### Notation key

| Symbol | Meaning |
|---|---|
| `<\|--` | Generalization (inheritance) |
| `*--` | Composition |
| `-->` | Association |
| `-` prefix on attribute | Private visibility |
| `+` prefix on attribute | Public visibility |