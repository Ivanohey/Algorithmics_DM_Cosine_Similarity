from ressources.stopwords import stopwords as stopwords_list
import string
import math

#Define variables
filename = "./ressources/ref-sentences.txt"
wordlist = ["spain", "anchovy", "france", "internet", "china", "mexico", "fish", "industry", "agriculture", "fishery", "tuna", "transport","italy", "web", "communication", "labour", "fish", "cod"]
#test_list = ["canada","switzerland","tuna", "internet"]


def read_reference_text(filename:str):
    """
    Allows to read the reference sentences file.

    :param filename: The file to read
    :return: The list of sentences
    """
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
    """
    Creates a dictionary containing key/value pairs of words occuring in the same sentences as a reference word. The key contains the word, the value contains the number of occurences in the whole text.

    :param w: Reference word
    :param list: List of sentences
    :return: Returns the dictionary with the occuring words and their number
    """
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
    """
    Computes the cosine similarity between two strings

    :param s1: String 1
    :param s2: String 2
    :return: Cosine similarity between string 1 and string 2
    """
    v1 = make_word_vector(s1, read_reference_text(filename))
    v2 = make_word_vector(s2, read_reference_text(filename))
    similarity = product(v1, v2) / (math.sqrt(product(v1, v1)* product(v2, v2)))
    return similarity

def product(v1: dict[str, int], v2: dict[str,int]) -> float:
    """
    Computes the scalar product between two vectors

    :param v1: Vector 1
    :param v2: Vector 2
    :return: Scalar product between vector 1 and vector 2
    """
    sp = 0.0
    for word in v1:
        sp += v1[word] * v2.get(word, 0)
    return sp

def compute_all_similarities(word_list: list) -> list:
    """
    Computes the cosine similarities between all strings in a list of strings

    :param word_list: List of strings
    :return: List of cosine similarities between the strings
    """
    list_to_print = []
    already_computed_list = []
    cosine_sim_list = []
    with open("all_results.txt", "w") as file:
        for w1 in word_list:
            for w2 in word_list:
                if w2 == w1:
                    continue
                if ([w2,w1] in already_computed_list) or ([w1,w2] in already_computed_list):
                    continue
                else:
                    print("Cosine similarity: "+  w1 + " - " + w2 + ": " + str(sim_word_vect(w1, w2)))
                    already_computed_list.append([w1,w2])
                    cosine_sim_list.append([w1,w2, sim_word_vect(w1,w2)])
                    list_to_print.append(w1 + " -> " + w2 + ", " + str(sim_word_vect(w1, w2)))
        file.write('\n'.join(list_to_print))
        return cosine_sim_list

def get_highest_similarities(wordlist, cosinelist):
    """
    Returns a list of only the highest cosine similarities for a given list of strings.

    :param wordlist: List of strings
    :param cosinelist: List of computed cosine similarities between strings
    :return: List of the highest cosine similarities between strings in a given list of strings
    """
    list_to_print = []
    with open("highest_results_only.txt", "w") as file:
        for word in wordlist:
            highest_tuple = ["","",0.0]
            for tuple in cosinelist:
                if word not in tuple:
                    continue
                else:
                    similarity = tuple[2]
                    if highest_tuple[2] < similarity:
                        highest_tuple[2] = similarity
                        if tuple[0] == word:
                            highest_tuple[0] = word
                            highest_tuple[1] = tuple[1]
                        elif tuple[1] == word:
                            highest_tuple[0] = word
                            highest_tuple[1] = tuple[0]
            #We print the highest tuple for this word and we save it to the list of highest cosine similarities
            print(highest_tuple)
            list_to_print.append(highest_tuple[0] + " -> " + highest_tuple[1] + ", " + str(highest_tuple[2]))
        file.write('\n'.join(list_to_print)) #saving the results in a separate file

#We compute the cosine similarity
get_highest_similarities(wordlist, compute_all_similarities(wordlist))
print("Process finished. Please find the results in the highest_results_only.txt")

