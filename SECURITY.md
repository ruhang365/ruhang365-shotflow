# Security policy

## Supported versions

Security fixes target the latest `0.x` Core release.

## Report privately

Use GitHub private vulnerability reporting. Do not put credentials, private generation links, real user media, local project paths, or exploit details in a public issue.

Include the affected version, operating system, synthetic reproduction, and impact.

## Core boundaries

- Core has no network client and collects no telemetry.
- Artifact paths must remain inside the active project.
- Project files store hashes and public-safe provider metadata, not credentials or account sessions.
- Pro is a separate future service and must consume the public ObservationPatch format.
