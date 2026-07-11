# HBnB Evolution — Part 3: Authentication & Database Integration

Extending the HBnB backend with JWT authentication, role-based access control, and persistent database storage using SQLAlchemy.

---

## Overview

Previous parts of the project used in-memory storage, which works for prototyping but doesn't scale. Part 3 transitions the application to a real database backend while securing the API with industry-standard authentication practices.

---

## Objectives

- **Authentication & Authorization** — Implement JWT-based authentication with Flask-JWT-Extended and enforce role-based access control using the `is_admin` attribute
- **Database Integration** — Replace in-memory repositories with SQLite (development) and MySQL (production) via SQLAlchemy ORM
- **CRUD Persistence** — Refactor all CRUD operations to interact with a persistent database
- **Schema Design** — Design and visualize the relational database schema using Mermaid.js
- **Data Integrity** — Enforce validation and constraints directly in the models

---

## Task Breakdown

| # | Task | Description |
|---|---|---|
| 1 | User model update | Store passwords securely using bcrypt2 |
| 2 | JWT authentication | Secure API endpoints with JWT tokens |
| 3 | Authorization | Restrict actions to admin vs. regular users |
| 4 | SQLite integration | Swap in-memory storage for SQLite |
| 5 | SQLAlchemy mapping | Map User, Place, Review, Amenity to the DB |
| 6 | MySQL configuration | Prepare production config for MySQL |
| 7 | ER diagram | Visualize the schema with Mermaid.js |

---

## Learning Outcomes

By the end of this part you will be able to:

- Issue and validate JWT tokens to manage user sessions
- Enforce role-based restrictions on specific API endpoints
- Design a relational schema and map it with SQLAlchemy
- Switch database backends between environments using Flask configuration
- Visualize entity relationships with Mermaid.js ER diagrams

---

## Resources

- [Flask-JWT-Extended Documentation](https://flask-jwt-extended.readthedocs.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Flask Official Documentation](https://flask.palletsprojects.com/)
- [Mermaid.js ER Diagrams](https://mermaid.js.org/syntax/entityRelationshipDiagram.html)

---

## AUTHOR

Ian Aviles