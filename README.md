# covid_psql

## Sources
 - USA coronavirus data from CDC via [John Hopkins University](https://github.com/CSSEGISandData/COVID-19)
 - 2016 Presidential Election to determine each state's political party
 
## Process
 - Automatically loaded most recent data in Postgres


# Requirements

|Application|Version|Use Case|
|----------:|:------|:-----|
|[PyCharm Community](https://www.jetbrains.com/pycharm/)| 2020.1.4 | Editing `Python` and `SQL` source code |
|[Postgres](https://www.postgresql.org/download/) | 12.0 | Database for connection |
|[Grafana](https://grafana.com/grafana/download) | OpenSource 7.1.3 | Dashboard visualization | 
|SQLite| - | Intermediate database (before postgres) |

## PyCharm -- git
 - Create/Update files
 - Add to VCS(Version Control System) - git
 - Commit and Push (Ctrl-k)
    - Add commit message

## Postgres
 - Database Connections via pg Admin
![Postgres Connections](/img/02_postgres_database_connections.png)
 
## Grafana
 - Piped results to Grafana Dashboard for visualization 
![Corona Rates](/img/01_grafana_mortality.png)
