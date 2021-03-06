# covid_psql

## Sources
 - USA and US territories coronavirus data from CDC via [John Hopkins University](https://github.com/CSSEGISandData/COVID-19)
 - 2016 Presidential Election to determine each state's political party
 
## Process
 - Automatically loaded most recent data in Postgres


# Requirements

|Application|Version|Use Case|
|----------:|:------|:-----|
|[PyCharm Community](https://www.jetbrains.com/pycharm/)| 2020.1.4 | Editing `Python` and `SQL` source code |
|[Postgres](https://www.postgresql.org/download/) | 12.0 | Database for connection |
|[Grafana](https://grafana.com/grafana/download) | OpenSource 7.1.3 | Dashboard visualization | 
|[Tableau Public](https://public.tableau.com/en-us/s/)| 2020.3 | Alternate visualizations |
|SQLite| - | Intermediate database (before postgres) |

 - `elaine/secrets.json` contains database connection attributes
```json
{
	"postgresql": {
		"user": "USER_NAME",
		"password": "PASSWORD",
		"host": "IP_ADDRESS - localhost",
		"port": "PORT_of_Postgres - 5432",
		"database": "NAME_OF_DATABASE"
	}
}
```

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

## Tableau
 - Visualized each state's death count with a gradient heat map 
![Death Counts](/img/03_tableau_death_map.png)
![Death Grid](/img/04_tableau_tiled.png)
![Death Monthly Grid](/img/05_tableau_monthly_death.png)
![Death Cali Grid](/img/06_tableau_cali_monthly_death.png)
