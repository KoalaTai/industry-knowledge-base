import json

industry_keywords = {
    "Quality": [
        "CAPA Management", "Root Cause Analysis", "Supplier Quality Auditing", 
        "Non-Conformance Investigations", "ISO 13485", "GMP Regulations"
    ],
    "Quality Systems": [
        "Audit Program Management", "Risk Assessment", "Cross-Functional Collaboration", 
        "EU MDR", "FDA Compliance", "21 CFR Part 820"
    ],
    "Compliance Management": [
        "FDA Regulations", "ISO Standards", "MDSAP", "Regulatory Compliance", 
        "Audit Readiness", "Supplier Qualification"
    ],
    "Regulatory Affairs": [
        "Regulatory Compliance", "EU MDR Compliance", "FDA Regulations", 
        "ISO Standards", "Risk Management"
    ],
    "CAPA Management": [
        "Corrective Actions", "Preventive Actions", "Root Cause Analysis", 
        "CAPA Reporting", "Non-Conformance Management"
    ],
    "Supplier Quality": [
        "Supplier Qualification", "Supplier Quality Auditing", "Supply Chain Continuity", 
        "Supplier Performance Management", "Supplier Change Evaluation"
    ]
}

def save_keywords_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def create_and_save_industry_keywords():
    save_keywords_to_json(industry_keywords, 'industry_keywords.json')
