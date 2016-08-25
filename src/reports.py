from db import DBManager


"""
Generates a report that shows the overlap between any
two searches.
"""
def generateReportCrossover(db):
    listTable = []
    searches = db.getSearches()

    # Setting up the first CSV line in the report
    firstLine = ['Total', 'Total']  # Should be search name, total?
    for s in searches:
        firstLine.append(s[1])

    listTable.append(firstLine)

    # Preparing the second line. Line of totals so are just getting single counts
    secondLine = ['Total', '']
    for s in searches:
        # s[0] is the text of a search query
        secondLine.append(str(len(db.getSearchResults(s[0]))))

    listTable.append(secondLine)

    for s in searches:
        # s[0] is the id of a search in the database
        # s[1] is the text of the search query
        line = [s[1], str(len(db.getSearchResults(s[0])))]
        for other in searches:
            # The function being called takes two search IDs and gets
            # the number of overlapping publications
            line.append(str(len(db.getOverlappingResults(s[0], other[0]))))
        listTable.append(line)

    return listTable


"""
Generates a report showing the number of publications
for a search for each year.

This function is essentially a printing function for the return
value of DBManager.getSearchesByYear()
"""
def generateReportByYear(db):
    listTable = []

    years = {}
    # The real meat of this function
    searches = db.getSearchesByYear()
    keys = searches.keys()

    # Create the first line of search text
    firstLine = ['Year']
    for s in keys:
        firstLine.append(s)
        for y in searches[s].keys():
            if y not in years:
                years[y] = []
            years[y].append(searches[s][y])

    listTable.append(firstLine)

    yearKeys = sorted(years.keys())

    # for each year, create the line and write the counts for each search
    for y in yearKeys:
        line = []
        line.append(y)
        for count in years[y]:
            line.append(count)
        listTable.append(line)

    return listTable


"""
    Generates a report for the number of contributing authors compared to each search.
"""
def generateAuthorReport(db):
    listTable = []

    numAuthors = len(db.getAuthors())
    searchCounts = db.getSearchesToAuthorCount()

    searches = searchCounts.keys()

    firstLine = ['Search', 'Total']
    secondLine = ['Num Authors', numAuthors]
    for s in searches:
        firstLine.append(s)
        secondLine.append(searchCounts[s])

    listTable.append(firstLine)
    listTable.append(secondLine)

    return listTable


def main():
    pass


if __name__ == "__main__":
    main()
