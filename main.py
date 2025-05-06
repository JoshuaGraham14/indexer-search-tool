import json
from crawler import *

inverted_index = {}

def build():
    quotes_hashmap = fetch_quotes()
    build_inverted_index(quotes_hashmap)

def load():
    global inverted_index
    try:
        with open("inverted_index.json", "r") as f:
            inverted_index = json.load(f)
        print("Inverted index loaded successfully.")
    except FileNotFoundError:
        print("Index file not found. You must run 'build' command first.")

def print_index(word):
    word = word.lower() 

    if word in inverted_index: 
        print(f"{word}: {inverted_index[word]}") 
    else:
        print(f"Word '{word}' can not be found in the index.") 

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
                if inverted_index == {}:
                    print("Index is empyty. Please load the index from the file system. Usage: 'load'.")
                else:
                    print_index(args[0])
        # elif command == "find":
        #     if len(args) < 2:
        #         print("⛔️ Usage: find <words>")
        #     else:
        #         find(args) 
        elif command == "exit":
            print("Exiting the application... Bye!")
            break 
        else:
            print("Unknown command. Try again")

if __name__=="__main__":
    main()