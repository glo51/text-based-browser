from sys import argv
from os import makedirs
from requests import get
from bs4 import BeautifulSoup
from colorama import init, Fore, deinit


def check_url(x):
    return 0 if '.' in x else 1


def make_file_name(x):
    parts = x.split('.')
    return parts[0]


def return_site(x):
    if not x.startswith('https://'):
        x = 'https://' + x
    page = get(x)
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li'])
    result = ''
    for _i, j in enumerate(content):
        if j.name == 'a':
            init()
            result += (Fore.BLUE + j.text + '\n')
            deinit()
        else:
            result += (j.text + '\n')
    return result


def back():
    try:
        print(return_site(history.pop()))
    except IndexError:
        pass


directory = argv[1]
url = ''
saved = []
history = []
add_to_history = ''

makedirs(directory, exist_ok=True)

while True:
    url = input()
    if url == 'exit':
        break
    elif url == 'back':
        add_to_history = ''
        back()
        continue
    file_name = make_file_name(url)

    if file_name in saved:
        with open(f'{directory}/{file_name}', 'r') as file:
            print(file.read())
            if add_to_history != '':
                history.append(add_to_history)
            add_to_history = file_name
    else:
        if check_url(url):
            print('error, invalid url')
            continue
        else:
            if add_to_history != '':
                history.append(add_to_history)
            add_to_history = file_name
            with open(f'{directory}/{file_name}', 'w') as file:
                site = return_site(url)
                file.write(site)
                print(site)
                saved.append(file_name)
