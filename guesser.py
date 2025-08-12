'''
# guesser.py
def interpret_query(query: str):
    """Guess HTML tag and class based on keywords in query."""
    query_lower = query.lower()

    # Keyword to HTML mapping
    mapping = {
        "headline": ("h1", ""),
        "title": ("h1", ""),
        "paragraph": ("p", ""),
        "link": ("a", ""),
        "button": ("button", ""),
        "image": ("img", ""),
        "price": ("span", "price"),
        "product": ("div", "product"),
        "article": ("div", "article"),
    }

    for keyword, (tag, css_class) in mapping.items():
        if keyword in query_lower:
            return {"tag": tag, "class": css_class}

    # Default fallback
    return {"tag": "p", "class": ""}
'''
