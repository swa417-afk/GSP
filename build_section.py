import html

def esc(s):
    return html.escape(s, quote=True)

def heading2(text):
    return (
        '<w:p><w:pPr><w:pStyle w:val="Heading2"/><w:spacing w:before="280" w:after="160"/></w:pPr>'
        '<w:r><w:rPr><w:rFonts w:ascii="Arial" w:cs="Arial" w:eastAsia="Arial" w:hAnsi="Arial"/><w:b/><w:bCs/>'
        '<w:color w:val="2E75B6"/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr>'
        f'<w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>'
    )

def body(text):
    return (
        '<w:p><w:pPr><w:spacing w:after="160" w:line="276"/></w:pPr>'
        '<w:r><w:rPr><w:rFonts w:ascii="Arial" w:cs="Arial" w:eastAsia="Arial" w:hAnsi="Arial"/>'
        '<w:color w:val="333333"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>'
        f'<w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>'
    )

def bold_label(text, before=200, after=120):
    return (
        f'<w:p><w:pPr><w:spacing w:before="{before}" w:after="{after}"/></w:pPr>'
        '<w:r><w:rPr><w:rFonts w:ascii="Arial" w:cs="Arial" w:eastAsia="Arial" w:hAnsi="Arial"/><w:b/><w:bCs/>'
        '<w:color w:val="1A1A2E"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>'
        f'<w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>'
    )

def sub_label(text):
    return (
        '<w:p><w:pPr><w:spacing w:before="120" w:after="60"/></w:pPr>'
        '<w:r><w:rPr><w:rFonts w:ascii="Arial" w:cs="Arial" w:eastAsia="Arial" w:hAnsi="Arial"/><w:b/><w:bCs/><w:i/><w:iCs/>'
        '<w:color w:val="2E75B6"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>'
        f'<w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>'
    )

def code_block(lines):
    out = []
    n = len(lines)
    for i, line in enumerate(lines):
        after = "160" if i == n - 1 else "0"
        out.append(
            f'<w:p><w:pPr><w:spacing w:after="{after}" w:line="240"/><w:ind w:left="360"/></w:pPr>'
            '<w:r><w:rPr><w:rFonts w:ascii="Courier New" w:cs="Courier New" w:eastAsia="Courier New" w:hAnsi="Courier New"/>'
            '<w:color w:val="2D2D2D"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
            f'<w:t xml:space="preserve">{esc(line)}</w:t></w:r></w:p>'
        )
    return ''.join(out)

def proof_para(label, text):
    return (
        '<w:p><w:pPr><w:spacing w:after="160" w:line="276"/></w:pPr>'
        '<w:r><w:rPr><w:rFonts w:ascii="Arial" w:cs="Arial" w:eastAsia="Arial" w:hAnsi="Arial"/><w:b/><w:bCs/>'
        '<w:color w:val="333333"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>'
        f'<w:t xml:space="preserve">{esc(label)} </w:t></w:r>'
        '<w:r><w:rPr><w:rFonts w:ascii="Arial" w:cs="Arial" w:eastAsia="Arial" w:hAnsi="Arial"/>'
        '<w:color w:val="333333"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>'
        f'<w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>'
    )

actions = [
    {
        "title": "1. Rejected Content in a Date Range",
        "request": [
            "{",
            '  "actionFilter": "content_ingest_decision",',
            '  "fromDate": "ISO-8601",',
            '  "toDate": "ISO-8601"',
            "}",
        ],
        "logic": [
            "results = []",
            "FOR attestation IN reconstruct(request):",
            '  IF attestation.metadata.decision == "REJECT":',
            "    results.append(attestation)",
            "RETURN results SORTED BY timestamp",
        ],
    },
    {
        "title": "2. Policy Version at Time of Decision",
        "request": [
            "{",
            '  "actionFilter": "content_ingest_decision",',
            '  "attestationId": "<target-attestation-id>"',
            "}",
        ],
        "logic": [
            "attestation = reconstruct(request)[0]",
            "policyVersion = attestation.metadata.policyVersion",
            "policyDocument = policyStore.lookup(policyVersion)",
            "RETURN policyDocument",
        ],
    },
    {
        "title": "3. Overridden Rejections",
        "request": [
            "{",
            '  "actionFilter": "override_applied"',
            "}",
        ],
        "logic": [
            "results = []",
            "FOR overrideAttestation IN reconstruct(request):",
            "  originalHash = overrideAttestation.metadata.decisionAttestationHash",
            "  originalAttestation = lookupByHash(originalHash)",
            "  results.append({ override: overrideAttestation, original: originalAttestation })",
            "RETURN results",
        ],
    },
    {
        "title": "4. Scan Failures in a Period",
        "request": [
            "{",
            '  "actionFilter": "content_ingest_decision",',
            '  "fromDate": "ISO-8601",',
            '  "toDate": "ISO-8601"',
            "}",
        ],
        "logic": [
            "results = []",
            "FOR attestation IN reconstruct(request):",
            '  IF "SCAN_FAILURE" IN attestation.metadata.reasonCodes:',
            "    results.append(attestation)",
            "RETURN results",
        ],
    },
    {
        "title": "5. Proof of Non-Retention",
        "request": [
            "{",
            '  "actionFilter": "content_ingest_decision",',
            '  "attestationId": "<target-attestation-id>"',
            "}",
        ],
        "logic": [
            "attestation = reconstruct(request)[0]",
            "proof = (attestation.metadata.retentionDays == 0)",
            "     AND (attestation.metadata.contentDestroyed == true)",
            "     AND NOT mainStorage.contains(attestation.metadata.inputFingerprint)",
            "RETURN proof   // boolean; true constitutes the auditable proof",
        ],
    },
]

parts = []
parts.append(heading2("8.2 Audit Action Logic"))
parts.append(body(
    "Each of the five reconstruction queries in 8.1 resolves to a specific request payload "
    "against POST /gsp/v1/reconstruct and a fixed evaluation procedure applied to the returned "
    "attestations. The logic below is deterministic and stateless: it reads already-persisted "
    "attestations and returns a derived answer. It writes nothing and calls no endpoint beyond "
    "the single reconstruction query."
))

for a in actions:
    parts.append(bold_label(a["title"]))
    parts.append(sub_label("Request"))
    parts.append(code_block(a["request"]))
    parts.append(sub_label("Evaluation logic"))
    parts.append(code_block(a["logic"]))

parts.append(proof_para(
    "Proof of non-modification:",
    "All five evaluation procedures operate as read-only logic against data already returned by "
    "POST /gsp/v1/reconstruct. No new endpoints are introduced, no new attestation fields are "
    "written, and no GSP primitive is altered. The audit action logic is implementation-layer "
    "tooling built on top of the existing reconstruction capability, in keeping with the "
    "separation of concerns in Section 9."
))

xml_block = ''.join(parts)
open('/home/claude/section_8_2.xml', 'w', encoding='utf-8').write(xml_block)
print(len(xml_block), "chars written")