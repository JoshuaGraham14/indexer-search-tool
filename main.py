from crawler import *

def build():
    quotes_hashmap = fetch_quotes()
    build_inverted_index(quotes_hashmap)

#----------------------------------

def main(): 
    print("--- Welcome to CW2 Search Tool ---")
    print("Type 'exit' to quit")
 
    while True:
        # command_input = input("> ").strip()
        command_input = "build"
        command_parts = command_input.split(" ")
        command = command_parts[0].lower()
        args=command_parts[1:] #gets args (i.e. input after 'command' word)
        
        if command == "build":
            build()
            break
        # elif command == "load":
        #     load() 
        # elif command == "print":
        #     print()
        # elif command == "find":
        #     if len(args) < 2:
        #         print("⛔️ Usage: find <words>")
        #     else:
        #         find(args[0], args[k]) 
        elif command == "exit":
            print("Exiting the application... Bye!")
            break 
        else:
            print("Unknown command. Try again")

if __name__=="__main__":
    main()