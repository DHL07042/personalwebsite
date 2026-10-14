# Website maintenance

Applies only to DHL07042/personalwebsite. CVs, manuscripts and application records have their own editors and approval paths.

## Review loop
1. Read the latest main commit, release.json, relevant files and previous PR. Compare the deployed site with that release; do not assume an attachment or older ZIP is current.
2. Record the owner's new requests, independently inspect the source/figures/public references, and distinguish facts, interpretations and missing evidence.
3. One editor per change set. Work on a branch and open a PR; never push main or merge without the owner's approval. Explain any proposed reversal of an approved decision.
4. Run the Checked-out files job on the PR. Review screenshots as well as the test report. A passing viewport test does not establish usability on every device or fast service on every network.
5. After an approved merge, inspect the Deployed site result and live release. Record the change IDs, evidence, tests and remaining decisions for the next editor. Another model's agreement is not factual evidence.

PR descriptions, comments, committed files and CI logs are public in this repository. Keep private correspondence, employment-clearance discussions and unpublished research review details outside the repository. Seven-day artifact retention is not seven-day retention of all repository history or logs.

## Stable structure and release
- Preserve page filenames and anchor IDs: gait-phase, initial-contact, force-sensing, cybathlon, experimental-systems, venture, J1–J5, C1, M1, T1.
- Preserve CNAME = daeholee.me. DNS/TLS configuration is separate from source changes; do not rewrite working DNS records based only on a timeout report.
- Change release.json, HTML site-release metadata and CSS/app.js cache keys together. Do not show the release identifier in the visitor-facing footer.
- The small theme bootstrap is inline before CSS to avoid a network fetch before body parsing. Its source is theme-init.js; copy that exact text into script#theme-bootstrap in every page when changing it. CI checks equality. Only app.js sets the js class after enhancement handlers are attached.
- Static HTML, CSS and native JavaScript; no analytics or service worker. Geist and Geist Mono are self-hosted under assets/fonts with their license. YouTube thumbnail requests remain external; players load on click.

## Approved design contract
- Default appearance: System, with no data-theme attribute in System mode. Preserve the three icon buttons and persistent preference.
- Preserve quiet links, small external-link icons, pill buttons, three Home project cards, timeline, and At a glance. Do not reintroduce a defensive Current employment block.
- Body 17–18px, navigation 17px, labels 16px, chips 13.6px, footer 16px. Reflow instead of shrinking text to fix wrapping. Protect short compound terms, not entire sentences.
- Research order: distance sensing (gait-phase, then initial-contact), instrumentation, WalkON/CYBATHLON, experimental systems, student-led project.
- Limitations once per study. Keep measured results distinct from individual contributions without repetitive disclaimers.
- Images open in a keyboard-accessible lightbox. Scientific plots and composite panels use contain; crop only ordinary photographs where no evidence is lost.
- Preserve the Samsung internship, exact YouTube titles, and the small Nerd Lab video loop with a pause control. Default motion must respect reduced-motion preferences.

## Evidence boundaries
- ADD: affiliation, title and dates only until the owner approves additional public wording.
- Preserve publication titles, author order and status. Separate journal articles, proceedings, presentations and manuscripts in preparation. Do not imply unrelated studies merely because entries are separate.
- T1 (ISPS 2021 presentation) and J1 (JKSPE 2026 article) are the same line of work; the site says so in one sentence ("first presented at ASME ISPS 2021"). Do not remove that lineage and do not add authorship commentary.
- Preserve WalkON Suit 4 in site prose. Published titles and quotations retain their original form; Roman/Arabic numeral variants alone are not different robots.
- Do not reframe preliminary comparisons as quantitative agreement, accuracy validation or clinical benefit without the relevant result.
- Do not add claims from an old research conversation to the current manuscript summary. Obtain the current approved research-status bridge for new numerical results.

## Media and provenance
- Use only owner-provided/approved photographs and diagrams. Existing assets are not a blanket license for new third-party materials. Do not recreate missing scientific axes or results with generated graphics.
- YouTube videos use the original AFN Pacific and CYBATHLON uploads via click-to-play players; do not download or rehost them. The Nerd Lab clip is an owner-supplied local MP4/WebM asset, not a YouTube file.
- gait-distance.webp and gait-phases.webp (crops of an unpublished PSAO analysis) stay off the rendered page. Their uncropped sources, and the other unused originals from the previous site, are kept in assets/src for reference.
- Project 01, part 1 uses three figures from the owner's ASME ISPS 2021 presentation deck [T1] (t1-shoe, t1-threshold, t1-phases). Captions cite [T1]; do not attribute them to J1.
- grf-results.webp is shown with the owner-supplied condition mapping (release 2026-10-14.7): Case I = virtual-spring pre-tuning off, Case II = weak, Case III = strong; the manuscript in preparation calls these FDL off/weak/strong. The caption states conditions only, not an effect.
- The M20 multi-panel photograph is not a decorative photo: display all panels. The thesis concept diagram uses (a) walking model, (b) flexion/extension, (c) stance/swing configurations.

## Checks
- PR: checked-out source on a local server. Main only: deployed site after release agreement.
- Check viewport widths including narrow phone, opened foldable, tablet, laptop and large desktop, both themes, enlarged text, theme persistence, no-JS/failed-JS navigation, and lightbox focus/closure.
- Green CI does not prove DNS/TLS correctness or complete video playback. Read the actual reports and flag untested scope.
- Network reports should distinguish DNS/connect/TLS/server response from browser parsing/resources. A fast overseas runner does not disprove a slow visit on the owner's network.
