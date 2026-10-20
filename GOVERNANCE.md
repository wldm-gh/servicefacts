# Governance

## Who looks after Service Facts

[WLDM](https://wldm.io/) maintains Service Facts. Two maintainers approve changes:

- WLDM, GitHub [@wldm-gh](https://github.com/wldm-gh), <peter@wldm.io>
- Peter (WLDM), GitHub [@growsontrees](https://github.com/growsontrees)

The same two people look after the `https://w3id.org/servicefacts/` redirect.

## Term IDs

- Pattern: `https://w3id.org/servicefacts/<industry>#<Term>`.
- No company name, version or status goes in a term ID.
- A term ID is never changed and never deleted.
- A replaced term stays in the file. It is marked `owl:deprecated true` and `schema:supersededBy` its replacement.
- If schema.org adds a term with the same meaning, our term is marked `schema:supersededBy` the schema.org term. Pages keep both for one year.

## Versions

- 0.x means draft. 1.0 means stable.
- Each release is a git tag (`<industry>-v<version>`, for example `legal-v0.1`) and a GitHub release.
- Each release gets a frozen copy at `https://w3id.org/servicefacts/<industry>/<version>`.
- Before each release: the checker passes with 0 errors, and every term URL is tested with a browser `Accept` header and a JSON-LD one.

## How a change is made

1. Anyone opens a GitHub issue: the fact, the buyer question it answers, and why no schema.org property fits.
2. A maintainer replies within 14 days.
3. A change is merged when both maintainers approve it.
4. Before 1.0, the method terms (`priority`, `module`, `answersQuestion` and the others) move to one shared namespace, `https://w3id.org/servicefacts/profile#`.

## If WLDM stops

WLDM will hand the repository and the w3id.org maintainer role to a willing party, or point the redirect at the last frozen copy. The licence (CC BY 4.0) lets anyone carry the vocabulary on.
