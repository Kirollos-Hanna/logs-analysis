# Description

The program uses python and psycopg2 to make queries to an SQL database and outputs the results in a simple text file. The queries include joining multiple tables to get the desired information and is presented in an easy to read format for interested readers.

## Requirements

- Python 3: [Download the latest version of Python here](https://www.python.org/downloads/)
- PostgreSQL: [Download from here](https://www.postgresql.org/download/)
- psycopg2: [Installation instructions](http://initd.org/psycopg/download/)
- if you're on windows, download [git bash](https://git-scm.com/downloads)

## How to run

- Download the [news database](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
- `cd` into the project directory.
- unzip the news database in the directory.
- run the command `psql -d news -f newsdata.sql`. (Make sure to download all the required software for this to work)
- use the `python` or `python3` command with the logsanalysis.py file from your command line. (i.e. `python logsanalysis.py`)
- The program will run for a while and will output the results into the output.txt file. (nothing will be output in the command line)

## How it works

- The program first connects to the news database and creates a cursor.
- It then performs three queries, namely:
  1. Finding the three most popular articles.
  2. Listing the most popular authors by article page views.
  3. Finding the days where more than 1% of requests to the website led to errors.
- The query results are then saved into strings and appended into the output.txt file.
