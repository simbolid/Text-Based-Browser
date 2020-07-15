# Jetbrains Academy Project: Text-based Browser
# @author Daniel Simboli
# July 14, 2020
import os
import shutil
import sys
import requests
from collections import deque
from colorama import Fore
from bs4 import BeautifulSoup

downloaded_sites = set()
site_stack = deque()


# create a directory, replacing another directory if it has the same name
def create_directory():
    if len(sys.argv) != 2:
        print("Please input the directory name as a parameter")
        exit()
    try:
        os.mkdir(sys.argv[1])
    except FileExistsError:
        shutil.rmtree(sys.argv[1])
        os.mkdir(sys.argv[1])
    return sys.argv[1]


# open the last site the user visited
def open_previous_site(directory):
    with open(os.path.join(directory, site_stack.pop())) as file:
        print(file.read())


# access a site from its saved file
def open_downloaded_site(directory, url):
    with open(os.path.join(directory, url)) as file:
        print(file.read())


# print out the parsed text from the site and save it to a file
def open_new_site(directory, url):
    text = requests.get(url).text
    downloaded_sites.add(shorten_url(url))
    with open(os.path.join(directory, shorten_url(url)), 'w') as new_file:
        soup = BeautifulSoup(text, 'html.parser')
        tags = soup.find_all(['title', 'p', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li'])
        for tag in tags:
            if tag.string:
                # make links blue
                if tag.name == 'a':
                    print(Fore.BLUE + tag.string)
                    new_file.write(Fore.BLUE + tag.string)
                else:
                    print(tag.string)
                    new_file.write(tag.string + '\n')


# remove the prefix and suffixes of a url
def shorten_url(url):
    url = url.replace('https://', '')
    if '.' in url:
        url = url[:url.rindex('.')]
    return url


def main():
    directory = create_directory()
    previous_site = ''

    while True:
        url = input()

        if url == 'exit':
            break

        if url == 'back' and len(site_stack) != 0:
            open_previous_site(directory)

        else:
            if previous_site:
                site_stack.append(previous_site)  # add the previous site the user visited to the stack
            previous_site = shorten_url(url)

            # display the site if it has a valid url or has been visited before
            if url in downloaded_sites:
                open_downloaded_site(directory, url)
            elif '.' in url:
                if 'https://' not in url:
                    url = 'https://' + url
                open_new_site(directory, url)
            else:
                print('Error: Incorrect URL')


main()
