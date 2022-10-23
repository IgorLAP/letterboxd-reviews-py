import json

import requests
from bs4 import BeautifulSoup

from get_texts import get_texts


def main():
    user_name = input('letterboxd username: ')
    valid_options = ['A', 'B', 'C', 'D']
    option = input(
        '''Choose:
        \nA - Get all reviews
        \nB - Until Page
        \nC - From...to...
        \nD - Get One Review
        \nAnswer? : '''
    ).strip().capitalize()
    if valid_options.__contains__(option) is False:
        print('Choose a valid option')
        return
    confirm = input(f'Confirm option {option} [y/n]: ').strip().capitalize()
    if confirm != 'Y':
        return
    BASE_URL = 'https://letterboxd.com'
    index_page = BeautifulSoup(requests.get(
        f'{BASE_URL}/{user_name}/films/reviews').content, 'html.parser')
    paginate_last_child = index_page.select('.paginate-page:last-child')
    if len(paginate_last_child) == 0:
        print(f'user: {user_name} was not found')
        return
    last_page = int(paginate_last_child[0].text)
    texts = get_by_option(option, last_page, user_name)
    if texts is not None and len(texts) > 0:
        with open('reviews.json', 'a', encoding='utf8') as outfile:
            json.dump(texts, outfile, indent=2, ensure_ascii=False)
        print('Done')


def get_by_option(val: str, last_page: int, user_name: str):
    match val:
        case  'A':
            return get_texts(last_page, user_name)
        case 'B':
            new_last = int(input('Until wich page : '))
            while new_last > last_page:
                new_last = int(
                    input(
                        f'Number is greater than your last page "{last_page}"' +
                        '\nUntil wich page? : '
                    )
                )
            return get_texts(new_last, user_name)
        case 'C':
            initial_page = int(input('"From" page : '))
            new_last = int(input('"To" page : '))
            return get_texts(new_last, user_name, initial_page)
        case 'D':
            movie_name = input('Movie name : ')
            return get_texts(last_page, user_name, query=movie_name.title())


main()
