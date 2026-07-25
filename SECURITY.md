# Security Policy

## Supported version

Only the commit identified by the production service's `X-Source-Commit`
header is considered actively deployed and supported.

## Report a vulnerability

Use GitHub's private vulnerability reporting or Security Advisory interface
for this repository. Do not open a public issue for a suspected vulnerability.

Include:

- affected endpoint and commit;
- reproduction steps using synthetic data;
- expected and observed behavior;
- potential impact;
- suggested mitigation, if available.

Never include API keys, access tokens, production request bodies, or personal
birth data. Credentials exposed in a report should be revoked immediately.
