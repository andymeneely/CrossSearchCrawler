# CrossSearchCrawler [![Build Status](https://travis-ci.org/rywils21/CrossSearchCrawler.svg?branch=master)](https://travis-ci.org/rywils21/CrossSearchCrawler)

CrossSearchCrawler began as a web crawler for IEEE Xplore and ACM digital libraries. It is much much easier to traverse those sites manually and download the citation information from searches. Thus, this tool is now just a citation data aggregation and analysis tool for searches from IEEE Xplore.

Please refer the [guide](#guide-exporting-search-results-from-ieee-xplore) for more information on the nuances of exporting search results from IEEE Xplore.

# Usage
Starting from scratch? Build the entire database and generate all reports by executing this command from the src folder of this project:

```shell
	python main.py do-everything ../searchesFrom_1998/(csv file here)
```

Of course, substitute the python call with the call to run python files on your machine. Python 3 is required.

./searchesFrom_1998 is a folder that contains data files downloaded from IEEE Xplore. You can of course use any CSV files downloaded from there as your source. More on that later.


Other commands that are available are:


```shell
	python main.py report-crossover
```

report-crossover does not load any files. It simply generates a crossover report of all the data currently populated in the database.


```shell
	python main.py report-by-year
```

report-by-year does not load any files. It simply generates a report showing how many results there were for each search query compared to years.


```shell
	python main.py report-by-authors
```

report-by-authors does not load any files. It simply generates a report showing the count of contributing authors for each search query.


```shell
	python main.py compile-folder /path/to/folder/ /output/file/name/
```

This command is used to compile a folder of small CSV files into a single larger CSV file. This was created in order to compile search results from multiple files that were produced from the same search. This is needed when a single search returns more than 2,000 results, and results must be downloaded page by page.


```shell
	python main.py validate-csv /path/to/folder/
```

validate-csv validates csv files within the folder that give to it. This is needed because IEEE Xplore escapes commas with double quote characters. Sometimes the way the escaping is done breaks valid CSV. Thus, raw data downloaded from IEEE Xplore must be validated to ensure that it will work with this script.


```shell
	python main.py load /path/to/folder/
```

load loads data from files in the input folder and puts those entries into the database. It is assumed that the only files in the folder are validated (using validate-csv) CSV files downloaded from IEEE Xplore.

# Shell Commands
The shell can be used for doing queries on the fly and for comparing the overlap between any number of searches. Searches are done by the database id. To start the shell, from the src directory, run:

```shell
python main.py shell
```
or
```shell
python shell.py
```
Both commands will take you to the same place. None of the shell commands are case sensitive. Once you're in the shell, here's what you can do:

To get out of the shell, you can use 'q', 'quit',  or 'exit'.
```shell
>q
>Q
>quit
>Quit
>exit
>Exit
```
Any of those will work.

To get the overlap of any number of searches, use 'count':
```shell
>count ID1 ID2 ... IDn
```
This command will get the number of publications that were returned for any combination of searches. The search ids in this command are separated by whitespace.

To get a list of the search query's IDs, just type 'search-ids' or 'ids'.
```shell
>search-ids
```
This will return a list of all of the ids mapped to their search query for all the saved searches in the database.

Don't want to have to print that every time to look up an id? Keep it handy by saving it to a file with 'save-searchids' or 'save-ids':
```shell
>save-ids /path/to/file
```
This command will take that same list printed by 'search-ids' and save it to a file for you to keep open for reference.

Want to see actual publication information from overlap queries instead of just the count? You're in luck! Use 'save-count'
```shell
>save-count /path/to/file ID1 ID2 ... IDn
```
This will find the overlap between any number of search IDs and print the publications id, title, year, and doi to the output file that you gave the path of.

Want to see how many publications 2 queries have in common per year?
```shell
>print-annual ID1 ID2
```
This will print the search text of queries ID1 and ID2, then show how many publications the two have in common each year.

Want to see how many publications up to 3 categories have in common? Use 'print-categories' or 'pc'
```shell
print-categories CATEGORY1 CATEGORY2 CATEGORY3
```
This will print the number of overlapping results for 3 search categories that are defined in the categories dict in shell.py.

Confused while in the shell? Type 'help' to get this same explanation right there!
```shell
>help
```

That's pretty much it for now. This will get expanded as more features are added.

# Guide: Exporting Search Results from IEEE Xplore

The CrossSearchCrawler works off of the search results exported from IEEE Xplore. The CSV file exported from IEEE Xplore has to be manually modified for CrossSearchCrawler to be able to parse it correctly. The _only_ manual change to the CSV file is to append, as fields, the metric that the results are associated with, the search string used to generate the results, and the literal "IEEE" to first line of the exported CSV file.

## IEEE Xplore Restriction

The export feature on IEEE Xplore restricts the number of results that can be exported to a CSV to 2000. If a search returns more than 2000 results, the results will have to be exported in chunks and manually combined into a single CSV file.

If none of the results displayed are selected, IEEE Xplore exports the first 2000 results by default. The subsequent results have to be selected to be exported. The "Select All" feature may be used but the number of results per page is restricted to a maximum of 100. As a consequence, exporting 2500 results requires manual aggregation of six files: default with 2000 results and five files with 100 results each. Fortunately, the number of results to show is controlled by a query string parameter, `rowsPerPage`, which can be set to a maximum of 2000. Overcoming the restriction to not show more than 100 results per page reduces the number of CSV files that must be manually aggregated.

**Remember**: When aggregating multiple CSV files, remove the header rows (first two rows) from all files except the file containing the first 2000 results (i.e. the default file).
