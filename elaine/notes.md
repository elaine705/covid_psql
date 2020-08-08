## Connection
Create an in memory database
```python
import sqlite3
conn = sqlite3.connect(':memory:')
cur = conn.cursor()

```

### `Stocks` Table
 - DATE:- INTEGER
    - (as YYYYMMDD)
 - TICKER:- TEXT
    - (name of stock)
 - PRICE:- REAL
    - (price end of day)
```sql
CREATE TABLE Stocks (
date INTEGER,
ticker TEXT,
price REAL)
```
    
## INSERT data
 - (20200530, AAPL, 317.94)
 - (20200530, MSFT, 183.25)
 
```sql
INSERT INTO Stocks (date,ticker,price)
VALUES (20200530, "AAPL", 317.94)
```

## SELECT data
```sql
SELECT * FROM Stocks
```

## Filtering
```sql
SELECT * FROM Stocks
WHERE Price > 200
```

## AGGREGATE COMMAND - MAX
 - max price with name 
```sql
SELECT Ticker, MAX(Price)
FROM Stocks
```


## GROUPING
 - group by day - get max for each day
 Ticker, max(price)

```sql
SELECT Ticker, MAX(Price)
FROM Stocks
Group BY Date
```

## INSERT Many values
 - (20200529, AAPL, 310)
 - (20200529, MSFT, 180)
```sql
INSERT INTO Stocks(date,ticker,price)
VALUES (20200529, "AAPL", 310), (20200529, "MSFT", 180)

```

## For each ticker, find abs(max-min)
```sql
SELECT Ticker, ABS(MAX(Price)-MIN(Price))
FROM Stocks
GROUP BY Ticker
```

## Create view for above
```sql
CREATE VIEW stock_inc as 
SELECT Ticker, ABS(MAX(Price)-MIN(Price))
FROM Stocks
GROUP BY Ticker
```

## MAX by n
 - for each ticker, find day at max(PRICE)
```sql
SELECT Date, MAX(Price)
FROM Stocks
GROUP BY Ticker
```

 - view for percent increase -- LAG
 	