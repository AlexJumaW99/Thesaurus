#import json 
import difflib 
import mysql.connector

#data = json.load(open('data.json')) #a dictionary 

con = mysql.connector.connect(  #allows us to connect to the db that is stored in the cloud
    user = 'ardit700_student',
    password = 'ardit700_student',
    host = '108.167.140.122',
    database = 'ardit700_pm1database'
)

cursor = con.cursor() #allows us to navigate through the tables in the db

def set_words(): #returns a list of all English words
    query = cursor.execute("SELECT Expression FROM Dictionary")
    results = cursor.fetchall()
    word_set = []

    for item in results:
        item = list(item)
        word_set.append(item)
    
    return word_set #This is a list of all the Expressions in the English language, use it for comparison

set_of_words = set_words() #List of lists
set_of_words = [ item for elem in set_of_words for item in elem] #changes set_of_words to a flat list [], not nested [[]]
set_of_words = set(set_of_words) #removes all duplicate values
set_of_words = list(set_of_words) #now we have a list with unique values

def fetch_meanings(word): #fetches the meanings of the word searched by the user
    query = cursor.execute(f"SELECT Definition FROM Dictionary WHERE Expression = '{word}' OR Expression = '{word.upper()}' OR Expression = '{word.title()}' ")
    results = cursor.fetchall()
    meaning = []

    for item in results:
        item = list(item)
        meaning.append(item)
    
    return meaning


def thesaurus():
    user_input = input('Enter word: ')
    print('\n')
    meanings = fetch_meanings(user_input) #This is a list of lists containing all the possible meanings as each list item
    meanings = [ item for elem in meanings for item in elem] #returns flat list, no longer nested

    if meanings: #if the meaning of the searched word exists then give it 
        for i in range (0,len(meanings)):
            print (f'{i+1}: {meanings[i]}')
    else:
        matches = difflib.get_close_matches(user_input, set_of_words)
        ask = input(f'Did you mean {matches[0]}, {matches[1]} or {matches[2]}? Y/N: ')

        if ask.lower() == 'y':
            print('\n')
            ask1 = int(input(f'Which? 1,2 or 3: '))
            if ask1 == 1:
                meanings = fetch_meanings(matches[0])
                meanings = [ item for elem in meanings for item in elem]
                for i in range (0,len(meanings)):
                    print (f'{i+1}: {meanings[i]}')
                    

            elif ask1 == 2:
                count = 1
                meanings = fetch_meanings(matches[1])
                meanings = [ item for elem in meanings for item in elem]
                for item in meanings:
                    print (f'{count}: {item}')
                    count += 1

            elif ask1 == 3:
                count = 1
                meanings = fetch_meanings(matches[2])
                meanings = [ item for elem in meanings for item in elem]
                for item in meanings:
                    print (f'{count}: {item}')
                    count += 1

        elif ask.lower() == 'n':
            print ('The word does not exist.')
        else:
            print ('Sorry, invalid choice')


condition = True 

while condition:
    thesaurus()
    print('\n')
    ask2 = input('Enter Q to quit or any other button to continue: ')

    if ask2.lower() == 'q':
        condition = False
    else: 
        continue

    