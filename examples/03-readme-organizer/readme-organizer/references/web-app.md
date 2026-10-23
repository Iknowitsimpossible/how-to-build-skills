# Template: Web app / website

A visitor wants to know: what does it look like, can I try it live, and how do I run it locally?

## Skeleton

````markdown
# Project Name

One sentence: what the site/app is and who it is for.

**Live demo:** https://...   <!-- only if a deploy URL is confirmed -->

![Screenshot](docs/screenshot.png)

## What it does

A short paragraph on the problem it solves and how it works.

- Key feature 1 (strongest selling point first)
- Key feature 2
- Key feature 3

Built with: Framework, Language, Database/Hosting.

## Installation

Requirements: Node.js 20+ (or Python 3.x, etc.)

```bash
git clone https://github.com/user/repo.git
cd repo
npm install
```

If environment variables are needed:

```bash
cp .env.example .env
```

Then fill in `.env` (explain each variable briefly, never include real values).

## Usage

```bash
npm run dev
```

Open http://localhost:PORT in your browser. Describe the main thing to try first.

## Deployment   <!-- optional -->
````

## Type-specific notes

- **Live demo first.** If the project is deployed (look for `homepage` in package.json, a CNAME file, GitHub Pages workflow, vercel/netlify config, or a URL in the repo description), put the link right under the title. That's what most visitors click.
- **Port:** take it from the dev server config or script (Vite defaults to 5173, Next/CRA to 3000, Flask to 5000) and confirm it from config if set.
- **Static sites** (plain HTML/CSS/JS, no build step): Installation becomes "clone and open `index.html`" or "serve with `python -m http.server`". Don't invent an npm step.
- **Full-stack apps:** if frontend and backend run separately, give each its own numbered step in Usage, in the order they must start.
- **Environment variables:** list each variable from `.env.example` with one line on what it's for and where to get it. Never copy real secrets from a committed `.env`. If you find one, warn the user that it is committed.
