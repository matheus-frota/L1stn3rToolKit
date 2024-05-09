import os
import time

import argparse
import requests


def title():
    return """
    ███████╗ ██████╗ █████╗ ███╗   ██╗
    ██╔════╝██╔════╝██╔══██╗████╗  ██║
    ███████╗██║     ███████║██╔██╗ ██║
    ╚════██║██║     ██╔══██║██║╚██╗██║
    ███████║╚██████╗██║  ██║██║ ╚████║
    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
    """


def banner(url, wordlist):
    if os.name == 'nt': 
        os.system('cls')
    else: 
        os.system('clear')
    print(title())
    print('---------------------------------------------------')
    print('')
    print(f'Wordlist: {wordlist}')
    print(f'URL:      {url}')
    print('')
    print('---------------------------------------------------')



def get_url(url, retry=True, n_retries=3):
    try:
        url = 'http://' + url.strip()
        response = requests.get(url, headers={'User-Agent': 'testando user'})
        if response.status_code >= 200 and response.status_code <= 300:
            return True, response.headers
        elif response.status_code in [401, 403, 407]:
            return True, response.headers
        return False, {}
    except Exception as e:
        print(e)
        if retry and n_retries > 0:
            time.sleep(5)
            n_retries-=1
            return get_url(url, n_retries=n_retries)
        return False, {}


def get_wordlist(path, use_common=True):
    try:
        file = open(path, 'r')
        return file.readlines()
    except FileNotFoundError:
        if use_common:
            path_common = 'wordlists/common.txt'
            if os.path.exists(path_common):
                file = open(path_common, 'r')
                return file.readlines()
            else:
                response = requests.get('https://raw.githubusercontent.com/v0re/dirb/master/wordlists/common.txt')
                file = response.text
                with open(path_common, 'w') as f:
                    f.write(file)
                return file
        return None
    

def scan(url, path_wordlist='wordlists/common.txt'):
    banner(url, path_wordlist)
    wordlist = get_wordlist(path_wordlist)
    for dir in wordlist:
        url_test = url + '/' + dir
        flag, headers = get_url(url_test)
        if flag:
            print(url_test)
            print(headers)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument('-w', '--wordlist')
    args = parser.parse_args()

    if args.url != None:
        if args.wordlist is not None:
            scan(args.url, args.wordlist)
        else:
            scan(args.url)


if __name__ == '__main__':
    main()