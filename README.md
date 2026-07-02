# hacking-by-the-sea-powerpoint-add-in
This is a powerpoint add-in we had to make during the Hacking By The Sea hackaton from the HZ HBO-ICT course

# Assignment:
Slidessibility

Track: Software Engineering

Contact: Tim Kardol & Valeria Stamenova

Number of teams: 1

Problem Statement: Dutch public-sector websites are legally required to meet WCAG 2.2 through EN 301 549 and the Tijdelijk besluit digitale toegankelijkheid overheid, yet accessibility is usually checked once, by hand, late in the process – and then quietly regresses with the next release. Developers experience it as a one-off audit event rather than an everyday engineering practice. The common scanners (axe-core, Lighthouse) are useful but catch only part of the picture and rarely live where regressions are actually introduced: the commit and the pull request.

Goal: Build tooling that treats accessibility as continuous engineering rather than an annual report. Lecturing slides should be accessible to everyone - Build a CLI that checks that inspects .pptx files directly via structure and flags accessibility defects. Output severity-ranked findings with fix hints, mirroring the format used for the web-based tracks.

Challenge: Instead of relying on a CLI that checks the exported PDF or the saved PPTX file, create a PowerPoint Add-in (in-app checking) that can highlight the issues in the presentation on the go.

Deliverables: Real developer tooling, not a one-off report: severity-ranked findings, actionable fix hints tied to specific WCAG success criteria, and a baseline mechanism so a team can adopt the gate without drowning in pre-existing debt. Include a sample integration against at least one real site and clear docs for wiring it into a pipeline.

User group: Screen-reader users, keyboard-only users, visually impaired users, and the developers who maintain these public-sector sites.

Inspiration: WCAG 2.2, axe-core, EN 301 549, DigiToegankelijk.nl, Playwright / Puppeteer, Lighthouse CI, GitHub Actions, accessibility tree / ARIA
