import json
from crawler import *
from find_and_rank import *

inverted_index = {}

def build():
    pages_content_dict = crawl_pages()
    build_inverted_index(pages_content_dict)

def load():
    global inverted_index
    try:
        with open("inverted_index.json", "r") as f:
            inverted_index = json.load(f)
        print("Inverted index loaded successfully.")
    except FileNotFoundError:
        print("Index file not found. You must run 'build' command first.")

def print_index(word):
    if not inverted_index:
        print("Index is empyty. Please load the index from the file system. Usage: 'load'.")
        return
    
    word = word.lower() 

    if word not in inverted_index:
        print(f"Word '{word}' can not be found in the index.")
        return

    print(f"\nPrinting inverted index for '{word}'...")
    print("-" * 140)
    print(f"{'URL':<80} | {'Count':<10} | Positions")
    print("-" * 140)
    for url, positions in inverted_index[word].items():
        print(f"{url:<80} | {len(positions):<10} | {positions}")
    print("-" * 140)

def find(query_words):
    if not inverted_index: 
        print("Index is empyty. Please load the index from the file system. Usage: 'load'.")
        return

    query_words = [word.lower() for word in query_words] 
    exact_matches = find_exact_phrase_matches(inverted_index, query_words)
    word_matches = find_word_matches(inverted_index, query_words)
    combined_scores = {} 

    #Add a weighted score for all exact phrase matches 
    for url, score in exact_matches:
        combined_scores[url] = combined_scores.get(url, 0) + score * 5  #Increase weight of finding an exact match by 5.
    #Add each score for each sinlge word matches
    for url, score in word_matches:
        combined_scores[url] = combined_scores.get(url, 0) + score

    #Sort scores in order
    ranked_urls = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)

    if not ranked_urls: 
        print("No results found.")
        return 
 
    print("--- Ranked Search Results ---")
    print("-" * 100)
    print(f"{'Results':<80} | {'Score':>6}")
    print("-" * 100) 
    for url, score in ranked_urls:
        print(f"{url:<80} | {score:>6}")
    print("-" * 100) 

#----------------------------------

def main():
    print("--- Welcome to CW2 Search Tool ---")
    print("Type 'exit' to quit")
 
    while True:
        command_input = input("> ").strip()
        command_parts = command_input.split(" ")
        command = command_parts[0].lower()
        args=command_parts[1:] #gets args (i.e. input after 'command' word)
        
        if command == "build":
            build()
        elif command == "load":
            load() 
        elif command == "print":
            if len(args) < 1:
                print("⛔️ Usage: find <words>")
            else:
                print_index(args[0])
        elif command == "find":
            if len(args) < 1:
                print("⛔️ Usage: find <words>")
            else:
                find(args) 
        elif command == "exit":
            print("Exiting the application... Bye!")
            break 
        else:
            print("Unknown command. Try again")

if __name__=="__main__":
    main()