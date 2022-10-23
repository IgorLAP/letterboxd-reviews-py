import requests
from bs4 import BeautifulSoup


def get_texts(last_page: int, user_name: str, initial_page=1, query=''):
    BASE_URL = 'https://letterboxd.com'
    texts: list[dict[str, str]] = []
    loop_count = (last_page + 1) - initial_page
    if query != '':
        print(f'Searching "{query}"')
    for counter in range(loop_count):
        print(f'In page: {counter + initial_page} of {last_page}')
        response = requests.get(
            f'{BASE_URL}/{user_name}/films/reviews/page/' +
            f'{counter + initial_page}'
        )
        reviews_page = BeautifulSoup(response.content, 'html.parser')
        headliners = reviews_page.select(
            'div.film-detail-content h2 :not(small a)')

        links_and_names: list[dict[str, str]] = []
        years = []
        movie_names: list[str] = []
        for index in range(len(headliners)):
            if index % 2 == 0:
                if query != '':
                    movie_names.append(headliners[index].text)
                else:
                    links_and_names.append({
                        'link': f'{BASE_URL}{headliners[index].get("href")}',
                        'name': headliners[index].text,
                    })
            else:
                years.append(headliners[index].text)
        if query != '' and movie_names.__contains__(query) is False:
            if counter + 1 > loop_count and len(texts) == 0:
                print('Review was not found')
            continue
        elif query != '' and movie_names.__contains__(query) is True:
            movie_found = reviews_page.find('a', string=query)
            url = f'{BASE_URL}{movie_found.get("href")}'
            review_page = BeautifulSoup(
                requests.get(url).content, 'html.parser'
            )
            paragraphs = review_page.select('.review div div p')
            review = []
            for item in paragraphs:
                review.append(item.text)
            texts.append({
                'movie': movie_found.text,
                'year': review_page.find('small', attrs={'class': 'metadata'}).text,
                'review': review
            })
            break
        else:
            counter = 0
            for movie in links_and_names:
                review_page = BeautifulSoup(
                    requests.get(movie['link']).content, 'html.parser')
                paragraphs = review_page.select('.review div div p')
                review = []
                for item in paragraphs:
                    review.append(item.text)
                texts.append({
                    'movie': movie['name'],
                    'year': years[counter],
                    'review': review
                })
                counter = counter + 1
    return texts
