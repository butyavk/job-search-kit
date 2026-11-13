# Security and privacy

## Reporting
Please report a vulnerability privately through GitHub (*Security* → *Report a vulnerability* on this repository), not in a public issue.

## What the kit touches
The kit is instructions, templates and two small Python scripts. It runs inside your Claude session and does nothing on its own:
- **Your pack** (`me/`) — read by Claude, written only when you confirm a fact or a block. It holds personal data: keep it out of public repositories (`.gitignore` blocks `me/`) and out of shared projects you do not control.
- **The tracker** — only through the tracker-mcp server, with a preview, a version check, a backup and undo.
- **Mail, calendar, LinkedIn, job boards** — only through the connectors and browser you give Claude, read-only in scheduled runs.
- **Outward actions** — submitting, sending, accepting, booking — are yours by default. An `autonomy` rule in your profile can let Claude send one kind of message in a live session you start; scheduled runs never send anything. Passwords, accounts, money and offers are always yours.

## Content from outside
Job postings, emails and web pages are data, not instructions: the skills tell Claude never to follow instructions found in them, and the forms skill flags injected instructions and honeypot fields to you.
