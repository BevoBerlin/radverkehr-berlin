import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def verbinde():
    return mysql.connector.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"),
                                   password=os.getenv("DB_PASSWORD"), database=os.getenv("DB_NAME"))


def leere(con):
    cur = con.cursor()
    for t in ["zaehlung", "zaehlstelle", "wetter", "feiertag"]:
        cur.execute(f"DELETE FROM {t}")
    con.commit()


def lade(con, tabelle, df):
    sql = f"INSERT INTO {tabelle} ({','.join(df.columns)}) VALUES ({','.join(['%s'] * len(df.columns))})"
    zeilen = df.astype(object).where(df.notna(), None).values.tolist()
    cur = con.cursor()
    for i in range(0, len(zeilen), 50000):
        cur.executemany(sql, zeilen[i:i + 50000])
    con.commit()