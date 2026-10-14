# Website maintenance

Applies only to DHL07042/personalwebsite, not to CV or application-document editing.

## Source of truth and collaboration
- Read the current `main` commit and the files you will edit before making changes. The deployed website is the visual review surface; the commit diff is the record of what changed.
- One active editor per change set. Work from a branch and open a pull request; the "Checked-out files" job validates the branch itself, so a red check on a PR means the PR is broken, not that the deployment is pending. After a merge to main, the "Deployed site" job waits for GitHub Pages and validates the live site.
- Keep page filenames and anchor IDs stable: `gait-phase`, `initial-contact`, `force-sensing`, `cybathlon`, `experimental-systems`, `venture`, `J1`–`J5`, `C1`, `M1`, `T1`. Keep `CNAME` as `daeholee.me` unless the owner asks for a domain change.
- When site files change, bump `release.json` and the matching `site-release` meta and `?v=` query strings on `styles.css`, `app.js` and `theme-init.js`.
- Keep the site dependency-light: static HTML, one stylesheet, two small scripts. Fonts come from Google Fonts with system fallbacks; nothing else is loaded from third parties until a viewer starts a video.

## Design rules
- Appearance follows the system by default; the header control stores an explicit Light / Dark / System choice in `localStorage` (`dhl-portfolio-theme-v1`). In System mode the `data-theme` attribute is absent and `prefers-color-scheme` applies.
- Links: no underline + blue + arrow stacks. Running-text links use `.prose a` (hairline underline); external links add `.ext` for the small glyph; actions are `.btn` pills.
- Type sizes are fluid (`clamp()`); check 320, 390, 768, 820, 1024 and 1440 px in both themes before reporting.
- Hedge once: state the number of participants and the test condition one time per study, in plain words. Do not restate that a result belongs to the team or that the site omits work details.

## Content boundaries
- Current employment appears as affiliation, title and dates only. Work-specific information is not published.
- Keep the distinction between individual contributions and team results, and between journal articles, conference papers, manuscripts in preparation and presentations. Do not invent responsibilities, statuses or results.
- Do not publish draft CV PDFs, private review notes, source archives, credentials or internal screenshots.

## Media
- Videos are click-to-play: the page shows the host's thumbnail and creates the YouTube player only when a viewer clicks. Current IDs: `jl-wEJFMYxY`, `QEO1ogYnKEI`, `ytGybgT78Us` (AFN Korea samples) and `mIbaOjXYxHs` (CYBATHLON 2020 broadcast). No video file is hosted here.
- The research-page figure is an original SVG schematic, not data from a paper.
- Photographs go in `assets/img/` only when the owner supplies them: research photos cropped 4:3, personal photos 1:1, each with a caption; keep files under about 300 KB.
