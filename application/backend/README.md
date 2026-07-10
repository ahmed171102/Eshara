# Backend — Node.js + Express Application Tier

This is the **Application Tier** of the Eshara three-tier architecture, as documented in **Chapter 5, Sections 5.3–5.4** of the thesis. It acts as the secure gateway between the React frontend and the FastAPI AI inference tier.

## Key Responsibilities

- **JWT Authentication:** Stateless session management using JSON Web Tokens; passwords hashed with `bcryptjs` before database storage
- **Prediction Proxy:** Receives sign frames from the frontend, validates the JWT, and proxies the request internally to FastAPI's `/predict` — the ML service is never exposed to the public internet
- **Real-time Chat:** Socket.IO server validates JWT on handshake and broadcasts messages via custom events (`chat:join`, `chat:send`, `chat:receive`)
- **Database:** SQLite managed via Prisma ORM with four models: `User`, `Room`, `RoomMember`, `Message`

## Message Types (from Prisma schema)

The `Message` model uses a `MessageType` enum to distinguish message origins:
- `TEXT` — manually typed by a user
- `PREDICTION` — AI-generated translation from the sign recognition models
- `SYSTEM` — automated notifications (user joined, left, disconnected)

This distinction is surfaced in the React UI to ensure users always know whether a message was typed or AI-generated.

## Structure

```
src/
├── app.js                  Express app setup (CORS, JSON parser, routes)
├── server.js               HTTP server entry point + Socket.IO init
├── controllers/
│   ├── auth.controller.js  Register / login (bcrypt + JWT)
│   ├── predict.controller.js  Proxy /predict to FastAPI
│   └── users.controller.js
├── routes/
│   ├── auth.routes.js
│   ├── predict.routes.js
│   ├── users.routes.js
│   └── health.routes.js
├── middleware/
│   └── auth.middleware.js  JWT verification guard
├── sockets/
│   └── chat.socket.js      Socket.IO event handlers
├── lib/
│   └── prisma.js           Prisma client singleton
└── utils/
    └── jwt.js              Token sign/verify helpers
prisma/
├── schema.prisma           Database schema (User, Room, RoomMember, Message)
└── migrations/             Prisma migration history
```

## Setup

```bash
npm install
npx prisma migrate dev   # Run database migrations
npm run dev
```

Runs at **http://localhost:3000**
