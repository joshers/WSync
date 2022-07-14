import re
import hashlib
import requests
from bs4 import BeautifulSoup

wordle = "https://www.nytimes.com/games/wordle/index.html"
df = "https://wordle.darkfox.io"
write_path = "./"


def get_scripts(url, index):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    sources = soup.findAll('script', {"src": True})
    return sources[index]["src"]


def wordle_validate():
    nytjs = get_scripts(wordle, 3)
    nytjs_data = requests.get(nytjs).text
    nytanswers = re.search(r'[a-z][a-z]=(\[.*?])', nytjs_data).group(1)
    nytcompare = "var La = " + nytanswers
    nythash = hash_check(nytcompare)
    print("NYT Answer Hash: " + nythash)

    dfjs = get_scripts(df, 0)
    dfjs_answers = "https://wordle.darkfox.io/" + dfjs
    dfjs_answers_data = requests.get(dfjs_answers).text
    dfhash = hash_check(dfjs_answers_data)
    print("DF Answer Hash: " + dfhash)

    if nythash != dfhash:
        print("MISMATCH")
        writefile("answers", nythash, "La", nytanswers)
    else:
        print("Answer files are in sync...")


def writefile(type, hash, var, content):
    file = open(writepath + type + "." + hash + ".js", "w")
    file.write("var " + var + " = " + content)
    file.close()


def hash_check(string):
    hashme = string.encode('utf-8')
    hash_object = hashlib.sha1(hashme)
    hex_dig = hash_object.hexdigest()
    return hex_dig


if __name__ == '__main__':
    wordle_validate()
