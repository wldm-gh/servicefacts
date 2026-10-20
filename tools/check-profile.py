"""Check an industry schema profile against the live schema.org vocabulary.

A "profile" is a JSON-LD file in the ArcherEDU shape: an @graph of rdf:Property
(and optionally rdfs:Class) nodes with schema:domainIncludes / schema:rangeIncludes.

It reports:
  1. schema.org terms the profile uses that do not exist, or do not fit the type.
  2. schema.org terms that are only in "pending" (usable, but not core).
  3. Custom terms whose domain/range points at a type that does not exist.
  4. Custom terms with a plain Text/Boolean range (cannot link to other data).
  5. Standard schema.org properties on the anchor type(s) that the profile does
     not use. Check each one before you invent a custom property.

Usage:
  python tools/check-profile.py <profile.jsonld> [--schemaorg <schemaorg-current-https.jsonld>] [--depth 1]

Without --schemaorg the latest vocabulary is downloaded into memory (nothing is saved).
"""
import argparse
import collections
import json
import sys
import urllib.request

SCHEMAORG_URL = "https://schema.org/version/latest/schemaorg-current-https.jsonld"
SCHEMA_NS = ("https://schema.org/", "http://schema.org/")
# Parents too generic to list in the "unused standard properties" report.
GENERIC = {"Thing", "CreativeWork", "Intangible"}
WEAK_RANGES = {"Text", "Boolean", "URL"}


def as_list(x):
    if x is None:
        return []
    return x if isinstance(x, list) else [x]


def load_schemaorg(path):
    if path:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    else:
        with urllib.request.urlopen(SCHEMAORG_URL, timeout=60) as r:
            data = json.loads(r.read().decode("utf-8"))
    nodes = {}
    for n in data["@graph"]:
        if n["@id"].startswith("schema:"):
            nodes[n["@id"][7:]] = n
    return nodes


def ids(value):
    out = []
    for v in as_list(value):
        i = v["@id"] if isinstance(v, dict) else v
        if isinstance(i, str) and i.startswith("schema:"):
            out.append(i[7:])
    return out


def ancestors(t, so):
    seen, todo = set(), [t]
    while todo:
        c = todo.pop()
        if c in seen or c not in so:
            continue
        seen.add(c)
        todo.extend(ids(so[c].get("rdfs:subClassOf")))
    return seen


def is_pending(n):
    return "pending" in json.dumps(n.get("schema:isPartOf", ""))


def local(term, prefixes):
    """Return ('schema', 'name') or ('custom', 'prefix:name')."""
    if ":" in term and not term.startswith("http"):
        pfx, name = term.split(":", 1)
        base = prefixes.get(pfx, "")
        if pfx == "schema" or base in SCHEMA_NS:
            return "schema", name
        return "custom", term
    for ns in SCHEMA_NS:
        if term.startswith(ns):
            return "schema", term[len(ns):]
    return "custom", term


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("profile")
    ap.add_argument("--schemaorg")
    ap.add_argument("--depth", type=int, default=1,
                    help="how many parent types to include in the 'unused standard properties' list")
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    so = load_schemaorg(a.schemaorg)
    with open(a.profile, encoding="utf-8") as f:
        prof = json.load(f)
    prefixes = {k: v for k, v in as_list(prof.get("@context"))[0].items() if isinstance(v, str)} \
        if prof.get("@context") else {}
    graph = prof.get("@graph", [])

    problems, pending, weak, custom_bad = [], [], [], []
    used_schema, anchors = set(), collections.Counter()

    for n in graph:
        kind, term = local(n["@id"], prefixes)
        doms = [local(d, prefixes) for d in (x["@id"] if isinstance(x, dict) else x
                                            for x in as_list(n.get("schema:domainIncludes")))]
        rngs = [local(r, prefixes) for r in (x["@id"] if isinstance(x, dict) else x
                                            for x in as_list(n.get("schema:rangeIncludes")))]
        for k, d in doms:
            if k == "schema":
                anchors[d] += 1
        if kind == "schema":
            used_schema.add(term)
            s = so.get(term)
            if not s:
                problems.append(f"{term}: does not exist in schema.org")
                continue
            if is_pending(s):
                pending.append(term)
            if s.get("@type") == "rdf:Property":
                real_dom = set(ids(s.get("schema:domainIncludes")))
                for k, d in doms:
                    if k == "schema" and not (ancestors(d, so) & real_dom):
                        problems.append(f"{term}: not valid on {d} (schema.org domain: {', '.join(sorted(real_dom))})")
        else:
            for k, t in doms + rngs:
                if k == "schema" and t not in so:
                    custom_bad.append(f"{term}: refers to schema:{t}, which does not exist")
            if rngs and all(k == "schema" and t in WEAK_RANGES for k, t in rngs):
                weak.append(f"{term} ({'/'.join(t for _, t in rngs)})")
            is_term = "DefinedTerm" in json.dumps(n.get("@type"))
            if is_term and "DefinedTermSet" not in json.dumps(n.get("@type")) and not n.get("schema:description"):
                custom_bad.append(f"{term}: value has no schema:description")
            elif not is_term and not n.get("rdfs:comment"):
                custom_bad.append(f"{term}: no definition (rdfs:comment)")

    print(f"Profile: {a.profile}")
    print(f"Terms: {len(graph)}  (schema.org: {len(used_schema)}, custom: {len(graph) - len(used_schema)})")
    print(f"Anchor types: {dict(anchors.most_common())}\n")

    print(f"1. schema.org terms that do not exist or do not fit ({len(problems)})")
    for p in problems:
        print("   -", p)
    print(f"\n2. schema.org terms only in 'pending' ({len(pending)}): {', '.join(sorted(pending)) or '-'}")
    print(f"\n3. Custom terms with broken references or no definition ({len(custom_bad)})")
    for p in custom_bad:
        print("   -", p)
    print(f"\n4. Custom terms with only Text/Boolean/URL range ({len(weak)}) - consider a real type so values can link")
    for p in weak:
        print("   -", p)

    print(f"\n5. Standard schema.org properties on the anchor types that the profile does not use")
    for anchor, _ in anchors.most_common():
        if anchor not in so:
            continue
        chain, level, frontier = [anchor], 0, [anchor]
        while level < a.depth:
            nxt = [p for t in frontier for p in ids(so[t].get("rdfs:subClassOf")) if p in so]
            chain += nxt
            frontier, level = nxt, level + 1
        chain = [c for c in chain if c not in GENERIC]
        unused = sorted(t for t, s in so.items()
                        if s.get("@type") == "rdf:Property"
                        and set(ids(s.get("schema:domainIncludes"))) & set(chain)
                        and t not in used_schema
                        and not s.get("schema:supersededBy"))
        print(f"   {anchor} (+ parents {chain[1:] or '-'}): {len(unused)}")
        print("     " + ", ".join(unused))


if __name__ == "__main__":
    main()
