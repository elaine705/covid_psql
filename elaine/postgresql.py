import csv
import json
import logging
from datetime import date as dt, timedelta

import psycopg2
import psycopg2.extras
import requests

LOGGER = logging.getLogger(__name__)


class Corona(object):
    """ USA Daily Corona Report """

    BASE_URL = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/'

    # midnight data
    DESIRED_COLUMNS = ('Province_State', 'Confirmed', 'Deaths', 'Mortality_Rate', 'FIPS')
    SOURCE = fr'{BASE_URL}csse_covid_19_daily_reports_us/{{date:%m-%d-%Y}}.csv'
    START_DATE = dt(2020, 4, 12)

    # UIDME data
    FIPS_DESIRED_COLUMNS = ('FIPS', 'UID', 'Country_Region', 'Lat', 'Long_', 'Population')
    SOURCE_FIPS = fr'{BASE_URL}UID_ISO_FIPS_LookUp_Table.csv'

    # Clustering results
    CLUSTER_COLUMNS = dict(
        PRESIDENTIAL_2016=('State', 'electoralDem', 'electoralRep'),
    )

    CLUSTER_SOURCE = dict(
        PRESIDENTIAL_2016='presidential2016results.csv',
    )

    def __init__(self, date: dt = START_DATE, *, init_meta: bool = False):
        """
        Creates and parses US Daily Reports
        :param date: CURRENT_DATE
        :param init_meta: initialize FIPS & state party preferences
        """

        with open('secrets.json') as f:
            self.db = psycopg2.connect(**json.load(f)['postgresql'])

        if init_meta:
            self.initialize_cluster_presidential(self._fetch_presidential())
            self.initialize_db_fips(self._fetch_fips())

        self.date: dt = self.last_date()
        while self.date < date:
            self.date = self.date + timedelta(days=1)
            self.insert_into_db(self._fetch_midnight())
        # self.analyze_death_by_fips()

    @staticmethod
    def get_desired_index(header: list, desired_columns: tuple) -> list:
        mapping = {column: position for position, column in enumerate(header)}
        return [mapping[column] for column in desired_columns]

    # <editor-fold desc="cluster_presidential">
    def _fetch_presidential(self) -> list:
        with open(Corona.CLUSTER_SOURCE['PRESIDENTIAL_2016']) as f:
            csv_presidential = csv.reader(f)
            header: list = next(csv_presidential)

            desired_index = self.get_desired_index(header, Corona.CLUSTER_COLUMNS['PRESIDENTIAL_2016'])
            data = []
            for line in csv_presidential:
                if line:
                    state = line[desired_index[0]]
                    dem = int(line[desired_index[1]])
                    rep = int(line[desired_index[2]])
                    data.append([state, 'D' if dem > rep else 'R'])

        return data

    def initialize_cluster_presidential(self, data: list):
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS CLUSTER( 
                STATE VARCHAR(20) PRIMARY KEY,
                PARTY VARCHAR(1)
            )
        """)

        cursor.execute("""TRUNCATE TABLE CLUSTER""")
        psycopg2.extras.execute_values(cursor, """
            INSERT INTO CLUSTER(STATE, PARTY)
            VALUES %s
        """, data, template='(%s, %s)')

        self.db.commit()

    # </editor-fold>

    # <editor-fold desc="FIPS">
    def _fetch_fips(self) -> list:
        url: str = Corona.SOURCE_FIPS
        data: list = requests.get(url).content.decode().split('\n')
        csv_data = csv.reader(data)

        self.desired_index = Corona.get_desired_index(next(csv_data), Corona.FIPS_DESIRED_COLUMNS)
        res = []
        for row in csv_data:
            if row and row[self.desired_index[0]] and row[self.desired_index[-1]]:
                res.append([row[index] for index in self.desired_index])
        return res

    def initialize_db_fips(self, data: list):
        cur = self.db.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS "UIDME"( 
                "UID" integer NOT NULL,
                "FIPS" integer,
                "Country_Region" character varying(25) COLLATE pg_catalog."default" NOT NULL,
                "Lat" double precision NOT NULL,
                "Long_" double precision NOT NULL,
                "Population" integer NOT NULL,
                CONSTRAINT "UIDME_pkey" PRIMARY KEY ("UID"),
                CONSTRAINT "uniFIPS" UNIQUE ("FIPS")
            )7
        """)

        cur.execute("""TRUNCATE TABLE "UIDME" CASCADE""")
        psycopg2.extras.execute_values(cur, """
            INSERT INTO "UIDME"("FIPS", "UID", "Country_Region", "Lat", "Long_", "Population")
            VALUES %s
        """, data, template='(%s, %s, %s, %s, %s, %s)')

        self.db.commit()

    # </editor-fold>p

    # <editor-fold desc="MIDNIGHT_DATA">
    def _fetch_midnight(self) -> list:
        url: str = Corona.SOURCE.format(date=self.date)
        data: list = requests.get(url).content.decode().split('\n')
        csv_data = csv.reader(data)

        self.desired_index = Corona.get_desired_index(next(csv_data), Corona.DESIRED_COLUMNS)
        res = []
        for row in csv_data:
            if row and float(row[self.desired_index[-3]] or '0') and int(row[self.desired_index[-1]] or '0') < 9000:
                res.append([row[index] or '0' for index in self.desired_index])
        return res

    def insert_into_db(self, data: list):
        cursor = self.db.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS public."MIDNIGHT_DATA" (
            "State" character varying(40) COLLATE pg_catalog."default" NOT NULL,
            "Date" date NOT NULL,
            "Confirmed" integer NOT NULL,
            "Deaths" integer NOT NULL,
            "Mortality_Rate" double precision NOT NULL,
            "FIPS" integer NOT NULL,
            CONSTRAINT "MidnightPrimKey" PRIMARY KEY ("State", "Date"),
            CONSTRAINT "foreignFIPS" FOREIGN KEY ("FIPS")
                REFERENCES public."UIDME" ("FIPS") MATCH SIMPLE
                ON UPDATE RESTRICT
                ON DELETE RESTRICT,
            CONSTRAINT "NonNegDeath" CHECK ("Deaths" >= 0),
            CONSTRAINT "NonNegConfirmed" CHECK ("Confirmed" >= 0),
            CONSTRAINT "NonNegMortality" CHECK ("Mortality_Rate" >= 0::double precision)
        )
        """)

        psycopg2.extras.execute_values(cursor, """
            INSERT INTO "MIDNIGHT_DATA"("State", "Date", "Confirmed", "Deaths", "Mortality_Rate", "FIPS")
            VALUES %s
        """, data, template=f"(%s, '{self.date}', %s, %s, %s, %s)")
        self.db.commit()

    def last_date(self) -> dt:
        cursor = self.db.cursor()
        cursor.execute(""" SELECT  MAX("Date") FROM public."MIDNIGHT_DATA" """)
        date = cursor.fetchone() or [Corona.START_DATE]
        return date[0]

    # </editor-fold>


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s]-%(message)s', datefmt='%H:%M:%S')
    corona = Corona(dt.today() - timedelta(days=1))
    corona.db.close()
