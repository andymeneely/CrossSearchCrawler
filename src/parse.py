def is_ascii(s):
    """Checks if a character is valid ascii.

    This was made to deal with weird characters in the CSV data files.
    """
    return all(ord(c) < 128 for c in s)


def parseCSVLine(line, headerNames):
    """
    Parses a single line of CSV text into a dictionary.

    Parameters:
        line: single line of CSV text
        headerNames: a list of names of headers of the CSV file

    Returns:
        A dictionary with headerNames values as the keys and the text value
        from the CSV line
    """
    entry = {}
    i = 0
    currentItem = ""
    openQuoteCount = 0
    char = ""
    # Parsing character by character
    for count in range(0, len(line)):
        char = line[count]
        # As long as there are more header names
        if i < len(headerNames):
            # if it's a comma and it's not escaped, save the item to the
            #  dictionary
            if char == ',' and openQuoteCount == 0:
                entry[headerNames[i]] = currentItem
                i += 1
                currentItem = ""
            # if there were no open quotes and this is a quote, it's an open
            #  quote
            elif char == '"' and openQuoteCount == 0:
                openQuoteCount += 1
            # else, this quote is a close quote
            elif char == '"':
                openQuoteCount -= 1
            # Not a special case. Just save the character to the current string
            else:
                currentItem += char
        else:
            break

    # Add on the last item
    if char != ',' and i < len(headerNames):
        entry[headerNames[i]] = currentItem

    # Initialize all of the headerNames into the dictionary with an empty value
    while i < len(headerNames):
        entry[headerNames[i]] = ""
        i += 1

    return entry


def parseFile(filePath):
    """
    This function parses an entire CSV data file.

    Parameters:
        filePath: the path to the file in which to parse

    Returns:
        searchDetails: A dictionary with details about the search.
            Specifically the search site and the search text
        entries: A list of dictionaries of each csv line in the file
    """
    csvFile = open(filePath, mode="r", errors="ignore").read()

    # Get the contents of the file and ensure every character is valid ascii
    contents = []
    currentLine = ""
    for char in csvFile:
        if is_ascii(char):
            if char == "\n":
                contents.append(currentLine)
                currentLine = ""
            elif char == '\t':
                currentLine += ","
            else:
                currentLine += char
        else:
            pass

    firstLine = contents[0].strip().strip(',')
    # Get the search details from the first line
    searchDetails = parseCSVLine(
            firstLine, ['url', 'date', 'metric', 'query', 'site']
        )

    headerLine = contents[1]
    fieldNames = headerLine.replace('"', '').strip().split(',')

    contents = contents[2::]

    # iterate and parse each line with parseCSV Line
    entries = []
    for line in contents:
        entry = parseCSVLine(line, fieldNames)
        if not containsStopWords(entry):
            entries.append(entry)

    return searchDetails, entries


def containsStopWords(entry):
    """Checks if any publication titles contain stopwords. Stopwords are words
    that make it blatantly obvious that the paper is not applicable to this
    study.

    Parameters:
        entry: a parsed CSV line as a dictionary. Like one returned from
            parseCSVLine
    """
    stopWords = [
            'table of content', 'abstract', 'content', 'preface',
            'front matter', 'title page', 'program guide',
            'program at a glance', 'list of papers', 'technical program',
            'author index', 'tutorial', 'conference program',
            'general session', 'front cover', 'keyword index', '- toc',
            'book of abstracts'
        ]

    if 'Document Title' in entry:
        title = entry['Document Title'].lower().strip('[]')
    elif 'Title' in entry:
        title = entry['Title'].lower().strip('[]')
    else:
        title = ""

    for word in stopWords:
        if title.startswith(word) or title.endswith(word):
            return True

    return False


def zoteroToIEEE(zoteroEntries):
    """Converts entries generated from Zotero exported files to be able to
    work with IEEE exported files.

    It does this by adding IEEE header names to the entry dictionaries with
    the same value as the corresponding Zotero header.
    """
    # Dictionary of key, values where the keys are zotero headers and values
    #  are IEEE equivalent headers
    transfers = {
            'Title': 'Document Title', 'Author': 'Authors', 'Url': 'PDF Link',
            'Publication Year': 'Year'
        }
    converted = []

    for entry in zoteroEntries:
        newEntry = {}
        for k in entry.keys():
            # If k needs to be converted
            if k in transfers.keys():
                # Add k's value to the dictionary with entry[k]'s value
                newEntry[transfers[k]] = entry[k]
            elif k == "Pages":
                # Parsing the start pages
                if "-" in entry[k]:
                    newEntry["Start Page"] = entry[k].split("-")[0]
                    newEntry["End Page"] = entry[k].split("-")[1]
                else:
                    newEntry["Start Page"] = ""
                    newEntry["End Page"] = ""
            else:
                newEntry[k] = entry[k]
        converted.append(newEntry)

    return converted


def reportToCSV(report):
    """Converts a list of lists into a CSV file.

    Parameters:
        report: a list of lists

    Returns:
        content: a single string that in CSV format generated from report.
                Each top level list became a line and the sub lists' contents
                were separated by commas.
    """
    content = ""
    for line in report:
        for s in line:
            content += str(s) + ","
        content += "\n"

    return content


def linesToCSV(report):
    """Converts a list of lines to a single string

    Parameters:
        report: a list of lines of text

    Returns:
        content: a single string of concatenated lines with a newline character
            in between each one
    """
    content = ""
    for line in report:
        content += line + "\n"

    return content


def getCSVHeader(filePath):
    """Gets the first two lines of a file and returns them as a single string.

    Parameters:
        filePath: the page to the CSV file

    Returns:
        header: A string for a header to an IEEE CSV citation data file
    """
    csvFile = open(filePath, mode="r", errors="ignore").read()

    lineCount = 0
    contents = []
    currentLine = ""
    for char in csvFile:
        # Only parse the first two lines because that's where the header is
        if lineCount < 2:
            if is_ascii(char):
                if char == "\n":
                    contents.append(currentLine)
                    lineCount += 1
                    currentLine = ""
                elif char == '\t':
                    currentLine += ","
                else:
                    currentLine += char
        else:
            break

    header = contents[0].strip().strip(',') + "\n" + \
        contents[1].replace('"', '').strip().strip(",")

    return header


def resultsFileToLists(filePath):
    """Extracts each data entry line from a CSV data file

    Parameters:
        filePath: the path to a CSV data file

    Returns:
        contents: a list of CSV lines

    """
    csvFile = open(filePath, mode="r", errors="ignore").read()

    contents = []
    currentLine = ""
    for char in csvFile:
        if is_ascii(char):
            if char == "\n":
                contents.append(currentLine)
                currentLine = ""
            else:
                currentLine += char
        else:
            pass

    return contents


def validateCSVLine(line):
    """Removes unecessary double quote (") characters from CSV lines.

    IEEE exports some files with double quotes escaping commas in value fields,
    but does so poorly and it invalidates CSV.

    Parameters:
        line: the CSV line

    Returns:
        newLine: the fixed CSV line
    """

    # Replace triple quotes with double quotes
    line = line.replace('\"\"\"', '\"\"')
    # Start with the first character
    newLine = line[0]

    if newLine == '"':
        quoteCount = 1
    else:
        quoteCount = 0

    for i in range(1, (len(line)-1)):
        char = line[i]
        lastChar = line[(i-1)]
        nextChar = line[(i+1)]

        if char == '"':
            quoteCount += 1
            if nextChar == ',' and (quoteCount % 2) == 0:
                newLine += char
            elif lastChar == ',' and quoteCount == 1:
                newLine += char
        elif char == ',' and (quoteCount % 2) == 0:
            quoteCount = 0
            newLine += char
        else:
            newLine += char

    if line[(len(line)-1)] == '"' or line[(len(line)-1)] == ',':
        newLine += line[(len(line)-1)]

    return newLine


def validateCSVfile(filePath):
    """Removes bad quotes from an entire CSV data file.

    Parameters:
        filePath: the path to a CSV data file

    Returns:
        contents: A string that is the cleansed contents of the CSV file

    """
    # Assumes that filePath has been checked to exist
    print("Cleaning CSV for: " + filePath)
    finalEntries = []
    header = getCSVHeader(filePath)
    finalEntries.append(header)
    entries = resultsFileToLists(filePath)
    finalEntries += entries

    contents = ""
    for entry in finalEntries:
        entry = validateCSVLine(entry)
        contents += entry + "\n"

    return contents


def compileFolder(filePaths):
    """Compiles a folder of CSV files that were downloaded page by page from
    IEEE.

    This happens when a search returns more than 200 results, they must be
    downloaded page by page.

    Parameters:
        filePaths: a list of filePaths for each file to be compiled into one

    Returns:
        contents: a string of all of the data from all the files. Can be
            written to a file or parsed.
    """

    finalEntries = []

    header = parse.getCSVHeader(filePaths[0])
    finalEntries.append(header)
    for f in filePaths:
        # Results file to lists leaves out the file headers and just gets the
        #  entries
        entries = parse.resultsFileToLists(f)
        finalEntries += entries

    contents = parse.linesToCSV(finalEntries)

    return contents


def main():
    print("Sorry, this file doesn't have anything to run.")


if __name__ == "__main__":
    main()
