# Contributing

This knowledge base is a collaborative effort. Contributions from glider operators, pilots, scientists, and engineers are welcome — whether that's fixing a typo, adding a procedure step, or writing a new guide from scratch.

---

## Ways to Contribute

- **Fix or improve existing content** — correct an outdated procedure, clarify a step, add a missing warning
- **Add to the Slocum One-Pager** — drop in a quick-reference command or reminder you use regularly
- **Expand a checklist** — add items based on hard-won field experience
- **Write a new guide** — document a procedure that isn't covered yet
- **Report an issue** — if something is wrong or missing, open a GitHub Issue

---

## Editing an Existing Page

The quickest way is directly on GitHub:

1. Navigate to the page on the live site
2. Click **Edit this page** (pencil icon, top right)
3. Make your changes in the GitHub editor
4. Submit a pull request with a short description of what you changed and why

---

## Adding New Content Locally

### 1. Set up the environment

```bash
git clone https://github.com/e-abdi/Glider-Operation-Best-Practices.git
cd Glider-Operation-Best-Practices

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Create a branch

```bash
git checkout -b your-name/short-description
```

### 3. Make your changes

All content lives under `docs/`. Each topic follows this structure:

```
docs/<topic>/
├── index.md               ← topic landing page
├── guides/
│   └── <guide-name>.md
└── checklists/
    └── checklist.md
```

Run the local dev server to preview as you write:

```bash
mkdocs serve
```

### 4. Register new pages in `mkdocs.yml`

If you add a new file, add it to the `nav:` section of `mkdocs.yml` so it appears in the sidebar.

### 5. Open a pull request

Push your branch and open a PR on GitHub. Include:
- What you added or changed
- Why (source document, field experience, correction of a known error)
- If it's a procedure change, note whether it has been reviewed by another operator

---

## Content Guidelines

- **Be specific.** Vague guidance is less useful than a concrete step.
- **Cite your sources.** If a procedure comes from a manual, OceanGliders best practices document, or institutional SOP, say so.
- **Use admonitions for safety-critical items.** Wrap anything that could damage equipment or endanger personnel in a `!!! danger` or `!!! warning` block.
- **Keep checklists actionable.** Each checkbox item should be a discrete, verifiable action — not a topic heading.
- **No lorem ipsum.** Every page should contain real, usable content. Placeholder text should be replaced before merging.

---

## File Naming

- Use lowercase with hyphens: `slocum-one-pager.md`, `deployment-checklist.md`
- Keep names short and descriptive
- Match the nav label in `mkdocs.yml` to the `title:` in the file's front matter

---

## Questions

Open a [GitHub Issue](https://github.com/e-abdi/Glider-Operation-Best-Practices/issues) or reach out to the repository maintainer.
