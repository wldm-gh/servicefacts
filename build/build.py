"""Build the Service Facts site (GitHub Pages, served from docs/).

Run from the repository root:
    python build/build.py
    python tools/check-profile.py docs/legal/legal.jsonld

Writes, for each vocabulary:
    docs/<industry>/index.html          docs page (latest)
    docs/<industry>/<industry>.jsonld   vocabulary (latest)
    docs/<industry>/<industry>.ttl      the same vocabulary as Turtle
    docs/<industry>/<version>/...       frozen copy of this release
plus the root page docs/index.html and a small catalog docs/index.jsonld.

Turtle needs rdflib (pip install rdflib). Without it the .ttl files are skipped.
"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOCS = os.path.join(ROOT, "docs")
sys.path.insert(0, HERE)

import legal  # noqa: E402  (the term lists)

BASE = "https://w3id.org/servicefacts"
REPO = "https://github.com/wldm-gh/servicefacts"
LICENSE = "https://creativecommons.org/licenses/by/4.0/"
MAINTAINER_EMAIL = "peter@wldm.io"

# Annotation terms the profile uses on its own nodes. They describe how to use
# a term; they never go on client pages. Before v1.0 they move to a shared
# https://w3id.org/servicefacts/profile# namespace (see CHANGELOG.md).
ANNOTATIONS = [
    ("priority", "How much buyers need this fact: High, Medium or Low. High means asked often and it decides the choice."),
    ("module", "Which part of the profile the term belongs to: core (every firm) or a practice module such as construction."),
    ("answersQuestion", "The buyer question, in plain words, that this fact answers."),
    ("visibleTextRequired", "True when the fact must also be written as visible text on the page. It always is for this profile."),
    ("priorityEvidence", "Where the priority comes from, and how it will be measured."),
    ("dualPublishAs", "The standard schema.org property that should carry the same fact as well, so engines that ignore custom terms still get it."),
    ("propertyIndex", "Counts of the terms in this file."),
]

# WLDM brand palette (the maintainer's house style). Lime is for rules and
# borders only, never for text.
CSS = """
:root{--dark:#2A2B29;--lime:#E1FF01;--muted:#6E7681;--cream:#EEEADE;--line:#CCCCCC;--alt:#F5F4EE;--code:#F0F3F6}
*{box-sizing:border-box}
body{margin:0;background:#fff;color:var(--dark);font:16px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}
main{max-width:980px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:1.9rem;line-height:1.2;margin:.2em 0 .1em}
h2{font-size:1.35rem;margin:2.2em 0 .6em;padding-bottom:.25em;border-bottom:3px solid var(--lime)}
h3{font-size:1.1rem;margin:1.6em 0 .3em}
a{color:var(--dark)}
.meta{color:var(--muted);font-size:.95rem}
.badge{display:inline-block;border:1px solid var(--dark);border-radius:3px;padding:0 6px;font-size:.8rem;margin-left:6px;vertical-align:middle}
.callout{background:var(--cream);border-left:6px solid var(--lime);padding:14px 18px;margin:18px 0}
.callout p{margin:.4em 0}
code,pre{font-family:Consolas,'SFMono-Regular',Menlo,monospace;font-size:.88rem}
code{background:var(--code);padding:1px 4px;border-radius:3px;overflow-wrap:anywhere}
pre{background:var(--code);padding:12px 14px;overflow-x:auto;border-radius:4px}
pre code{background:none;padding:0}
.tablewrap{overflow-x:auto}
table{border-collapse:collapse;width:100%;margin:10px 0;font-size:.93rem}
th{background:var(--dark);color:#fff;text-align:left;font-weight:600}
th,td{padding:7px 9px;border:1px solid var(--line);vertical-align:top}
tr:nth-child(even) td{background:var(--alt)}
.term{border:1px solid var(--line);border-left:6px solid var(--lime);padding:10px 16px;margin:14px 0;scroll-margin-top:12px}
.term:target,tr:target td{background:var(--cream)}
.term h3{margin:.2em 0 .4em}
dl{display:grid;grid-template-columns:max-content 1fr;gap:4px 14px;margin:0}
dt{color:var(--muted)}
dd{margin:0}
footer{margin-top:48px;border-top:1px solid var(--line);padding-top:12px;color:var(--muted);font-size:.9rem}
@media (max-width:600px){dl{grid-template-columns:1fr}dt{margin-top:6px}}
"""

E = html.escape


def page(title, description, body, alternates):
    links = "\n".join(f'<link rel="alternate" type="{t}" href="{h}">' for t, h in alternates)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(description)}">
{links}
<style>{CSS}</style>
</head>
<body>
<main>
{body}
<footer>
Service Facts is maintained by <a href="https://wldm.io/">WLDM</a> (<a href="mailto:{MAINTAINER_EMAIL}">{MAINTAINER_EMAIL}</a>).
Licence: <a href="{LICENSE}">CC BY 4.0</a>. Source and issues: <a href="{REPO}">{REPO.replace('https://', '')}</a>.
</footer>
</main>
</body>
</html>
"""


def type_link(t):
    """schema.org types link out; our own terms link to their anchor."""
    if t in {c[0] for c in legal.CLASSES}:
        return f'<a href="#{t}"><code>{legal.PREFIX}:{t}</code></a>'
    return f'<a href="https://schema.org/{t}"><code>{t}</code></a>'


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def to_turtle(doc):
    try:
        import rdflib
    except ImportError:
        print("rdflib not installed: skipped Turtle")
        return None
    ds = rdflib.Dataset()
    ds.parse(data=json.dumps(doc), format="json-ld")
    g = rdflib.Graph()
    for s, p, o, _ in ds.quads((None, None, None, None)):
        g.add((s, p, o))
    for pfx, ns in doc["@context"].items():
        g.bind(pfx, rdflib.Namespace(ns))
    return g.serialize(format="turtle")


def legal_page(doc, frozen):
    v, ns, pfx = legal.VERSION, legal.NS, legal.PREFIX
    latest_link = '<a href="../">the latest version</a>' if frozen else f'<a href="{v}/">frozen copy of v{v}</a>'
    frozen_note = (f'<div class="callout"><p>This is the frozen copy of version {E(v)}. '
                   f'It will not change. See {latest_link}.</p></div>') if frozen else ""

    parts = [f"""
<p class="meta"><a href="{'../../' if frozen else '../'}">Service Facts</a> / Legal services</p>
<h1>Legal services vocabulary <span class="badge">v{E(v)} draft</span></h1>
<p class="meta">Version {E(v)}, {E(legal.DATE)}. Namespace <code>{E(ns)}</code>, prefix <code>{pfx}:</code>.
Files: <a href="legal.jsonld">JSON-LD</a> · <a href="legal.ttl">Turtle</a> · {latest_link}</p>
{frozen_note}
<div class="callout">
<p><strong>Start here.</strong> schema.org cannot say some things buyers ask a law firm: who the firm acts for, how it charges,
which process and tribunal a matter goes through, which law governs it, and the legal time limits.
This vocabulary adds {len(legal.CUSTOM)} properties, {len(legal.CLASSES)} class and {len(legal.TERM_SETS)} value lists for those facts.
Use standard schema.org first. Use these terms only where schema.org has no home.</p>
<p><strong>Status: draft.</strong> Version 0.x can still change. Term IDs never change and are never deleted.
Version 0.1 was built for Australian building and construction law.</p>
</div>

<h2 id="how-to-use">How to use it on a page</h2>
<ol>
<li>Write the prefix inline in <code>@context</code>. Never load a remote context file: if it cannot load, JSON-LD processing stops.</li>
<li>Write every fact as visible text on the page too, for example in a "Key facts" table. Search engines and AI engines quote text, not hidden markup.</li>
<li>Where a standard schema.org property can carry part of the fact, publish it as well (see "Also publish as").</li>
</ol>
<pre><code>{E('''{
  "@context": ["https://schema.org", {"legal": "https://w3id.org/servicefacts/legal#"}],
  "@type": "Service",
  "name": "Security of payment claims",
  "audience": {"@type": "BusinessAudience", "audienceType": "Subcontractors"},
  "legal:actsFor": {"@id": "https://w3id.org/servicefacts/legal#PartyRoles-subcontractor"},
  "legal:disputeProcess": {"@id": "https://w3id.org/servicefacts/legal#DisputeProcesses-adjudication"}
}''')}</code></pre>

<h2 id="properties">Properties</h2>
<div class="tablewrap"><table>
<tr><th>Property</th><th>Goes on</th><th>Value</th><th>Priority</th><th>Buyer question</th></tr>"""]
    for term, dom, rng, prio, module, question, definition, dual in legal.CUSTOM:
        parts.append(f"<tr><td><a href=\"#{term}\"><code>{pfx}:{term}</code></a></td>"
                     f"<td>{', '.join(dom)}</td><td>{', '.join(rng)}</td><td>{prio}</td><td>{E(question)}</td></tr>")
    parts.append("</table></div>")

    for term, dom, rng, prio, module, question, definition, dual in legal.CUSTOM:
        parts.append(f"""<div class="term" id="{term}"><h3><code>{pfx}:{term}</code></h3>
<p>{E(definition)}</p><dl>
<dt>ID</dt><dd><code>{E(ns + term)}</code></dd>
<dt>Goes on</dt><dd>{', '.join(type_link(t) for t in dom)}</dd>
<dt>Value</dt><dd>{', '.join(type_link(t) for t in rng)}</dd>
<dt>Priority</dt><dd>{prio}</dd>
<dt>Module</dt><dd>{module}</dd>
<dt>Buyer question</dt><dd>{E(question)}</dd>
{f'<dt>Also publish as</dt><dd>{E(dual)}</dd>' if dual else ''}
</dl></div>""")

    parts.append('<h2 id="classes">Classes</h2>')
    for name, parent, comment in legal.CLASSES:
        users = [t for t, d, r, *_ in legal.CUSTOM if name in r]
        parts.append(f"""<div class="term" id="{name}"><h3><code>{pfx}:{name}</code></h3>
<p>{E(comment)}</p><dl>
<dt>ID</dt><dd><code>{E(ns + name)}</code></dd>
<dt>Subclass of</dt><dd>{type_link(parent)}</dd>
<dt>Value of</dt><dd>{', '.join(f'<a href="#{t}"><code>{pfx}:{t}</code></a>' for t in users)}</dd>
<dt>Parts</dt><dd>{', '.join(f'<a href="#{t}"><code>{pfx}:{t}</code></a>' for t, d, *_ in legal.CUSTOM if name in d)}</dd>
</dl></div>""")

    parts.append('<h2 id="value-lists">Value lists</h2>'
                 '<p>Each value is a <code>DefinedTerm</code> with its own ID. Point to it with <code>{"@id": "…"}</code>. '
                 'Matches to outside vocabularies say how close they are (SKOS). Only an exact match may become <code>sameAs</code> on a page.</p>')
    for set_code, label, terms in legal.TERM_SETS:
        parts.append(f'<h3 id="{set_code}" class="term" style="border:0;padding:0">{E(label)} <code>{pfx}:{set_code}</code></h3>'
                     '<div class="tablewrap"><table><tr><th>Value ID</th><th>Name</th><th>Meaning</th><th>Matches</th></tr>')
        for code, name, desc, same in terms:
            tid = f"{set_code}-{code}"
            matches = "<br>".join(f'{kind}: <a href="{E(url)}">{E(url.rsplit("/", 1)[-1])}</a>'
                                  for kind, url in legal.VERIFIED_MATCH.get((set_code, code), []))
            parts.append(f'<tr id="{tid}"><td><code>{pfx}:{tid}</code></td><td>{E(name)}</td><td>{E(desc)}</td><td>{matches}</td></tr>')
        parts.append("</table></div>")

    parts.append('<h2 id="schema-org">schema.org properties this profile uses</h2>'
                 '<p>Use these first. The priority says how much buyers need the fact.</p>'
                 '<div class="tablewrap"><table><tr><th>Property</th><th>On</th><th>Priority</th><th>Note</th></tr>')
    for prop, types, prio, note in legal.STANDARD:
        parts.append(f'<tr><td><a href="https://schema.org/{prop}"><code>{prop}</code></a></td>'
                     f'<td>{", ".join(types)}</td><td>{prio}</td><td>{E(note)}</td></tr>')
    parts.append("</table></div>")

    parts.append('<h2 id="annotations">Profile notes in the file</h2>'
                 '<p>The vocabulary file uses these terms to describe its own terms. They never go on a page.</p>'
                 '<div class="tablewrap"><table><tr><th>Term</th><th>Meaning</th></tr>')
    for term, meaning in ANNOTATIONS:
        parts.append(f'<tr id="{term}"><td><code>{pfx}:{term}</code></td><td>{E(meaning)}</td></tr>')
    parts.append("</table></div>")

    parts.append(f"""<h2 id="versions">Versions and changes</h2>
<div class="tablewrap"><table><tr><th>Version</th><th>Date</th><th>Change</th></tr>
<tr><td><a href="{'./' if frozen else f'{v}/'}">{E(v)}</a></td><td>{E(legal.DATE)}</td><td>First public draft.</td></tr>
</table></div>
<p>Rules: a term ID is never changed or deleted. A replaced term is marked <code>owl:deprecated</code> and
<code>schema:supersededBy</code> its replacement. Each release gets a frozen copy.
Propose a change as a <a href="{REPO}/issues">GitHub issue</a>.</p>""")

    title = f"Legal services vocabulary v{v} | Service Facts"
    desc = "Extra schema.org terms for law firms: who they act for, fees, dispute processes, forums, governing law and legal time limits."
    return page(title, desc, "\n".join(parts), [("application/ld+json", "legal.jsonld"), ("text/turtle", "legal.ttl")])


def root_page():
    v = legal.VERSION
    body = f"""
<h1>Service Facts</h1>
<p class="meta">Open vocabularies for the facts buyers ask about professional services.</p>
<div class="callout">
<p>schema.org describes businesses well, but it cannot say many of the facts that decide a buyer's choice,
such as who a law firm acts for or how long a legal deadline is. Service Facts adds a small, checked set of terms
for each industry, on top of schema.org.</p>
<p>Every term has a permanent ID under <code>{BASE}/</code>. The ID never changes, even if these files move.</p>
</div>
<h2>Vocabularies</h2>
<div class="tablewrap"><table>
<tr><th>Industry</th><th>Namespace</th><th>Version</th><th>Files</th></tr>
<tr><td><a href="legal/">Legal services</a></td><td><code>{BASE}/legal#</code></td><td>{v} (draft)</td>
<td><a href="legal/legal.jsonld">JSON-LD</a> · <a href="legal/legal.ttl">Turtle</a></td></tr>
</table></div>
<h2>Rules</h2>
<ul>
<li>Standard schema.org first. A new term only where schema.org has no home.</li>
<li>A term ID never changes and is never deleted.</li>
<li>Pages write the prefix inline. They never load a remote context file.</li>
<li>Every fact in the markup is also written as visible text on the page.</li>
</ul>
<h2>Licence and maintainers</h2>
<p>Licence: <a href="{LICENSE}">CC BY 4.0</a>. Anyone may use, copy and adapt these vocabularies if they credit Service Facts.
Maintained by <a href="https://wldm.io/">WLDM</a>. Anyone can propose a change as a <a href="{REPO}/issues">GitHub issue</a>.</p>
"""
    return page("Service Facts", "Open schema.org extension vocabularies for professional services.", body,
                [("application/ld+json", "index.jsonld")])


def catalog():
    return {
        "@context": {"schema": "https://schema.org/"},
        "@id": BASE,
        "@type": "schema:CreativeWork",
        "schema:name": "Service Facts",
        "schema:description": "Open schema.org extension vocabularies for the facts buyers ask about professional services.",
        "schema:license": LICENSE,
        "schema:maintainer": {"@type": "schema:Organization", "schema:name": "WLDM", "schema:url": "https://wldm.io/",
                              "schema:email": MAINTAINER_EMAIL},
        "schema:discussionUrl": f"{REPO}/issues",
        "schema:hasPart": [{"@id": f"{BASE}/legal", "@type": "schema:CreativeWork",
                            "schema:name": "Service Facts: Legal Services Profile", "schema:version": legal.VERSION}],
    }


def main():
    doc = legal.build()
    text = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    ttl = to_turtle(doc)
    for frozen, d in [(False, os.path.join(DOCS, "legal")), (True, os.path.join(DOCS, "legal", legal.VERSION))]:
        write(os.path.join(d, "legal.jsonld"), text)
        if ttl:
            write(os.path.join(d, "legal.ttl"), ttl)
        write(os.path.join(d, "index.html"), legal_page(doc, frozen))
    write(os.path.join(DOCS, "index.html"), root_page())
    write(os.path.join(DOCS, "index.jsonld"), json.dumps(catalog(), indent=2) + "\n")
    write(os.path.join(DOCS, ".nojekyll"), "")
    print(f"Built legal v{legal.VERSION}: {len(legal.STANDARD)} schema.org, {len(legal.CUSTOM)} custom properties, "
          f"{len(legal.CLASSES)} class, {len(legal.TERM_SETS)} value lists -> {DOCS}")


if __name__ == "__main__":
    main()
