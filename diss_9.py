from bs4 import BeautifulSoup
import re
import requests
import unittest

# Task 1: Get the URL that links to the Pokemon Charmander's webpage.
# HINT: You will have to add https://pokemondb.net to the URL retrieved using BeautifulSoup
def getCharmanderLink(soup):
    url = 'https://pokemondb.net'
    info = ''
    tags = soup.find_all('a')
    for tag in tags:
        if tag.text == 'Charmander':
            info = tag.get('href')
    return url + info


# Task 2: Get the details from the box below "Egg moves". Get all the move names and store
#         them into a list. The function should return that list of moves.
def getEggMoves(pokemon):
    url = 'https://pokemondb.net/pokedex/'+ str(pokemon)
    #add code here
    egg_moves = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    page = soup.find('div', class_= "grid-col span-lg-6")
    table = page.find('table').find_next('table').find_next('table')
    rows = table.find_all('tr')
    for row in rows:
        egg_move = row.find('a', class_ = 'ent-name')
        if egg_move:
            egg_moves.append(egg_move.text)
    return egg_moves
    
    
# Task 3: Create a regex expression that will find all the times that have these formats: @2pm @5 pm @10am
# Return a list of these times without the '@' symbol. E.g. ['2pm', '5 pm', '10am']
def findLetters(sentences):
    # initialize an empty list
    lst = []
    
    # define the regular expression
    regex = r'@\d{1,2}\s?[ap]m'

    # loop through each sentence or phrase in sentences
    for line in sentences:

    # find all the words that match the regular expression in each sentence
        words = re.findall(regex, line)

    # loop through the found words and add the words to your empty list
        for word in words:
            new_word = word.strip('@')
            lst.append(new_word)

    #return the list of the last letter of all words that begin or end with a capital letter

    return lst


def main():
    url = 'https://pokemondb.net/pokedex/national'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    getCharmanderLink(soup)
    getEggMoves('scizor')

class TestAllMethods(unittest.TestCase):
    def setUp(self):
        self.soup = BeautifulSoup(requests.get('https://pokemondb.net/pokedex/national').text, 'html.parser')

    def test_link_Charmander(self):
        self.assertEqual(getCharmanderLink(self.soup), 'https://pokemondb.net/pokedex/charmander')

    def test_egg_moves(self):
        self.assertEqual(getEggMoves('scizor'), ['Counter', 'Defog', 'Feint', 'Night Slash', 'Quick Guard'])

    def test_findLetters(self):
        self.assertEqual(findLetters(['Come eat lunch at 12','there"s a party @2pm', 'practice @7am','nothing']), ['2pm', '7am'])
        self.assertEqual(findLetters(['There is show @12pm if you want to join','I will be there @ 2pm', 'come at @3 pm will be better']), ['12pm', '3 pm'])

if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)