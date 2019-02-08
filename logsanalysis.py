#!/usr/bin/env python3
import psycopg2
import datetime


def db_connect():
    """
    Create and return a database connection and cursor.

    The functions creates and returns a database connection and cursor to the
    database defined by DBNAME.
    Returns:
        db, c - a tuple. The first element is a connection to the database.
                The second element is a cursor for the database.
    """
    db = psycopg2.connect(database="news")
    return db, db.cursor()


def execute_query(query):
    """
    execute_query returns the results of an SQL query.

    execute_query takes an SQL query as a parameter,
    executes the query and returns the results as a list of tuples.
    args:
    query - an SQL query statement to be executed.

    returns:
    A list of tuples containing the results of the query.
    """
    db, c = db_connect()
    c.execute(query)
    rows = c.fetchall()
    db.close()
    return rows


def print_top_articles():
    """Print out the top 3 articles of all time."""
    query = """
            SELECT articles.title, count(*) AS views
            FROM articles, log
            WHERE log.path = CONCAT('/article/', articles.slug)
            GROUP BY articles.title
            ORDER BY views DESC
            LIMIT 3
            """
    results = execute_query(query)

    mostPopularArticles = "The most popular three articles of all time: \n"
    for articleTitle, viewNum in results:
        mostPopularArticles += '\t"{}" - {} views\n'.format(
            articleTitle, viewNum)

    return mostPopularArticles


def print_top_authors():
    """Print a list of authors ranked by article views."""
    query = """
            SELECT authors.name, count(*) AS views
            FROM articles, log, authors
            WHERE log.path = CONCAT('/article/', articles.slug)
            AND articles.author = authors.id
            GROUP BY authors.name
            ORDER BY views desc
            """
    results = execute_query(query)

    mostPopularAuthors = "The most popular authors of all time: \n"
    for author, viewNum in results:
        mostPopularAuthors += '\t"{}" - {} views\n'.format(author, viewNum)

    return mostPopularAuthors


def print_errors_over_one():
    """Print out the error report.

    This function prints out the days and that day's error percentage where
    more than 1% of logged access requests were errors.
    """
    query = """
            SELECT errorsperday.date,
                ROUND(100.0 * errorsperday.count/visitsperday.count, 2) AS errorpercentage
            FROM (
                SELECT DATE(time), COUNT(*)
                FROM log
                WHERE status LIKE '4%'
                GROUP BY DATE(time)
            ) AS errorsperday,
            (
                SELECT DATE(time), COUNT(*)
                FROM log
                GROUP BY DATE(time)
            )  AS visitsperday
            WHERE errorsperday.date = visitsperday.date
            AND visitsperday.count * 0.01 < errorsperday.count
            """
    results = execute_query(query)

    bigErrorDays = "Days where more than 1% of requests led to errors: \n"
    for date, errorRate in results:
        dateStr = date.strftime("%B %d, %Y")

        bigErrorDays += '\t{} - {}% errors\n'.format(dateStr, errorRate)

    return bigErrorDays


if __name__ == '__main__':

    # Open the output file and write to it the results of the queries
    outputFile = open('output.txt', 'a')
    outputFile.write(print_top_articles() + '\n' +
                     print_top_authors() + '\n' + print_errors_over_one())
    outputFile.close()
