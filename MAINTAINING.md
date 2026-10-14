# Website maintenance

Applies only to DHL07042/personalwebsite, not to CV or application-document editing.

## Source of truth and collaboration
- Read the current `main` commit and the files you will edit before making changes. The deployed website is the visual review surface; the commit diff is the record of what changed.
- Use one active editor for a change set. Work from a fresh branch for substantive changes; review and fast-forward/merge without force-pushing. Do not overwrite a concurrent change from another editor.
- Keep stable page filenames and research/publication anchor IDs. Keep `CNAME` as `daeholee.me` unless the owner explicitly requests a domain change.
- Bump `release.json` and the matching `site-release` metadata/asset query strings. Confirm that the live release matches the intended commit before reporting completion.
- Keep the site dependency-light. Current files are static HTML, CSS and small native JavaScript. No analytics or backend are required.

## Content boundaries
- State current employment separately from academic research. Do not invent project responsibilities, publication statuses, research results or media ownership.
- Preserve the distinction between individual contributions and team results, and between published articles, manuscripts in preparation and presentations.
- Do not publish nonpublic work details, draft CV PDFs, private review notes, source archives, credentials, or internal screenshots.
- A public webpage, a local file, or a published paper is not by itself a license to reproduce an image.

## Media
- The three AFN videos were already linked as filming/editing samples in the owner's portfolio. They are presented via the original AFN Pacific YouTube uploads, not copied or rehosted. This does not assert sole copyright ownership or clear third-party material in the videos.
- Current embedded IDs: `jl-wEJFMYxY`, `QEO1ogYnKEI`, `ytGybgT78Us`.
- The CYBATHLON broadcast remains an external link. Do not download its footage or use its frames as owned photographs.
- Add photographs only after the owner provides publication permission and identifies the source. No profile photograph has been approved for this release.
- The current decorative background is original CSS, not a stock photograph or experimental plot. No font binaries are stored in the repository.

## Checks
- Test 320px and wider layouts, keyboard navigation, 200% text, and both themes.
- Test Light/Dark/System selection, reload persistence, inter-page persistence, and OS changes while System is selected.
- Without JavaScript, all five pages and normal links remain readable. A blocked video must retain an original-source link.
- A green build/diagnostic job is not a certificate audit. Read the actual DNS/TLS flags and hostnames in diagnostic results.
- DNS/TLS changes are distinct from website-source changes. Do not repeatedly rewrite working DNS records to fix a certificate problem.
