from ressources.stopwords import stopwords as stopwords_list
import string
import math

#Define variables
filename = "./ressources/ref-sentences.txt"
wordlist = ["spain", "anchovy", "france", "internet", "china", "mexico", "fish", "industry", "agriculture", "fishery", "tuna", "transport","italy", "web", "communication", "labour", "fish", "cod"]


#GOAL: For each word in wordlist, print the word with the highest similarity from wordlist

#Reading lines and storing them in a list, returns the list
def read_reference_text(filename:str):
    f = open(filename)
    sentence_list = []
    for line in f:
        #We get rid of all punctuation and transform to lowercase
        nopunct = line.translate(str.maketrans('','',string.punctuation))
        sentence_list.append(nopunct.lower())
        #sentence_list.append(line.lower())
    f.close()
    return sentence_list

def make_word_vector(w: str, list: list[str]):
    reference_word = w
    word_dictionary = {}
    for sentence in list:
        #Check if the reference word is part of the sentence, if yes we create dictionaries
        if reference_word in sentence:
            #Check conditions for words in sentence
            for word in sentence.split():
                #if the sentence word = reference word we go to next word
                if word == reference_word:
                    continue
                #if sentence word is too short we go to next word
                if len(word) < 3:
                    continue
                #if sentence word is stopword we go to next word
                elif word in stopwords_list:
                    continue
                #if all conditions are passed, we create dictionary entry
                else:
                    #Check if word exists
                    if word in word_dictionary:
                        word_dictionary.update({word: word_dictionary[word]+1})
                    else:
                        word_dictionary[word] = 1

    return word_dictionary


def sim_word_vect(s1: str, s2:str)-> float:
    v1 = make_word_vector(s1, read_reference_text(filename))
    v2 = make_word_vector(s2, read_reference_text(filename))
    similarity = product(v1, v2) / (math.sqrt(product(v1, v1)* product(v2, v2)))
    return similarity
def product(v1: dict[str, int], v2: dict[str,int]) -> float:
    sp = 0.0
    for word in v1:
        sp += v1[word] * v2.get(word, 0)
    return sp





#We compute the cosine similarity
result = sim_word_vect("nato", "countries")
print(result)

