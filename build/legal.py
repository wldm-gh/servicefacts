"""Service Facts: the legal services vocabulary, as Python lists.

Edit the lists here, never the generated JSON. Then run:
    python build/build.py
    python tools/check-profile.py docs/legal/legal.jsonld

The vocabulary is an @graph of rdf:Property nodes, rdfs:Class nodes and
schema:DefinedTermSet value lists. Term IDs are hash IDs under NS. A term ID
never changes and is never deleted (see GOVERNANCE.md).
"""
VERSION = "0.1"
DATE = "2026-10-20"
NS = "https://w3id.org/servicefacts/legal#"
PREFIX = "legal"  # short name for NS in JSON-LD. Change NS and PREFIX together.


def p(name):
    """A term in our namespace, as a compact IRI (PREFIX:name)."""
    return f"{PREFIX}:{name}"

# ---------------------------------------------------------------------------
# 1. Standard schema.org properties we use, per anchor type.
#    (property, [types], priority, note)
# ---------------------------------------------------------------------------
STANDARD = [
    # Firm and offices
    ("name", ["LegalService", "Service", "Person", "Legislation", "GovernmentOrganization", "DefinedTerm"], "High", "Exact name, same everywhere."),
    ("url", ["LegalService", "Service", "Person", "Legislation", "GovernmentOrganization"], "High", "The main-site page for this entity. For Acts and bodies: the official URL."),
    ("sameAs", ["LegalService", "Person", "Legislation", "GovernmentOrganization", "DefinedTerm"], "High", "Wikidata item, official register entry, LinkedIn, law society directory entry."),
    ("telephone", ["LegalService"], "High", ""),
    ("address", ["LegalService"], "High", "One LegalService node per office."),
    ("areaServed", ["LegalService", "Service"], "High", "State or region as an AdministrativeArea with sameAs Wikidata."),
    ("hasOfferCatalog", ["LegalService", "Service"], "High", "Practice areas under the firm; matter types under a practice area."),
    ("department", ["LegalService"], "Medium", "Links the firm to each office."),
    ("parentOrganization", ["LegalService"], "Medium", "Links each office back to the firm."),
    ("employee", ["LegalService"], "Medium", "The lawyers."),
    ("knowsAbout", ["LegalService", "Person"], "Medium", "Practice-area terms, Acts, standard contract forms."),
    ("memberOf", ["LegalService", "Person"], "Medium", "Law society, industry bodies."),
    ("openingHoursSpecification", ["LegalService"], "Medium", ""),
    ("legalName", ["LegalService"], "Low", ""),
    ("foundingDate", ["LegalService"], "Low", ""),
    # Practice areas and matter types
    ("description", ["Service", "DefinedTerm"], "High", "Specific, not marketing. Same words as the page."),
    ("provider", ["Service"], "High", "The firm (or the office)."),
    ("serviceType", ["Service"], "High", "Plain name of the matter type, e.g. 'Security of payment claim'."),
    ("category", ["Service"], "High", "The practice-area term from the PracticeAreas list."),
    ("audience", ["Service"], "High", "Dual-publish of actsFor, as Audience + audienceType text."),
    ("offers", ["Service"], "High", "Initial consultation and any published fixed fee, as Offer."),
    ("serviceOutput", ["Service"], "Medium", "What the client gets, e.g. an adjudication determination or a signed contract."),
    ("isRelatedTo", ["Service"], "Medium", "Sibling matter types."),
    ("availableChannel", ["Service"], "Low", "In person, phone, video."),
    ("hoursAvailable", ["Service"], "Low", "Urgent or after-hours help, if offered."),
    # People
    ("jobTitle", ["Person"], "High", "Partner, Principal, Senior Associate, Lawyer."),
    ("worksFor", ["Person"], "High", ""),
    ("hasCredential", ["Person"], "High", "Admission, practising certificate, accredited specialisation."),
    ("hasOccupation", ["Person"], "Medium", "Occupation with an ANZSCO/OSCA code."),
    ("alumniOf", ["Person"], "Medium", ""),
    ("knowsLanguage", ["Person"], "Medium", "Buyers ask for lawyers who speak their language."),
    ("workLocation", ["Person"], "Medium", "The office the lawyer works from (the office LegalService node)."),
    ("image", ["Person"], "Medium", ""),
    ("award", ["Person", "LegalService"], "Low", "Only real, verifiable awards."),
    # Credentials and occupation
    ("credentialCategory", ["EducationalOccupationalCredential"], "High", "Admission / Practising certificate / Accredited specialist."),
    ("recognizedBy", ["EducationalOccupationalCredential"], "High", "Court (admission), regulator (practising certificate), law society (specialisation)."),
    ("validIn", ["EducationalOccupationalCredential"], "High", "The state where it is valid."),
    ("about", ["EducationalOccupationalCredential", "WebPage"], "High", "Credential: the specialist area. Page: the main Service it is about."),
    ("occupationalCategory", ["Occupation"], "Medium", "ANZSCO or OSCA code as CategoryCode."),
    ("occupationLocation", ["Occupation"], "Low", ""),
    # Pages
    ("mentions", ["WebPage"], "High", "Every Act, body and legal term named in the visible text."),
    ("reviewedBy", ["WebPage"], "High", "The lawyer who checked the page. Legal content must show this."),
    ("lastReviewed", ["WebPage"], "High", "Law changes. Buyers and AI need to know the page is current."),
    ("citation", ["WebPage"], "Medium", "The Acts the page relies on (dual-publish of governingLegislation)."),
    ("author", ["WebPage"], "Medium", ""),
    ("dateModified", ["WebPage"], "Medium", ""),
    # Legislation and bodies
    ("alternateName", ["Legislation", "GovernmentOrganization"], "High", "Short names people use: 'SOPA', 'VCAT'."),
    ("legislationJurisdiction", ["Legislation"], "High", ""),
    ("legislationIdentifier", ["Legislation"], "Medium", "Act number, e.g. 'No. 15 of 2002'."),
    ("legislationType", ["Legislation"], "Medium", "Act, Regulations, section."),
    ("legislationLegalForce", ["Legislation"], "Medium", "InForce / NotInForce / PartiallyInForce."),
    ("isPartOf", ["Legislation"], "Medium", "A section node points to its Act."),
    # Terms
    ("inDefinedTermSet", ["DefinedTerm"], "High", ""),
    ("termCode", ["DefinedTerm"], "Low", ""),
    # Offers
    ("price", ["Offer"], "High", "Only when the firm publishes the price."),
    ("priceCurrency", ["Offer"], "High", "AUD."),
    ("itemOffered", ["Offer"], "High", ""),
    ("priceSpecification", ["Offer"], "Medium", "Hourly rate as UnitPriceSpecification with unitText 'hour'."),
]

# ---------------------------------------------------------------------------
# 2. New properties (rung 5): only where schema.org has no home.
#    (term, [domain types], [range types], priority, module, question, definition, dual-publish)
#    Types without a prefix are schema.org. "TimeLimit" is ours.
# ---------------------------------------------------------------------------
CUSTOM = [
    ("actsFor", ["Service", "LegalService", "Person"], ["DefinedTerm"], "High", "core",
     "Do you act for subcontractors / homeowners / builders?",
     "A party role the firm or lawyer acts for in this kind of matter. Value from the PartyRoles list.",
     "audience (Audience + audienceType text)"),
    ("feeArrangement", ["Service", "Offer"], ["DefinedTerm"], "High", "core",
     "Is it a fixed fee? Do you charge by the hour? Is the first meeting free?",
     "How the firm charges for this kind of matter. Value from the FeeArrangements list.",
     "offers → Offer with price / priceSpecification, when a price is published"),
    ("disputeProcess", ["Service"], ["DefinedTerm"], "High", "core",
     "Will this go to court? Can it be settled by mediation or adjudication?",
     "A dispute-resolution process the service can use or lead to. Value from the DisputeProcesses list.",
     ""),
    ("forum", ["Service"], ["GovernmentOrganization", "Organization"], "High", "core",
     "Which court or tribunal hears this? Who appoints the adjudicator?",
     "A court, tribunal, government scheme or appointing body where this kind of matter is decided or resolved.",
     "WebPage.mentions"),
    ("governingLegislation", ["Service", "DefinedTerm"], ["Legislation"], "High", "core",
     "Which law covers my situation?",
     "An Act, regulation or section that governs this kind of matter or defines this term.",
     "WebPage.citation"),
    ("hasTimeLimit", ["Service", "Legislation", "DefinedTerm"], ["TimeLimit"], "High", "core",
     "How long do I have to respond / to claim / to appeal?",
     "A legal time limit that applies. Every practice area has these (limitation periods, response deadlines).",
     ""),
    ("appliesToStep", ["TimeLimit"], ["DefinedTerm"], "High", "core",
     "(part of a time limit)",
     "The step that must be done in time, e.g. 'Payment schedule'.", ""),
    ("timeAllowed", ["TimeLimit"], ["QuantitativeValue"], "High", "core",
     "(part of a time limit)",
     "How much time. QuantitativeValue with value and unitText, e.g. 10 + 'business days'.", ""),
    ("countedFrom", ["TimeLimit"], ["DefinedTerm"], "High", "core",
     "(part of a time limit)",
     "The event the time runs from, e.g. 'Payment claim served'.", ""),
    ("legalSource", ["TimeLimit"], ["Legislation"], "High", "core",
     "(part of a time limit)",
     "The Act or section that sets the time limit. Use a Legislation node for the section, isPartOf the Act.", ""),
    ("consequenceIfMissed", ["TimeLimit"], ["Text"], "Medium", "core",
     "What happens if I miss the deadline?",
     "Plain statement of what happens if the step is late or missed.", ""),
    ("typicalDuration", ["Service"], ["Duration", "QuantitativeValue"], "Medium", "core",
     "How long will it take?",
     "The usual time from instruction to outcome, as a range. Must come from the firm, not a guess.", ""),
    ("matterValueRange", ["Service"], ["MonetaryAmount"], "Medium", "core",
     "Do you take small claims? Is my matter big enough?",
     "The claim or deal values the firm usually handles for this service (MonetaryAmount with minValue / maxValue).", ""),
    ("dateAdmitted", ["Person", "EducationalOccupationalCredential"], ["Date"], "High", "core",
     "How experienced is the lawyer?",
     "Date the lawyer was admitted to practise. schema.org credentials have no award date.", ""),
    ("contractForm", ["Service", "LegalService", "Person"], ["CreativeWork"], "High", "construction",
     "Can you review my HIA / Master Builders / AS 4000 contract?",
     "A standard-form contract the firm drafts, reviews or disputes. Value: a CreativeWork node for the contract form.",
     "knowsAbout on the firm and the lawyer"),
    ("projectType", ["Service"], ["DefinedTerm"], "Medium", "construction",
     "Do you handle home builds, renovations, apartments or commercial projects?",
     "The kind of building project the service covers. Value from the ProjectTypes list.", ""),
]

CLASSES = [
    ("TimeLimit", "StructuredValue",
     "A legal time limit: a step that must be done within a set time, counted from a set event, under a named law."),
]

# ---------------------------------------------------------------------------
# 3. Value lists (DefinedTermSet). sameAs is filled only with verified IDs.
#    (set, set label, [(code, name, description, [sameAs...])])
# ---------------------------------------------------------------------------
TERM_SETS = [
    ("PartyRoles", "Party roles", [
        ("homeowner", "Homeowner", "A person who owns, or is building or renovating, their home.", []),
        ("owners-corporation", "Owners corporation", "The body that manages common property in a strata or apartment building.", []),
        ("builder", "Builder", "A registered builder carrying out or managing building work.", []),
        ("head-contractor", "Head contractor", "The contractor engaged directly by the owner or principal.", []),
        ("subcontractor", "Subcontractor", "A contractor engaged by another contractor.", []),
        ("supplier", "Supplier", "A person who supplies goods or materials for building work.", []),
        ("developer", "Property developer", "A person or company developing property for sale or lease.", []),
        ("consultant", "Building consultant", "An architect, engineer, surveyor or other design or certifying professional.", []),
    ]),
    ("FeeArrangements", "Fee arrangements", [
        ("fixed-fee", "Fixed fee", "One agreed price for a defined piece of work.", []),
        ("staged-fixed-fee", "Staged fixed fee", "A fixed price per stage of the matter.", []),
        ("hourly-rate", "Hourly rate", "Charged by time spent, at a stated hourly rate.", []),
        ("capped-fee", "Capped fee", "Charged by time, up to an agreed maximum.", []),
        ("conditional-fee", "Conditional fee", "Fees payable only on a successful outcome, where the law allows it.", []),
        ("free-initial-consultation", "Free initial consultation", "A first meeting at no charge.", []),
    ]),
    ("DisputeProcesses", "Dispute processes", [
        ("negotiation", "Negotiation", "Parties settle directly or through lawyers.", []),
        ("mediation", "Mediation", "A neutral mediator helps the parties reach agreement.", []),
        ("conciliation", "Conciliation", "A government conciliator helps the parties reach agreement.", []),
        ("adjudication", "Statutory adjudication", "A fast, binding interim decision on a payment dispute under security of payment law.", []),
        ("tribunal", "Tribunal hearing", "A hearing and decision by a tribunal.", []),
        ("litigation", "Court litigation", "Proceedings in a court.", []),
        ("arbitration", "Arbitration", "A private, binding decision by an arbitrator.", []),
        ("expert-determination", "Expert determination", "An expert decides a technical question, usually by contract.", []),
    ]),
    ("ProjectTypes", "Project types (construction module)", [
        ("domestic-new-home", "New home build", "Domestic building work to build a new home.", []),
        ("domestic-renovation", "Home renovation or extension", "Domestic building work on an existing home.", []),
        ("apartment-strata", "Apartment or strata building", "Multi-owner residential buildings and their common property.", []),
        ("commercial", "Commercial construction", "Non-residential building projects.", []),
    ]),
    ("PracticeAreas", "Practice areas", [
        ("building-construction", "Building and construction law", "Law of building contracts, payment, defects and building disputes.", []),
        ("family", "Family law", "Law of separation, divorce, parenting and property settlement.", []),
        ("wills-estates", "Wills and estates", "Law of wills, estate planning, probate and will disputes.", []),
        ("employment", "Employment law", "Law of employment contracts, dismissal and workplace rights.", []),
        ("business-commercial", "Business and commercial law", "Law of buying, selling and running a business, and commercial contracts.", []),
        ("debt-recovery", "Debt recovery", "Recovering money owed, by demand, negotiation or court action.", []),
    ]),
]

# Mappings to outside vocabularies, verified 2026-09-28 (FOLIO live API, Wikidata API).
# SKOS says how close the match is. Only "exact" may become schema:sameAs in page JSON-LD.
FOLIO = "https://folio.openlegalstandard.org/"
WD = "http://www.wikidata.org/entity/"
VERIFIED_MATCH = {
    ("PracticeAreas", "building-construction"): [
        ("close", FOLIO + "R7o4TiXsYQ6vV6MrJMTfnS7"),  # FOLIO "Construction and Development Law"
        ("close", WD + "Q811705"),                     # construction law (de/fr sitelinks differ: close, not exact)
    ],
    ("DisputeProcesses", "mediation"): [("close", FOLIO + "R9zgcjBBIdWMnwIR8nqsoS8")],   # FOLIO "Mediation"
    ("DisputeProcesses", "arbitration"): [("close", FOLIO + "RXO2u2WBkUUcEG1jczLIcA")],  # FOLIO "Arbitration"
    ("DisputeProcesses", "litigation"): [("close", FOLIO + "R79LjWBKHCdmQKEW6zPY8Co")],  # FOLIO "Litigation Practice"
    ("DisputeProcesses", "adjudication"): [
        ("broad", WD + "Q357789"),     # adjudication in general
        ("related", WD + "Q7445053"),  # security of payment
    ],
    ("ProjectTypes", "apartment-strata"): [("related", WD + "Q5978901")],  # strata title
}
SKOS = {"exact": "skos:exactMatch", "close": "skos:closeMatch",
        "broad": "skos:broadMatch", "related": "skos:relatedMatch"}


def s(t):
    return {"@id": t if ":" in t else (p(t) if t in {c[0] for c in CLASSES} else "schema:" + t)}


def build():
    graph = []
    for prop, types, prio, note in STANDARD:
        graph.append({
            "@id": "schema:" + prop, "@type": "rdf:Property",
            "rdfs:label": prop,
            "rdfs:comment": note or "Standard schema.org property.",
            "schema:domainIncludes": [s(t) for t in types],
            "schema:isPartOf": {"@id": "https://schema.org"},
            p("priority"): prio, p("module"): "core",
        })
    for name, parent, comment in CLASSES:
        graph.append({"@id": p(name), "@type": "rdfs:Class", "rdfs:label": name,
                      "rdfs:comment": comment, "rdfs:subClassOf": s(parent)})
    for term, dom, rng, prio, module, question, definition, dual in CUSTOM:
        node = {
            "@id": p(term), "@type": "rdf:Property",
            "rdfs:label": term, "rdfs:comment": definition,
            "schema:domainIncludes": [s(t) for t in dom],
            "schema:rangeIncludes": [s(t) for t in rng],
            "schema:isPartOf": {"@id": NS.rstrip("#")},
            p("priority"): prio, p("module"): module,
            p("answersQuestion"): question,
            p("visibleTextRequired"): True,
            p("priorityEvidence"): "Hypothesis v0.1: from a review of law-firm service pages and the questions buyers ask. To be measured with AI prompt tracking.",
        }
        if dual:
            node[p("dualPublishAs")] = dual
        graph.append(node)
    for set_code, label, terms in TERM_SETS:
        set_id = p(set_code)
        graph.append({"@id": set_id, "@type": "schema:DefinedTermSet", "schema:name": label,
                      "schema:hasDefinedTerm": [{"@id": p(f"{set_code}-{c}")} for c, *_ in terms]})
        for code, name, desc, same in terms:
            node = {"@id": p(f"{set_code}-{code}"), "@type": "schema:DefinedTerm",
                    "schema:name": name, "schema:termCode": code,
                    "schema:inDefinedTermSet": {"@id": set_id}}
            if desc:
                node["schema:description"] = desc
            for kind, url in VERIFIED_MATCH.get((set_code, code), []):
                node.setdefault(SKOS[kind], []).append({"@id": url})
            if same:
                node["schema:sameAs"] = same
            graph.append(node)

    n_std, n_cus = len(STANDARD), len(CUSTOM)
    doc = {
        "@context": {
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "schema": "https://schema.org/",
            "owl": "http://www.w3.org/2002/07/owl#",
            "skos": "http://www.w3.org/2004/02/skos/core#",
            PREFIX: NS,
            "xsd": "http://www.w3.org/2001/XMLSchema#",
        },
        "@id": NS.rstrip("#"),
        "@type": ["schema:CreativeWork", "owl:Ontology"],
        "owl:versionIRI": {"@id": f"{NS.rstrip('#')}/{VERSION}"},
        "owl:versionInfo": VERSION,
        "schema:name": "Service Facts: Legal Services Profile",
        "schema:version": VERSION,
        "schema:dateModified": DATE,
        "schema:license": "https://creativecommons.org/licenses/by/4.0/",
        "schema:maintainer": {"@type": "schema:Organization", "schema:name": "WLDM", "schema:url": "https://wldm.io/",
                              "schema:email": "peter@wldm.io"},
        "schema:discussionUrl": "https://github.com/wldm-gh/servicefacts/issues",
        "schema:creativeWorkStatus": "Draft",
        "schema:description": "Draft. Facts buyers ask about legal services, and how to state and mark them up. "
                              "Standard schema.org first; custom terms only where schema.org has no home. "
                              "v0.1 was built for Australian building and construction law.",
        p("propertyIndex"): {
            "schemaOrgProperties": n_std, "customProperties": n_cus, "classes": len(CLASSES),
            "termSets": len(TERM_SETS),
            "modules": sorted({c[4] for c in CUSTOM}),
        },
        "@graph": graph,
    }
    return doc
