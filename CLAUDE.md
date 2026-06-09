# jonasbruns.com — personal site

Personal homepage for **Jonas Bruns**, served at `https://jonasbruns.com`.

## What this is

A single static page about Jonas. Deliberately tiny: no framework, no build step,
no dependencies. Just hand-written HTML + CSS that Caddy serves as files.

## Stack & structure

- **Plain static HTML + CSS.** No Node, no bundler, no JS framework. (A few lines of
  vanilla JS are fine if ever needed — e.g. the footer year.)
- Files:
  - `index.html` — the whole page (Hero → About → Work & projects → Links/contact)
  - `styles.css` — all styling; responsive; supports light + dark via `prefers-color-scheme`
  - `assets/` — favicon, photo, og-image
  - `docs/specs/` — the approved design doc this was built from

## Preview locally

No build. Either open `index.html` directly, or for correct relative paths:

```bash
python -m http.server 8000
# then open http://localhost:8000
```

## Conventions

- Keep it dependency-free and fast. Don't add a framework or build step without a real reason.
- Semantic, accessible HTML (landmarks, alt text, focus states, good contrast).
- Edit content in `index.html`; placeholders are marked with `<!-- TODO -->` comments.

## Hosting & deploy

Served by the **single Caddy instance already running on the Hetzner VPS** — the one in
the `whatsapp-mcp` triage stack. That Caddy owns ports 80/443 on the box, so it is the
edge for every site on it, including this one.

**Infra facts:**
- **VPS:** Hetzner, Ubuntu 26.04, public IP **168.119.247.89**.
- **DNS:** registrar/DNS is **Strato**. Apex `jonasbruns.com` and `www` A-records point
  at the VPS IP. (Historically the apex pointed at Strato's WordPress hosting — now retired.)
- **TLS:** automatic via Caddy + Let's Encrypt once DNS resolves to the VPS.

**Deploy flow:**
1. This repo is cloned on the VPS at **`/opt/jonasbruns-site`**.
2. Push to `origin main` here → on the VPS `cd /opt/jonasbruns-site && git pull`.
3. No restart needed — Caddy serves the files live.

**⚠️ Cross-repo coupling (important):** the *serving config* for this site does NOT live
in this repo. It lives in the **`whatsapp-mcp` repo** (`/opt/whatsapp-mcp`), which holds
the shared `Caddyfile` and `docker-compose.yml`. Serving this site requires, in that repo:
- a Caddy site block:
  ```
  jonasbruns.com, www.jonasbruns.com {
      root * /srv/jonasbruns-site
      file_server
      encode gzip
  }
  ```
- a read-only bind-mount of the site into the caddy container, in `docker-compose.yml`:
  ```
  - /opt/jonasbruns-site:/srv/jonasbruns-site:ro
  ```
- then `docker compose up -d caddy` to reload.

So: **content changes** = this repo. **Serving/TLS/routing changes** = the `whatsapp-mcp` repo's Caddyfile.
