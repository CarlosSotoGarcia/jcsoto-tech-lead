# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is **not a software project** — there is no source code, build system, package manifest, or test
suite. It is Juan Carlos Soto García's personal repository of professional-profile documents: a CV, and
technical-profile writeups summarizing his work history and skills, generated from analysis of his actual
work (git history across other repositories, Jira, GitHub, Claude Code session logs, etc.).

There are no build, lint, or test commands to run here.

## Structure

- [README.md](README.md) — one-line repo description/tagline.
- [experiencia/](experiencia/) — professional profile documents:
  - `CV Juan Carlos Soto García.pdf` — CV.
  - `PERFIL-TECNICO.md` — technical profile centered on his role at CXC (LenderHub/Nuevos Negocios
    platform): a Tech Lead / architect role spanning FastAPI backend, Angular micro-frontends, and
    Terraform/GCP infrastructure, plus MR-integration and engineering-automation metrics.
  - `perfil-tecnico-carlos-soto.md` — broader technical profile covering his own SaaS ventures under
    Novex Dynamics (Zity, FluxV2, Flux, Signalink, ZenStock, etc.) and consulting work, derived from his
    personal GitHub account.
- [itz/](itz/) — unrelated personal/administrative document (a university thesis-extension form), not
  part of the professional-profile material.

## Working with this repository

- Content is written in Spanish; preserve that unless asked otherwise.
- These documents follow a stated methodology of only including **verifiable, evidence-backed claims**
  (sourced from git history, Jira, GitHub, and similar), with explicit "Limitaciones declaradas" /
  limitations sections. When editing or extending them, keep that evidentiary standard — don't add
  claims, metrics, or achievements that aren't backed by a stated source.
- Numbers, dates, and metrics in these files (commit counts, MR counts, repo lists, dates) are
  point-in-time snapshots tied to a stated "corte"/cutoff date in each document. Treat them as historical
  data, not something to silently recompute or extrapolate.
