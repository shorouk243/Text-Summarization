# NLP Pkgs
import spacy 
nlp = spacy.load('en_core_web_sm') # load the model (English) into spaCy
# Pkgs for Normalizing Text
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
# Import Heapq for Finding the Top N Sentences
# Heap is a data structure
from heapq import nlargest # returns the specified number of largest elements


# Defining the text_summarizer function
def text_summarizer(raw_docx):# takes a raw_docx paramete which represents the input text to be summarized.
    raw_text = raw_docx # Assigns the input text to the raw_text variable.
    docx = nlp(raw_text) # It processes the raw_text using the spaCy language model (nlp) and assigns the processed document to the docx variable.
    stopwords = list(STOP_WORDS) # The stopwords are loaded into the stopwords list
    # This code calculates the frequency of each word in the document (docx) 
    # and stores it in the word_frequencies dictionary.
    word_frequencies = {}  # Initializes an empty dictionary word_frequencies to store the frequency of each word in the document.
    for word in docx: # Iterate over each word in the document.
        if word.text not in stopwords: # And checks if the word is not a stopword.
            if word.text not in word_frequencies.keys(): # The code checks if the current word is not already a key in the word_frequencies dictionary. 
                word_frequencies[word.text] = 1 # If it's not present, it means this is the first occurrence of the word, so the code adds it to the dictionary with an initial frequency of 1.
            else:
                word_frequencies[word.text] += 1 # If the current word is already a key in the word_frequencies dictionary, it means the word has occurred before. In this case, the code increments the frequency of the word by 1.

# The code calculates the maximum frequency of any word in the document.
    maximum_frequncy = max(word_frequencies.values()) 

    for word in word_frequencies.keys(): # The code checks if the current word is already a key in the word_frequencies dictionary. 
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy) #  This division normalizes the word frequency by scaling it to a value between 0 and 1.

    # Sentence Tokens
    sentence_list = [ sentence for sentence in docx.sents ]

    # Sentence Scores
    sentence_scores = {} # Initializes an empty dictionary sentence_scores to store the scores of each sentence.
    for sent in sentence_list:  
        for word in sent: # Iterate over each word in the sentence:
            if word.text.lower() in word_frequencies.keys(): # Check if the word is in the word_frequencies dictionary
                if len(sent.text.split(' ')) < 30: # Checks if the current sentence has less than 30 words. This condition is used to filter out very long sentences that may not be suitable for summarization.
                    if sent not in sentence_scores.keys(): # If the sentence is not already a key in the sentence_scores dictionary, it assigns the word frequency as the initial score for that sentence. If the sentence is already a key in the dictionary, it adds the word frequency to the existing score.
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]

    # uses nlargest from heapq to select the top 7 sentences based on their scores from the sentence_scores dictionary. It then extracts the text of these sentences and joins them together with a space to form the summary. 
    summarized_sentences = nlargest(7, sentence_scores, key=sentence_scores.get)
    final_sentences = [ w.text for w in summarized_sentences ]
    summary = ' '.join(final_sentences)
    return summary
    
# In summary, the text_summarizer function takes an input text,
# processes it using spaCy, calculates word frequencies,
# assigns scores to sentences based on word frequencies, 
# selects the top sentences, and returns the summary of the input text.

# 1- Filtering tokens 
# 2- Normalization
# 3- Weighing sentences
# 4-  Summarizing the string