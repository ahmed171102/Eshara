# Database — Prisma Schema & Migrations

This folder contains the **standalone database schema and migration history** for the Eshara system, separated from the backend application code for clarity. The full database design is documented in **Chapter 5, Section 5.4** of the thesis.

## Technology

| Component | Technology |
|---|---|
| ORM | **Prisma** |
| Database (local dev) | SQLite (`dev.db` — gitignored, never committed) |
| Database (production) | PostgreSQL via **Neon** (cloud-hosted, serverless) |

## Files

```
database/
├── schema.prisma                          # Database schema — single source of truth
└── migrations/
    ├── migration_lock.toml                # Prisma migration provider lock
    └── 20260508085321_init_auth_chat/
        └── migration.sql                  # Initial migration: all tables + enums
```

---

## Data Models

### `User`
Stores registered accounts. Passwords are **never stored in plaintext** — only a `bcryptjs`-hashed `passwordHash`.

```prisma
model User {
  id           String       @id @default(cuid())
  name         String
  email        String       @unique
  passwordHash String
  createdAt    DateTime     @default(now())
  updatedAt    DateTime     @updatedAt
  memberships  RoomMember[]
  messages     Message[]
}
```

### `Room`
Represents a chat room. Supports `DIRECT` (1-to-1) and `GROUP` types.

### `RoomMember`
Junction table linking `User` ↔ `Room` with `@@unique([roomId, userId])` — a user can only join a room once.

### `Message`
Stores all messages with a `MessageType` enum to distinguish origins:

| Type | Meaning |
|---|---|
| `TEXT` | Manually typed by a user |
| `PREDICTION` | AI-generated translation from the sign recognition models |
| `SYSTEM` | Automated notifications (user joined/left/disconnected) |

This distinction is surfaced in the React UI — users always know whether a message was typed or AI-generated.

---

## Running Migrations

```bash
# From the application/backend/ directory:
npx prisma migrate dev     # Apply migrations to local SQLite dev.db
npx prisma studio          # Open Prisma Studio to browse the database visually
```

> **Important:** `dev.db` is gitignored and should never be committed — it contains real user data. Clone users should run `npx prisma migrate dev` to generate a fresh empty database.
