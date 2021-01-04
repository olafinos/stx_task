from typing import Dict


def add_books_using_api(keywords: Dict) -> int:
    base_link = "https://www.googleapis.com/books/v1/volumes?"
    for key, value in keywords.items():
        base_link += f"{key}={value if value else ''}+"
