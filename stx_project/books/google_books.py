from typing import Dict, List, Union
import requests
import json

class GoogleBooksDownloader():
    def get_books_using_api(self, keywords: Dict) -> int:
        base_link = self._create_link(keywords)
        resources = self._get_all_books(base_link)
        return resources

    def _create_link(self, keywords: Dict) -> str:
        base_link = "https://www.googleapis.com/books/v1/volumes?"
        for key, value in keywords.items():
            if value:
                base_link += f"{key}={value}+"
        return base_link

    def _get_all_books(self, link: str) -> List[Dict]:
        pagination_index = 0
        books = []
        resource = self._get_resource(link+f"&startIndex={pagination_index}&maxResults=40")
        while "items" in resource.keys():
            books.extend(book['volumeInfo'] for book in resource['items'])
            pagination_index +=40
            resource = self._get_resource(link + f"&startIndex={pagination_index}&maxResults=40")
        return books

    def _get_resource(self, link: str) -> Dict:
        response = requests.get(link)
        return json.loads(response.content)

class GoogleBooksParser():
    def parse(self, resources: List[Dict]) -> List[Dict]:
        books = []
        for resource in resources:
            isbn = self._get_isbn(resource)
            if not isbn:
                continue
            book = { "title" : resource['title'],
                     "isbn_number": isbn,
                     "author": ", ".join(resource.get('authors', ['NA'])),
                     "publication_date": resource.get('publishedDate', None),
                     "number_of_pages" : resource.get('pageCount', 0),
                     "cover_link": resource.get('imageLinks',{'thumbnail': None})['thumbnail'],
                     "publication_language": resource['language']
            }
            books.append(book)
        return books

    def _get_isbn(self,resource: Dict) -> Union[str, None]:
        identifiers = resource.get('industryIdentifiers', None)
        if identifiers:
            for id_type in identifiers:
                if id_type['type'] == 'ISBN_13':
                    return id_type['identifier']
            return id_type['identifier']
        return None
