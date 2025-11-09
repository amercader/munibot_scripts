#!/usr/bin/env python3
# encoding: utf-8
import os
import argparse
import json
import sqlite3
import configparser


FILE_TEMPLATE = """
window.MunibotPosts = {}
"""


def create(db_path, profile):

    db = sqlite3.connect(db_path)

    if profile == "es":
        code_field = "cod_ine"
        mastodon_field = "mastodon_es"
        table = "es"
    elif profile == "cat":
        code_field = "cod_ine"
        mastodon_field = "mastodon_cat"
        table = "es"
    elif profile == "fr":
        code_field = "insee"
        mastodon_field = "mastodon_fr"
        table = "fr"
    elif profile == "us":
        code_field = "GEOID"
        mastodon_field = "mastodon_us"
        table = "us"

    sql = f"""
        SELECT {code_field}, {mastodon_field}
        FROM {table}
        WHERE {mastodon_field} IS NOT NULL
        """
    posts_query = db.execute(sql)

    posts = {row[0]: row[1] for row in posts_query.fetchall()}

    if profile == "cat":
        count = db.execute(
            f"SELECT COUNT(*) FROM {table} WHERE codcomuni = '09'"
        ).fetchone()[0]
    else:
        count = db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

    out = {"mastodon": {"posts": posts, "total": count, "posted": len(posts.keys())}}

    return FILE_TEMPLATE.format(json.dumps(out))


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

    parser = argparse.ArgumentParser(description="Generate current posts JSON files")

    parser.add_argument("profile", help="Profile to export")
    parser.add_argument("-c", "--config", help="Munibot config file")

    args = parser.parse_args()

    db_path = db_path_from_config(args.config, args.profile)

    print(create(db_path, args.profile))
