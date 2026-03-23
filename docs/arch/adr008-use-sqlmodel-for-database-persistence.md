# ADR008: Use SQLModel for Database Persistence

## Context

This project is a teaching-oriented FastAPI starter for a URL shortener. The current implementation uses a simple file-backed store so students can begin with a working application and a clear separation between routes, services, and persistence.

The next architectural step is to replace that temporary store layer with real database-backed persistence. We need a persistence approach that works well with FastAPI, supports typed Python models, and is approachable for students who are learning how to move from in-memory or file-backed data to relational storage.

The chosen tool should:

- Fit naturally with FastAPI request-handling patterns.
- Support typed models with clear field declarations.
- Build on broadly useful SQLAlchemy concepts without requiring students to learn the full ORM surface area up front.
- Work well with PostgreSQL.
- Keep the codebase small and readable for instructional use.

## Decision

Use `SQLModel` for the database persistence layer.

`SQLModel` combines Pydantic-style model declarations with SQLAlchemy-powered table mapping and sessions. This makes it a good fit for a FastAPI codebase and provides a practical bridge between API validation models and relational persistence concepts.

In this project, `SQLModel` will be used for:

- Persistence entities in [../../src/entities](../../src/entities)
- Database engine and session management in [../../src/db.py](../../src/db.py)
- Table creation for local development and instructional workflows
- Student work that replaces the current file-backed store implementation

## Considered Options

- Raw SQL with `psycopg2`
    - Pros: exposes SQL directly and keeps abstractions minimal.
    - Cons: more boilerplate, more manual mapping code, and a steeper path for students moving from Python models to relational persistence.

- SQLAlchemy ORM directly
    - Pros: powerful, flexible, industry-standard foundation.
    - Cons: larger API surface and more conceptual overhead than needed for this starter.

- Keep the file-backed store indefinitely
    - Pros: simplest implementation, very low setup cost.
    - Cons: does not teach relational persistence, transactions, sessions, or database-backed application design.

## Consequences

- Students learn a persistence tool that fits naturally into the existing FastAPI architecture.
- The repository can maintain a clean distinction between API models in [../../src/models](../../src/models) and persistence entities in [../../src/entities](../../src/entities).
- Database session handling becomes an explicit part of the application architecture through [../../src/db.py](../../src/db.py).
- The project remains approachable while still introducing foundational relational database patterns.
- Some duplication between API models and persistence entities may remain, but that separation is acceptable for clarity in a teaching codebase.