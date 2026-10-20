"""Test that every Service Facts term URL resolves, for a browser and for a JSON-LD client.

Usage:
    python tools/test-term-urls.py                    # against https://w3id.org
    python tools/test-term-urls.py --base http://localhost:8080   # a local w3id.org server

For each term ID in docs/<industry>/<industry>.jsonld (every node ID and every
property used, in our namespace), it requests the ID twice and follows redirects:
  - browser Accept: must end at 200 text/html, and the page must have an element
    whose id is the term's fragment (so the browser lands on the definition);
  - application/ld+json: must end at 200 application/ld+json, and the file must
    use the term.
It also tests the root, and the frozen copy of the current version.
Exit code 1 if any check fails.
"""
import argparse
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W3ID = "https://w3id.org"
BROWSER = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
LDJSON = "application/ld+json"
UA = "servicefacts-term-test/0.1 (+https://github.com/wldm-gh/servicefacts)"


def fetch(url, accept, cache):
    key = (url, accept)
    if key not in cache:
        req = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                cache[key] = (r.status, r.headers.get("Content-Type", ""), r.geturl(), r.read().decode("utf-8"))
        except Exception as e:  # noqa: BLE001  (report every failure the same way)
            cache[key] = (getattr(e, "code", 0), "", url, str(e))
    return cache[key]


def terms(doc, prefix, ns):
    found = set()

    def walk(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k.startswith(prefix + ":"):
                    found.add(k.split(":", 1)[1])
                if k == "@id" and isinstance(v, str) and v.startswith(prefix + ":"):
                    found.add(v.split(":", 1)[1])
                walk(v)
        elif isinstance(x, list):
            for i in x:
                walk(i)
    walk(doc)
    return sorted(found)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=W3ID, help="w3id.org, or a local w3id.org server")
    ap.add_argument("--industry", default="legal")
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    path = os.path.join(ROOT, "docs", a.industry, f"{a.industry}.jsonld")
    with open(path, encoding="utf-8") as f:
        local = json.load(f)
    ns = local["@context"][a.industry]
    version = local["schema:version"]
    ids = terms(local, a.industry, ns)
    base_ns = ns.replace(W3ID, a.base.rstrip("/"))
    doc_url = base_ns.rstrip("#")

    cache, fails, rows = {}, 0, []

    def check(label, url, accept, want_type, test_body):
        nonlocal fails
        status, ctype, final, body = fetch(url, accept, cache)
        ok = status == 200 and want_type in ctype and test_body(body)
        fails += not ok
        rows.append(f"{'PASS' if ok else 'FAIL'}  {label:<55} {'browser' if accept == BROWSER else 'ld+json':<8} {status} {ctype.split(';')[0]:<20} {final}")

    check("/servicefacts/", f"{a.base.rstrip('/')}/servicefacts/", BROWSER, "text/html", lambda b: "Service Facts" in b)
    check("/servicefacts/", f"{a.base.rstrip('/')}/servicefacts/", LDJSON, "application/ld+json",
          lambda b: json.loads(b)["@id"] == f"{W3ID}/servicefacts")
    for v_url, label in [(doc_url, f"/servicefacts/{a.industry}"), (f"{doc_url}/{version}", f"/servicefacts/{a.industry}/{version}")]:
        check(label, v_url, BROWSER, "text/html", lambda b: f"v{version}" in b)
        check(label, v_url, LDJSON, "application/ld+json", lambda b: json.loads(b)["@id"] == ns.rstrip("#"))
    for t in ids:
        # The fragment never reaches the server; the browser keeps it after the redirect.
        check(f"{a.industry}:{t}", doc_url, BROWSER, "text/html", lambda b, t=t: re.search(rf'\bid="{re.escape(t)}"', b) is not None)
        check(f"{a.industry}:{t}", doc_url, LDJSON, "application/ld+json", lambda b, t=t: f'"{a.industry}:{t}"' in b)

    print("\n".join(rows))
    print(f"\n{len(ids)} terms, {len(rows)} checks against {a.base}: {len(rows) - fails} passed, {fails} failed.")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
