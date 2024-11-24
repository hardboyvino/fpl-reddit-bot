import spacy
from fuzzywuzzy import process

nlp = spacy.load('en_core_web_sm')

def extract_player_names(input_text, name_variations):
    """
    Extracts player names from the input text using NLP and fuzzy matching.

    Parameters:
    - input_text (str): The text to parse.
    - name_variations (Dict[str, str]): The mapping of name variations to standard names.

    Returns:
    - List[str]: A list of extracted player names.
    """
    doc = nlp(input_text)
    extracted_names = []

    # Combine all variations into a list for fuzzy matching
    all_variations = list(name_variations.keys())

    # Extract potential names using NER and tokens
    potential_names = set()
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'ORG', 'GPE']:
            potential_names.add(ent.text)
    for token in doc:
        if token.pos_ == 'PROPN':
            potential_names.add(token.text)

    # Fuzzy match extracted names to variations
    for name in potential_names:
        match, score = process.extractOne(name.lower(), all_variations)
        if score >= 80:  # Threshold can be adjusted
            normalized_name = name_variations[match]
            if normalized_name not in extracted_names:
                extracted_names.append(normalized_name)

    return extracted_names

def determine_query_type(input_text):
    """
    Determines the type of query from the input text.

    Parameters:
    - input_text (str): The text to parse.

    Returns:
    - str: The type of query ('RMT', 'Transfer', 'Comparison', 'Unknown').
    """
    input_text = input_text.lower()
    if 'rate my team' in input_text or 'rmt' in input_text:
        return 'RMT'
    elif 'transfer' in input_text or 'buy' in input_text or 'sell' in input_text:
        return 'Transfer'
    elif 'or' in input_text or 'vs' in input_text or 'versus' in input_text:
        return 'Comparison'
    else:
        return 'Unknown'
