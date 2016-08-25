from db import DBManager
categories = {
    'effectiveness': [37, 31, 39, 35, 38, 30, 32, 36, 34, 33],
    'performance': [24, 25, 27, 26, 29, 41, 45, 28, 42, 43, 46, 44, 47, 48, 49, 59, 52, 53, 54, 55],
    'dfas': [19, 20, 21, 22, 23],
    'null': []
}

"""
Called from the shell. Returns the count of publications returned for all of the given search IDs.
"""

def parseCountCommand(db, command):
    # split on whitespace and remove first value which should be "overlap"
    args = command.split()[1::]
    searchIDs = []
    for a in args:
        if a.isdigit():
            searchIDs.append(a)

    result = db.getOverlapIDs(searchIDs)
    print(len(result))


"""
Called from the shell. Prints publication info for the overlapping publications for the searchIDs to an output file.
"""

def parseSaveCountCommand(db, command):
    # split on whitespace and remove first command
    args = command.split()[1::]
    outputFile = args[0]
    args = args[1::]
    searchIDs = []
    for a in args:
        if a.isdigit():
            searchIDs.append(a)

    print("Writing results to: " + outputFile)

    results = db.getOverlapIDs(searchIDs)

    content = "Publication ID, Title, Year, DOI\n"
    for r in results:
        content += str(db.getPubById(r[0])) + "\n"

    with open(outputFile, 'w') as out:
        out.write(content)


"""
Called from the shell. Prints the search ids and their overlap for each year.
"""

def printYearlyOverlap(db, command):
    searches = db.getSearches()
    searchA = int(command[0])
    searchB = int(command[1])
    print("Overlap between '" + searches[searchA - 1][1] + "' and '" + searches[searchB - 1][1] + "'")
    print("year | overlap | first results | second results | percentage overlapping")
    for year in range(1998, 2016):  # can go back to 1990, but IDS not found before 98 anyway!
        count, firstTotal, secondTotal = db.getOverlappingYearlyResults(searchA, searchB, year)
        percentage = "-"
        if firstTotal + secondTotal > 0:
            percentage = str(round(((count / (firstTotal + secondTotal)) * 100), 2))
        print(str(year) + " | " + str(count) + " | " + str(firstTotal) + " | " + str(secondTotal) + " | " + percentage + " %")


"""
Called from the shell. Prints the search ids and their search text to the shell.
"""

def printSearchIDs(db):
    searches = db.getSearches()

    for s in searches:
        print(str(s[0]) + "|" + str(s[1]))


"""
Called from the shell. Saves the list of searches and IDs to a file.

Parameters:
    db: instance of DBManager
    command: the command entered into the shell. The first half is just the string that got this function called.
            The file path to print should be the second part of this string.
"""

def printSearchIDs(db, command):
    searches = db.getSearches()
    path = command.split()
    if len(path) > 1:
        path = path[1]
        content = "search ID | search Query text\n"
        for s in searches:
            content += str(s[0]) + "|" + str(s[1]) + "\n"

        with open(path, 'w') as out:
            out.write(content)
        print("Writing results to: " + path)

    else:
        content = "search ID | search Query text\n"
        for s in searches:
            content += str(s[0]) + "|" + str(s[1]) + "\n"
        print(content)

def printCategories(db, command):
    if len(command) != 3:
        print("Please include 3 categories!")
        return
    for category in command:
        if category not in categories:
            print("Invalid category name! Categories are: " + str(categories.keys()))
            return
    db.getCategoryOverlap(categories[command[0]], categories[command[1]], categories[command[2]])

"""
Called from the shell. Prints out directions for using the shell.
"""

def help():
    print("None of the commands in the shell are case-sensitive. Use whatever you want.\n\n" + \
          "To get out of the shell, you can use 'q', 'quit',  or 'exit'. Any of those will work.\n\n" + \
          "To get the overlap of any number of searches, use 'count': \n\n" + \
          "\t>count ID1 ID2 ... IDn\n\n" + \
          "This command will get the number of publications that were returned for any combination of searches. The search ids in this command are separated by whitespace.\n\n" + \
          "To get a list of the search query's IDs, just type 'search-ids' or 'ids'.\n" + \
          "\t>search-ids\n\n" + \
          "This will return a list of all of the ids mapped to their search query for all the saved searches in the database.\n\n" + \
          "Don't want to have to print that every time to look up an id? Keep it handy by saving it to a file with 'save-searchids' or 'save-ids':\n" + \
          "\t>save-ids /path/to/file\n\n" + \
          "This command will take that same list printed by 'search-ids' and save it to a file for you to keep open for reference.\n\n" + \
          "Want to see actual publication information from overlap queries instead of just the count? You're in luck! Use 'save-count'\n" + \
          "\t>save-count /path/to/file ID1 ID2 ... IDn\n\n" + \
          "This will find the overlap between any number of search IDs and print the publications id, title, year, and doi to the output file that you gave the path of.\n\n" + \
          "Want to see how many publications 2 queries have in common per year? Use 'print-annual' or 'pa'\n" + \
          "\t>print-annual ID1 ID2\n\n" + \
          "This will print the search text of queries ID1 and ID2, then show how many publications the two have in common each year.\n\n" + \
          "Want to see how many publications up to 3 categories have in common? Use 'print-categories' or 'pc'\n" + \
          "\t>print-categories CATEGORY1 CATEGORY2 CATEGORY3\n\n" + \
          "This will print the number of overlapping results for 3 search categories that are defined in the categories dict.\n\n" + \
          "Confused while in the shell? Type 'help' to get this same explanation right here!\n" + \
          "\t>help\n\n"
          )


"""
The main shell of the shell. Entry point for all of the commands.

Parameters:
    db: A DBManager object

Returns:
    Nothing
"""

def run(db):
    print(
        "Entering shell. See documentation or type 'help' for available commands.\nType \"quit\" or \"exit\" to leave.")
    command = input(">")
    while command.lower() != "quit" and command.lower() != "exit" and command.lower() != 'q':

        if command.lower().startswith("count"):
            parseCountCommand(db, command)

        elif command.lower().startswith("save-count"):
            parseSaveCountCommand(db, command)

        elif command.lower().startswith("searchids") or command.lower().startswith("ids"):
            printSearchIDs(db, command)

        elif command.lower().startswith("save-searchids") or command.lower().startswith("save-ids"):
            printSearchIDs(db, command)

        elif command.startswith("print-annual") or command.startswith("pa"):
            if len(command.split()) == 3:
                printYearlyOverlap(db, command.split()[1:])

        elif command.startswith("print-categories") or command.startswith("pc"):
            printCategories(db, command.split()[1:])

        elif command.startswith("help"):
            help()

        else:
            print('"' + command + '" is not supported. See documentation or type help for supported commands.')
        command = input(">")


"""
Entry point of this file.

Just connects to the database and calls run
"""

def main():
    db = DBManager()
    run(db)


if __name__ == "__main__":
    main()
