#!/usr/bin/env python3
# encoding: utf-8
import os
import argparse
import json
import sqlite3
import configparser


FILE_TEMPLATE = """
window.MunibotTweets = {}
"""


def create(db_path, profile):

    db = sqlite3.connect(db_path)

    if profile == "es":
        code_field = "cod_ine"
        tweet_field = "tweet_es"
        table = "munis_esp"
    elif profile == "cat":
        code_field = "cod_ine"
        tweet_field = "tweet_cat"
        table = "munis_esp"
    elif profile == "fr":
        code_field = "insee"
        tweet_field = "tweet_fr"
        table = "communes_fr"

    sql = f"""
        SELECT {code_field}, {tweet_field}
        FROM {table}
        WHERE {tweet_field} IS NOT NULL
        """
    data = db.execute(sql)

    return FILE_TEMPLATE.format(json.dumps({row[0]: row[1] for row in data.fetchall()}))


def db_path_from_config(path, profile):

    if not os.path.exists(path):
        raise ValueError(
            """
INI file not found. It must be a "munibot.ini" file in the current directory,
otherwise pass the location with the "--config" parameter""".strip()
        )

    cp = configparser.RawConfigParser()
    cp.read(path)
    return cp[f"profile:{profile}"]["db_path"]


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate current tweets JSON files")

    parser.add_argument("profile", help="Profile to export")
    parser.add_argument("-c", "--config", help="Munibot config file")

    args = parser.parse_args()

    db_path = db_path_from_config(args.config, args.profile)

    print(create(db_path, args.profile))
