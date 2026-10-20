# Service Facts

Open vocabularies for the facts buyers ask about professional services.

schema.org describes businesses well, but it cannot say many facts that decide a buyer's choice. For a law firm, that is who it acts for, how it charges, which tribunal hears a matter, which law governs it, and how long a legal deadline is. Service Facts adds a small, checked set of terms for each industry, on top of schema.org.

- Docs: <https://w3id.org/servicefacts/> (site: <https://wldm-gh.github.io/servicefacts/>)
- Licence: [CC BY 4.0](LICENSE)
- Maintainer: [WLDM](https://wldm.io/), <peter@wldm.io>

## Vocabularies

| Industry | Namespace | Version | Docs | Files |
|---|---|---|---|---|
| Legal services | `https://w3id.org/servicefacts/legal#` (prefix `legal:`) | 0.1, draft | [docs](https://wldm-gh.github.io/servicefacts/legal/) | [JSON-LD](docs/legal/legal.jsonld), [Turtle](docs/legal/legal.ttl) |

Version 0.x is a draft and can still change. Term IDs never change and are never deleted.

## Use it on a page

Write the prefix inline. Never load a remote context file: if it cannot load, JSON-LD processing stops.

```json
{
  "@context": ["https://schema.org", {"legal": "https://w3id.org/servicefacts/legal#"}],
  "@type": "Service",
  "name": "Security of payment claims",
  "audience": {"@type": "BusinessAudience", "audienceType": "Subcontractors"},
  "legal:actsFor": {"@id": "https://w3id.org/servicefacts/legal#PartyRoles-subcontractor"}
}
```

Three rules:

1. Use standard schema.org first. Use a Service Facts term only where schema.org has no home.
2. Write every fact as visible text on the page as well. Search engines and AI engines quote text, not hidden markup.
3. Where a standard property can carry part of the fact, publish it too (the docs say which one).

## How the IDs work

Each term ID is a hash ID, for example `https://w3id.org/servicefacts/legal#actsFor`. [w3id.org](https://w3id.org/) is a permanent-ID redirect service run by a W3C community group. It sends a browser to the docs page, and a JSON-LD or Turtle client to the vocabulary file. If these files ever move, only the redirect changes. Pages that use the terms do not change.

## Build

```
pip install rdflib
python build/build.py
python tools/check-profile.py docs/legal/legal.jsonld
```

Edit the term lists in `build/legal.py`, never the generated files in `docs/`. The checker must report 0 terms that do not exist or do not fit, and 0 custom terms with broken references.

After each release, test that every term URL resolves, for a browser and for a JSON-LD client:

```
python tools/test-term-urls.py
```

## Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) and [GOVERNANCE.md](GOVERNANCE.md). Changes are listed in [CHANGELOG.md](CHANGELOG.md).
