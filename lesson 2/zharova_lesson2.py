import os
import json
import requests
import bs4

HEADERS = {
    'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
}
URL = 'https://geekbrains.ru/posts'
BASE_URL = 'https://geekbrains.ru'


def get_next_page(soap: bs4.BeautifulSoup) -> str:
    ul = soap.find('ul', attrs={'class': 'gb__pagination'})
    a = ul.find(lambda tag: tag.name == 'a' and tag.text == '›')
    return f"{BASE_URL}{a['href']}" if a else None


def get_post_url(soap):
    post_a = soap.select('div.post-items-wrapper div.post-item a')
    return set(f"{BASE_URL}{itm['href']}" for itm in post_a)


def get_page(url):
    while url:
        print(url)
        response = requests.get(url, headers=HEADERS)
        soap = bs4.BeautifulSoup(response.text, 'lxml')
        yield soap
        url = get_next_page(soap)


def get_post_data(post_url):
    template_data = {'url': post_url,
                     'image': '',
                     'title': '',
                     'writer': {'name': '',
                                'url': ''},
                     'tags': []}
    response = requests.get(post_url, headers=HEADERS)
    soap = bs4.BeautifulSoup(response.text, 'lxml')
    template_data['title'] = soap.select_one('article h1.blogpost-title').text
    template_data['tags'] = {itm.text: f"{BASE_URL}{itm['href']}" for itm in soap.select('a.small')}
    template_data['image'] = soap.select_one('article.col-sm-6 img')['src']
    template_data['writer']['url'] = f"{BASE_URL}{soap.select_one('div.col-md-5 a')['href']}"
    template_data['writer']['name'] = soap.find('div', attrs={'itemprop': 'author'}).text

    return template_data


def post_data(template_data, file_dir):
    file_name = template_data['url'].replace('/', '_').replace('.', '_').replace(':', '')

    with open(os.path.join(file_dir, f'{file_name}.json'), 'w') as file:
        file.write(json.dumps(template_data))


def get_tag_data(tag_name, tag_url):
    # {'tag_name': {'url': '', 'posts': ['url_post', ]}}
    response = requests.get(tag_url, headers=HEADERS)
    soap = bs4.BeautifulSoup(response.text, 'lxml')
    post_a = soap.select('div.post-items-wrapper div.post-item a')
    tag_posts = list(set(f"{BASE_URL}{itm['href']}" for itm in post_a))
    return {tag_name: {'url': tag_url, 'posts': tag_posts}}


def post_tags(all_tegs_data, file_dir, file_name):
    with open(os.path.join(file_dir, f'{file_name}.json'), 'w') as file:
        file.write(json.dumps(all_tegs_data))


if __name__ == '__main__':
    FILE_DIR = os.path.join(os.getcwd(), 'posts')
    if not os.path.exists(FILE_DIR):  # Если пути не существует создаем его
        os.makedirs(FILE_DIR)

    all_tags = []
    all_tags_data = []

    data = get_page(URL)

    for soap in get_page(URL):
        posts = get_post_url(soap)
        for url in posts:
            data = get_post_data(url)
            post_data(data, FILE_DIR)
            for tag_name, tag_url in data['tags'].items():
                if tag_name not in all_tags:
                    all_tags.append(tag_name)
                    all_tags_data.append(get_tag_data(tag_name, tag_url))

    post_tags(all_tags_data, FILE_DIR, 'tags')
