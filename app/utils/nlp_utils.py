import spacy

nlp = spacy.load("en_core_web_sm")

def extract_nlp_fields(text: str):
    doc = nlp(text)

    # Placeholder logic — replace with proper rule-based extraction
    title = None
    skills = []
    responsibilities = []

    for sent in doc.sents:
        if "responsible for" in sent.text.lower():
            responsibilities.append(sent.text.strip())
        if any(keyword in sent.text.lower() for keyword in ["skill", "proficient", "experience with"]):
            skills.append(sent.text.strip())

    # Simple heuristic for title
    lines = text.split("\n")
    for line in lines:
        if len(line.split()) <= 8:
            title = line.strip()
            break

    return {
        "title": title,
        "skills": skills,
        "responsibilities": responsibilities
    }
