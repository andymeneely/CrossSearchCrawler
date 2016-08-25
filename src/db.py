import sqlite3
import os


"""
An class for handling all of the operations with the database.
"""
class DBManager:

    """
    The constructor function of this object.

    When a object of this class is instantiated, a database
    connection is established and then the sql script is executed
    to ensure that all of the tables and indexes exist.
    """
    def __init__(self, connection="searches.db"):
        self.connectionFilePath = connection
        self.conn = sqlite3.connect(connection)
        self.cursor = self.conn.cursor()

        self.initializeTables()

    """
    Executes the sql script to create the tables and indexes.
    """
    def initializeTables(self):
        commands = open('sql_commands.sql', 'r').read()
        self.cursor.executescript(commands)

    """
    Given a search and result entries, enters that data into the database.
    """
    def putSearchResults(self, searchDetails, entries):

        searchID = self.putSearch(searchDetails)
        for entry in entries:
            entryID = self.putEntry(entry)
            self.putSearchLink(searchID, entryID)

    """
    Enters data for a single search into the database.
    """
    def putSearch(self, search):
        exists = False

        # Check if this search has been inserted yet
        idSql = 'SELECT id FROM searches WHERE searchText="%s" AND site="%s";' %(search['query'], search['site'])
        self.cursor.execute(idSql)
        results = self.cursor.fetchall()
        if len(results) > 0:
            exists = True

        # If it doesn't exist, insert it
        if not exists:
            sql = 'INSERT INTO searches (searchText, site) VALUES ( "%s", "%s");' %(search['query'], search['site'])
            self.cursor.execute(sql)

        # Get the ID
        self.cursor.execute(idSql)
        idVal = self.cursor.fetchone()

        return idVal[0]

    """
    Enters data for a single publication into the database.
    """
    def putEntry(self, entry):
        exists = False

        idSql = 'SELECT id FROM publications WHERE title="%s" AND year="%s" AND doi="%s" AND isbn="%s" AND issn="%s"' % (entry['Document Title'], entry['Year'], entry['DOI'], entry["ISBN"], entry["ISSN"])
        self.cursor.execute(idSql)
        results = self.cursor.fetchall()

        if len(results) > 0:
            exists = True

        if not exists:
            sql = 'INSERT INTO publications (title, year, doi, isbn, issn, url, startpage, endpage) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");' % (entry['Document Title'], entry['Year'], entry['DOI'], entry['ISBN'], entry['ISSN'], entry["PDF Link"], entry["Start Page"], entry["End Page"])
            self.cursor.execute(sql)

        self.cursor.execute(idSql)
        idVal = self.cursor.fetchone()

        for author in entry["Authors"].split(";"):
            authorID = self.putAuthor(author)
            self.putAuthorPubLink(authorID, idVal[0])

        return idVal[0]

    """
    Enters data for a single author into the database.
    """
    def putAuthor(self, authorName):
        exists = False

        # Check if this search has been inserted yet
        idSql = 'SELECT id FROM authors WHERE name="%s";' %(authorName)
        self.cursor.execute(idSql)
        results = self.cursor.fetchall()
        if len(results) > 0:
            exists = True

        # If it doesn't exist, insert it
        if not exists:
            sql = 'INSERT INTO authors(name) VALUES ("%s");' %(authorName)
            self.cursor.execute(sql)

        # Get the ID
        self.cursor.execute(idSql)
        idVal = self.cursor.fetchone()

        return idVal[0]

    """
    Enters the IDs of a search and publication pair.
    """
    def putSearchLink(self, searchID, entryID):
        exists = False
        idSql = 'SELECT searchID, pubID FROM searchpublink WHERE searchID="%s" AND pubID="%s";' % (searchID, entryID)
        self.cursor.execute(idSql)
        results = self.cursor.fetchall()
        if len(results) > 0:
            exists = True

        if not exists:
            putSql = 'INSERT INTO searchpublink (searchID, pubID) VALUES ("%s", "%s");' % (searchID, entryID)
            self.cursor.execute(putSql)

    """
    Enters the IDs of a author and publication pair.
    """
    def putAuthorPubLink(self, authorID, pubID):
        exists = False
        idSql = 'SELECT authorID, pubID FROM authorpublink WHERE authorID="%s" AND pubID="%s";' % (authorID, pubID)
        self.cursor.execute(idSql)
        results = self.cursor.fetchall()
        if len(results) > 0:
            exists = True

        if not exists:
            putSql = 'INSERT INTO authorpublink (authorID, pubID) VALUES ("%s", "%s");' % (authorID, pubID)
            self.cursor.execute(putSql)

    def getSearches(self):
        sql = "SELECT id, searchText from searches order by id ASC;"
        self.cursor.execute(sql)

        return self.cursor.fetchall()

    def getPublications(self):
        sql = "SELECT id, title, year, doi, startpage, endpage from publications;"
        self.cursor.execute(sql)

        return self.cursor.fetchall()

    def getSearchPubLinks(self):
        sql = "SELECT searchID, pubID from searchpublink;"
        self.cursor.execute(sql)

        return self.cursor.fetchall()

    def getAuthors(self):
        sql = "SELECT id, name FROM authors;"
        self.cursor.execute(sql)

        return self.cursor.fetchall()

    def getAuthorPubLinks(self):
        sql = "SELECT authorID, pubID from authorpublink;"
        self.cursor.execute(sql)

        return self.cursor.fetchall()

    def getSearchResults(self, searchID):
        sql = "SELECT pubID from searchpublink where searchID=%s;" % (searchID)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()

        return results

    def getPubById(self, pubID):
        sql = "SELECT id, title, year, doi from publications where id=%s" % (pubID)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()[0]

        return result

    """
    This function returns a grouping of searches by year.

    The year value is in the publications table. The search query text is in the searches table.

    There is probably a more efficient way to do this in sql but I don't know how to write it.
    """
    def getSearchesByYear(self):
        searches = self.getSearches()
        links = self.getSearchPubLinks()
        pubs = self.getPublications()

        yearCountSQL = "SELECT count(*) FROM publications INNER JOIN searchpublink ON publications.id=searchpublink.pubID WHERE searchpublink.searchID=%s AND publications.year=%s"

        years = []
        y = 1990
        while y < 2016:
            years.append(str(y))
            y += 1

        searchesByYear = {}
        for s in searches:
            searchID = s[0]
            searchText = s[1]
            searchesByYear[searchText] = {}

            for y in years:
                sql = yearCountSQL %(searchID, y)
                self.cursor.execute(sql)
                count = self.cursor.fetchone()[0]
                searchesByYear[searchText][y] = count

        return searchesByYear

    def getSearchesToAuthorCount(self):

        authLinks = self.getAuthorPubLinks()
        searchLinks = self.getSearchPubLinks()

        searches = self.getSearches()

        searchCounts = {}
        for s in searches:
            searchCounts[s[1]] = set()
            for link in searchLinks:
                if link[0] == s[0]:
                    for auth in authLinks:
                        if link[1] == auth[1]:
                            searchCounts[s[1]].add(auth[0])

        for key in searchCounts.keys():
            searchCounts[key] = len(searchCounts[key])

        return searchCounts

    """
    Returns a list of publication IDs that are mapped to both searchIDs in searchpublink
    """
    def getOverlappingResults(self, searchID1, searchID2):

        results1 = self.getSearchResults(searchID1)

        results2 = self.getSearchResults(searchID2)

        results = []
        for r in results1:
            if r in results2:
                results.append(r)

        return results

    """
    Returns a count of overlapping results for 3 categories. Each category is an array of searchID's
    """
    def getCategoryOverlap(self, category1, category2, category3):

        resultsA = []
        resultsB = []
        resultsC = []
        for searchID in category1:
            resultsA += self.getSearchResults(searchID)
        for searchID in category2:
            resultsB += self.getSearchResults(searchID)
        for searchID in category3:
            resultsC += self.getSearchResults(searchID)

        ABoverlap = []
        BCoverlap = []
        ACoverlap = []
        ABCoverlap = []
        for r in resultsA:
            if r in resultsB:
                ABoverlap.append(r)
                if r in resultsC:
                    ABCoverlap.append(r)
            if r in resultsC:
                ACoverlap.append(r)
        for r in resultsB:
            if r in resultsC:
                BCoverlap.append(r)
        print("Overlap results")
        print("A only: " + str(len(resultsA)) + ", B only: " + str(len(resultsB)) + ", C only: " + str(len(resultsC)))
        print("A & B: " + str(len(ABoverlap)) + ", A & C: " + str(len(ACoverlap)) + ", B & C: " + str(len(BCoverlap)) +", A & B & C: " + str(len(ABCoverlap)))

        return

    """
    Returns a list of publication IDs that are mapped to both given searchIDs in searchpublink for a given year
    """
    def getOverlappingYearlyResults(self, searchID1, searchID2, year):
        overlap = self.getOverlappingResults(searchID1, searchID2)
        total1 = self.getSearchResults(searchID1)
        total2 = self.getSearchResults(searchID2)
        firstResults = []
        secondResults = []
        for pubID in total1: #gets total publications for searchID1. Probably not efficient
            sql = "SELECT year from publications where id=%s;" % (pubID)
            self.cursor.execute(sql)
            firstResults += self.cursor.fetchall()
        for pubID in total2: #gets total publications for searchID2. Probably not efficient
            sql = "SELECT year from publications where id=%s;" % (pubID)
            self.cursor.execute(sql)
            secondResults += self.cursor.fetchall()
        results = []
        for pubID in overlap:
            sql = "SELECT year from publications where id=%s;" % (pubID)
            self.cursor.execute(sql)
            results += self.cursor.fetchall()
        yearFormat = ((str(year)),)
        return [results.count(yearFormat), firstResults.count(yearFormat), secondResults.count(yearFormat)]

    """
    Gets the count of publications that overlap for the given list of searchIDs

    Parameters:
        self: this DBManager
        searchIDs: a list of search IDs to get the overlap of

    Returns:
        results: a list of publication entries that were linked to all IDs in searchIDs
    """
    def getOverlapIDs(self, searchIDs):

        if len(searchIDs) > 0:
            sql = "select pubID from searchpublink where searchID=%s " % (searchIDs[0])
            for i in range(1, len(searchIDs)):
                sql += "intersect select pubID from searchpublink where searchID=%s " % (searchIDs[i])
            sql += ";"
            self.cursor.execute(sql)

            return self.cursor.fetchall()

        return []

    def shutdown(self):
        self.conn.commit()
        self.conn.close()

    """
    Close the connection to the database and delete the file.
    """
    def destroy(self):
        self.conn.commit()
        self.conn.close()
        os.remove(self.connectionFilePath)
