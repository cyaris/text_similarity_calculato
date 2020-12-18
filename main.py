import string
from copy import deepcopy

## function to submit the text.
def submit_text(number_input):

    text = input("\nPlease enter text number {} > ".format(number_input))
    print("\nYou've submitted: \"{}\"".format(text))
    input_evaluation = input("\nIf you'd like to resubmit, enter \"yes\" > ")

    return [text, input_evaluation]

## function to run the text submission process, including resubmission.
def submit_text_process(number_input):

    submit_text_output = submit_text(number_input)
    text = submit_text_output[0]
    input_evaluation = submit_text_output[1]
    ## overwriting text upon check
    text = input_check(text, input_evaluation, number_input)

    return text

## allowing for text inputs inputs to be resubmitted if the user wishes.
def input_check(text, input_evaluation, number_input):

    while input_evaluation=='yes':
        submission_output = submit_text(number_input)
        text = submission_output[0]
        input_evaluation = submission_output[1]

    print("\nGlad you're satisfied with text number {}!".format(number_input))

    return text

## First, I'm going to remove any punctuation from both texts, and compare them based on their words alone.
## I'll also make all words lowercase.
def remove_punctuation_from_text(text_input, number_input):

    # print("\nRemoving punctuation from Text {}...".format(number_input))
    original_text_length = deepcopy(len(text_input))
    text_input = text_input.translate(str.maketrans('', '', string.punctuation))
    # print("Total punctuation characters removed from Text {}: {}".format(number_input, original_text_length - len(text_input)))
    # print("Making all characters in Text {} lowercase...".format(number_input))
    text_input = text_input.lower()

    return text_input

## function below counts total words between both lists.
## No word can be counted more than the lowest number of times it appeared in either list.
## See next function for further documentation.
def get_total_words(list_input_1, list_input_2):

    ## note: only need to iterate over one list because we will add the total words from one list with the remainder from the other
    list_input_2_copy = deepcopy(list_input_2)
    for word in list_input_1:
        if word in list_input_2_copy:
            list_input_2_copy.remove(word)

    total_words = len(list_input_1) + len(list_input_2_copy)

    return total_words

## Function below counts total overlapping words between both lists.
## No word can be counted more than the lowest number of times it appeared in either list.

## For example, consider these two possible inputs:
## Input 1: \"I love ice cream and I love pizza.
## Input 2: \"Love is a powerful word
## The total overlapping words here would be 1. "Love" is the only word that appears in both texts.
## It can only be counted once though because it only appears in the second text once.
## Here's one more example to make sure this is all clear.

## Consider these two possible inputs:
## Input 1: "blah blah hi friend blah blah blah blah blah"
## Input 2: "hi friend stop saying blah blah"
## The total overlapping words here would be 4. 1 for "hi," 1 for "friend," and 2 for "blah."
## Blah is counted twice because the lowest number of occurances it had between both lists was 2.

def count_word_list_overlap(list_input_1, list_input_2):

    ## note: only need to iterate over one list because the overlap cannot be in one and not the other
    word_overlap = 0
    overlapped_words = []
    list_input_2_copy = deepcopy(list_input_2)
    for word in list_input_1:
        if word in list_input_2_copy:
            word_overlap+=1
            overlapped_words.append(word)
            list_input_2_copy.remove(word)

    return [word_overlap, overlapped_words]

## this function is repeatedly called in evaluate_word_combination_overlap, inside of a while loop.
## its purpose is to iterate over possible phrases (starting with a single word) until the phrase is no longer an exact match.
def phrase_counter(text_input_1, text_input_2, overlapped_words_input, word_overlap_indice):

    phrase_length = 0
    for i, word in enumerate(overlapped_words_input[word_overlap_indice:]):

        if i==0:
            current_phrase = word
            phrase_length = 1
        else:
            previous_phrase = deepcopy(current_phrase)
            current_phrase = current_phrase + ' ' + word
            phrase_length+=1
        if current_phrase not in text_input_1 or current_phrase not in text_input_2:
            phrase_length-=1
            break
        else:
            final_phrase = current_phrase

    return [phrase_length, final_phrase]

## function returns a list of each exact match phrase between the two lists.
## note: word overlap has already been calculated and will be used as an input.
def evaluate_word_combination_overlap(overlapped_words_input, text_input_1, text_input_2):

    word_overlap_indice = 0
    phrase_match_score = 0
    phrase_matches = []

    while word_overlap_indice < len(overlapped_words_input):

        phrase_counter_ouput = phrase_counter(text_input_1, text_input_2, overlapped_words_input, word_overlap_indice)
        phrase_length = phrase_counter_ouput[0]
        phrase_match_score+=(phrase_length*phrase_length)
        word_overlap_indice+=phrase_length

        if phrase_length > 1:
            phrase_matches.append(phrase_counter_ouput[1])

    return [phrase_match_score, phrase_matches]

print("\nTwo texts are need to run this program.")

text_1 = submit_text_process(1)
text_2 = submit_text_process(2)
print("\nBoth texts have been received.")

text_1 = remove_punctuation_from_text(text_1, 1)
text_2 = remove_punctuation_from_text(text_2, 2)
text_1_words = text_1.split(" ")
text_2_words = text_2.split(" ")

print("\nRunning analysis on text similarity...")
print("No punctuation will be included. All characters will be evaluated in lowercase.")
print("Evaluating word overlap and multi-word (phrase) overlap between the two texts...")
print("Longer phrases (by total words) will be given higher weights than shorted phrases.")

word_overlap_output = count_word_list_overlap(text_1_words, text_2_words)
word_overlap = word_overlap_output[0]
overlapped_words = word_overlap_output[1]

print("\n–––––Word Metrics–––––")
print("\nTotal Word Text 1: {}".format(len(text_2_words)))
print("Total Word Text 2: {}".format(len(text_2_words)))
print("Total Overlapping Words: {}".format(word_overlap))
print("Overlapping Words List: {}".format(overlapped_words))

phrase_match_ouput = evaluate_word_combination_overlap(overlapped_words, text_1, text_2)
phrase_match_score = phrase_match_ouput[0]
phrase_matches = phrase_match_ouput[1]

print("\n–––––Phrase Metrics–––––")
print("\nTotal Multi-Word Phrases: {}".format(len(phrase_matches)))
print("Phrase Match List: {}".format(phrase_matches))

total_words_between_both_lists = get_total_words(text_1_words, text_2_words)

print("\n–––––Text Similarity–––––")
## the denominator is the total_words_between_both_lists squared.
## numerator is the summation of the total words in each phrase squared.
## this includes single word phrases (regular overlapping words)
## the idea here is that the same words in a totally different order should get credit, but nowhere near as much credit as the same words in the same order.
text_similarity_denominator = total_words_between_both_lists*total_words_between_both_lists
print("\nText Similarity Score: {}\n".format(phrase_match_score/text_similarity_denominator))
