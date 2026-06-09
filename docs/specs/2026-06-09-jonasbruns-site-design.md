# Design — jonasbruns.com personal site

**Date:** 2026-06-09
**Status:** Approved

## Goal

Replace the unfinished WordPress site at `jonasbruns.com` with a simple, fast,
good-looking personal homepage about Jonas Bruns.

## Decisions

- **Hosting:** the existing Hetzner VPS (`168.119.247.89`), served by the single Caddy
  instance already running in the `whatsapp-mcp` triage stack (it owns ports 80/443).
- **Stack:** plain static HTML + CSS. No framework, no build step, no dependencies.
- **Scope:** one scrollable page with four sections — Hero, About, Work & projects,
  Links & contact.

## Structure

```
index.html        single page, four sections
styles.css        responsive; light + dark via prefers-color-scheme
assets/           favicon.svg (JB monogram); TODO: photo, og-image
CLAUDE.md         project + infra/deploy context
README.md
docs/specs/       this document
```

## Look & feel

Warm, minimal, typographic. Serif display headings + system sans body, generous
whitespace, one terracotta accent, fully responsive, light/dark aware. Deliberately not
generic-AI-looking. Easily re-themed via CSS custom properties in `:root`.

## Hosting & deploy

- Repo cloned on the VPS at `/opt/jonasbruns-site`; deploy = `git pull`.
- Serving config lives in the **`whatsapp-mcp` repo** (shared `Caddyfile` +
  `docker-compose.yml`): a `jonasbruns.com, www.jonasbruns.com { file_server }` block and a
  read-only bind-mount `/opt/jonasbruns-site:/srv/jonasbruns-site:ro` into the caddy
  container. Caddy auto-issues TLS once DNS resolves to the VPS.
- **Tradeoff (accepted):** content lives in this repo; routing/TLS lives in the triage
  repo — light cross-repo coupling, documented in both `CLAUDE.md` files. Could later be
  decoupled by promoting Caddy to a standalone shared proxy.

## DNS

At Strato: repoint apex `jonasbruns.com` A-record from "STRATO Standard" to
`168.119.247.89`, and add a `www` A-record to the same IP. Retires the WordPress site.

## Testing

Light, as fits a static page: HTML/link sanity check + manual visual review in the
browser (desktop + mobile widths, light + dark).

## Out of scope (YAGNI)

Blog, CMS, analytics, contact form/backend, build pipeline. Add later only if a real need
appears.
