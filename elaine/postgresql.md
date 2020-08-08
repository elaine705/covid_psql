

## Due 20200718 (into postgresql) -- 
 1. Download and insert FIPS + truncate
 1. Load START_DATE into MIDNIGHT_DATA + truncate
    1. No need to create table
 1. analyze_death_by_fips
 1. Create View with MAD
 1. analyze_death_by_fips with MAD
 
 Run and commit in python then confirm in pgAdmin
 
### Extra
 1. for each date between START_DATE and TODAY, load MIDNIGHT_DATA
 1. remove truncate for midnight and pick the last date
 

## 20200717
 1. Loaded `Cluster by President Party`

### Postgresql -- psycopg2
 1. Connection
 ```python
import psycopg2

postgres_cred = dict(user=None, password=None, host=None, port=None, database=None)
connection = psycopg2.connect(**postgres_cred)
```
 1. Execute
```python
import psycopg2

connection = psycopg2.connect('postgres_cred')
cursor = connection.cursor()
cursor.execute('SQL_COMMAND')

# If you want to pull data
cursor.fetchall()
cursor.fetchone()
```
 1. Insert Many via `execute_values`
 ```python
from psycopg2.extras import execute_values

execute_values('cursor', 'SQL_COMMAND', ['data'], template='(%s, %s, ...)')
```
 1. Save Data!!
 ```python
import psycopg2

connection = psycopg2.connect('postgres_cred')
connection.commit()
```
 1. Rollback on ERROR
 ```python
import psycopg2

connection = psycopg2.connect('postgres_cred')
connection.rollback()
```
 1. Truncate (hack)
    - clears the table of all data
 ```sql
 TRUNCATE TABLE CLUSTER 
```
