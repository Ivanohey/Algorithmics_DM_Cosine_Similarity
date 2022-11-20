from ressources.stopwords import stopwords as stopwords_list

#Define variables
filename = "./ressources/ref-sentences.txt"
wordlist = ["spain", "anchovy", "france", "internet", "china", "mexico", "fish", "industry", "agriculture", "fishery", "tuna", "transport","italy", "web", "communication", "labour", "fish", "cod"]


#GOAL: For each word in wordlist, print the word with the highest similarity from wordlist

#Reading lines and storing them in a list, returns the list
def read_reference_text(filename:str):
    f = open(filename)
    sentence_list = []
    # Add each line in a list and converts all chars to lowercase
    for line in f:
        sentence_list.append(line.lower())
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
                print(word_dictionary)
    return word_dictionary


def sim_word_vect(v1: dict[str, int], v2:dict[str, int]):
    similarity = 0.0
    return similarity

#We execute the file
#read_reference_text(filename)
make_word_vector("canada", read_reference_text(filename))