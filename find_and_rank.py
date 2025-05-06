import spacy
nlp = spacy.load("en_core_web_sm")

#Very similar to naive pattern seraching algorithm:
#Reference: https://www.geeksforgeeks.org/naive-algorithm-for-pattern-searching/
def find_exact_phrase_matches(inverted_index, query_words):
    #Check first word exists; If not, don't even bother checking.
    first_word =query_words[0] 
    remaining_words = query_words[1:]
    if first_word not in inverted_index: return []  

    scores = {} 
    # Loop trhough each page where the first word exists...
    for url, first_word_positions in inverted_index[first_word].items():
        for pos in first_word_positions: 
            match_found = True

            #Given we have a first word, loop through each remaining word and check if they appear all in correct position...
            for i in range(len(remaining_words)):
                word = query_words[i+1]

                #Must check all this:
                #1: the next remaining_word exists in the inverted_index
                #2: the next remaining_word exists in the same current URL
                #3: the next remaining_word is at the next position
                if (
                    word not in inverted_index or
                    url not in inverted_index[word] or
                    (pos+i+1) not in inverted_index[word][url]
                ):
                    match_found = False
                    break
                 
            if match_found:
                #add 1 to score for that url (i.e. number of exact phrases encountered in that url):
                scores[url] = scores.get(url, 0) + 1

    # Sort by score
    scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return scores

#Adds the number of times each query word appears in each URL 
def find_word_matches(inverted_index, query_words):
    scores = {}

    for word in query_words:
        if word not in inverted_index: #skip word if not found
            continue
        for url, positions in inverted_index[word].items():
            # Increment the score for this URL by the num of times the word appears...
            scores[url] = scores.get(url, 0) + len(positions)

    # Sort by score
    scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return scores
