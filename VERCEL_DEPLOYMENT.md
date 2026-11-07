# Deploying to Vercel

Vercel detects the Flask application in `app.py`. Static assets are kept under
`public/static` so Vercel can serve them from its CDN; templates are included in
the Python function by `vercel.json`.

Before deploying, create a MySQL database and apply [`database/schema.sql`](database/schema.sql)
to it. Configure these environment variables in the Vercel project for every
deployment environment:

- `FLASK_SECRET_KEY`: a long, random secret used to sign sessions.
- `DB_BACKEND`: `mysql`.
- `DB_HOST`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME`: the database connection
  settings.

The application intentionally refuses to start on Vercel without these settings:
Vercel's function filesystem is ephemeral, so SQLite cannot reliably persist user
accounts or applications across invocations.
