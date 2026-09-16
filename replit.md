# FreightIQ Charter Intelligence

FreightIQ is an enterprise maritime analytics workspace for freight forecasting, vessel feasibility, port constraints, idle-time analysis, and contract strategy comparison.

## Run & Operate

- `pnpm --filter @workspace/api-server run dev` — run the API server (port 5000)
- `pnpm --filter @workspace/freightiq run dev` — run the FreightIQ frontend
- `pnpm --filter @workspace/freightiq run typecheck` — typecheck the FreightIQ frontend
- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from the OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- Required env: `DATABASE_URL` — Postgres connection string

## Stack

- pnpm workspaces, Node.js 24, TypeScript 5.9
- API: Express 5
- DB: PostgreSQL + Drizzle ORM
- Validation: Zod (`zod/v4`), `drizzle-zod`
- API codegen: Orval (from OpenAPI spec)
- Build: esbuild (CJS bundle)

## Where things live

- `artifacts/freightiq/src/App.tsx` — shared shell, routing, page composition, and interactions
- `artifacts/freightiq/src/data/mockData.ts` — deterministic maritime datasets and domain types
- `artifacts/freightiq/src/index.css` — FreightIQ visual tokens, typography, semantic statuses, and responsive utilities
- `artifacts/freightiq/src/components/` — reusable dashboard, chart, table, form, vessel, port, contract, and risk components
- `artifacts/freightiq/src/pages/` — route-level page components
- `lib/api-spec/openapi.yaml` — future API contract source of truth

## Architecture decisions

- The first release is frontend-only and uses deterministic mock services so the complete decision workflow works without a backend.
- Routing uses `wouter` and is prefix-aware through the artifact's managed `BASE_PATH`.
- The UI intentionally separates model-derived signals from user decisions and avoids presenting contract scenarios as a single guaranteed winner.
- Future FastAPI integration should replace the mock service functions while preserving the current typed page contracts.

## Product

FreightIQ gives chartering and logistics managers a single operating view across market rates, forecast direction, vessel compatibility, East Coast port constraints, idle time, contract scenarios, and operational risk. The primary Charter Analysis journey starts with a cargo requirement and ends with a transparent decision summary.

## User preferences

The requested product direction is premium enterprise maritime analytics: deep navy/deep blue, slate-white cards, restrained motion, high information density, semantic status colors, and no cartoonish or gaming-dashboard styling.

## Gotchas

- The frontend workflow supplies `PORT` and `BASE_PATH`; run the artifact through its managed workflow rather than starting Vite manually.
- If the backend is added later, keep the mock data service boundary intact so API wiring does not spread across page components.

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
