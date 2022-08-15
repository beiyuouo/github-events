#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    :   utils.py
# @Time    :   2022-08-12 22:14:46
# @Author  :   Bingjie Yan
# @Email   :   bj.yan.pa@qq.com
# @License :   Apache License 2.0

import os
import base64
import sys
import re
import json
import yaml
from github import Github
import pytz

github_activity = {
    "PushEvent": "📌",
    "CreateEvent": "📁",
    "WatchEvent": "⭐",
    "ForkEvent": "🍴",
    "IssuesEvent": "📝",
    "PullRequestEvent": "📦",
    "ReleaseEvent": "🎉",
    "CommitCommentEvent": "💬",
    "DeleteEvent": "🗑",
    "DownloadEvent": "📁",
    "FollowEvent": "👤",
    "GistEvent": "📝",
    "IssueCommentEvent": "💬",
    "PublicEvent": "📝",
}

GITHUB_START_COMMENT = "<!-- START_SECTION:github -->"
GITHUB_END_COMMENT = "<!-- END_SECTION:github -->"


def get_activity_emoji(tag: str) -> str:
    """Get activity emoji"""
    return github_activity.get(tag, "")


def mkdir(path: str) -> None:
    """Make directory"""
    if not os.path.exists(path):
        os.mkdir(path)


def prepare_database():
    """Prepare database"""
    database_path = os.path.join(os.path.dirname(__file__), "..", "database")
    mkdir(database_path)


def get_user_events(g: Github):
    """Get user events"""
    import github

    privacy = ""

    print("username:", g.get_user().login)

    return github.PaginatedList.PaginatedList(
        github.Event.Event,
        g._Github__requester,
        f"/users/{g.get_user().login}/events{privacy}",
        None,
    )


def cache_events(g: Github, time_zone=pytz.timezone("Asia/Shanghai")) -> None:
    """Cache events"""
    prepare_database()
    print("username:", g.get_user().name)

    global entries
    entries = get_user_events(g)
    print(entries)
    for entry in entries:
        # print(entry)
        entry_time = entry.created_at.astimezone(time_zone)
        entry_time_str = entry_time.strftime("%Y-%m-%d %H:%M:%S")
        # print(entry_time_str)
        entry_date = entry_time.strftime("%Y-%m-%d")
        # print(entry_date)

        entry_year = entry_time.strftime("%Y")

        year_path = os.path.join(
            os.path.dirname(__file__), "..", "database", entry_year
        )
        mkdir(year_path)

        # print(entry.raw_data)
        # load raw data as json
        entry_data = entry.raw_data

        # json to yaml
        # print(entry_data)
        # print(type(entry_data))

        entry_path = os.path.join(year_path, f"{entry_date}.yaml")
        if os.path.exists(entry_path):
            with open(entry_path, "r") as f:
                entry_list = yaml.load(f, Loader=yaml.FullLoader)
                # check time
        else:
            entry_list = {}

        # if entry.id in entry_list:
        #     break

        entry_list[entry.id] = entry_data

        with open(entry_path, "w") as f:
            yaml.dump(entry_list, f)


def generate_github(
    username: str,
    limit: int,
    readme: str,
    time_format='"%Y-%m-%dT%H:%M:%SZ"',
    time_zone=pytz.timezone("Asia/Shanghai"),
) -> str:
    """Generate github"""
    print(limit, type(limit))
    arr = [
        {
            "title": item["title"],
            "url": item["link"],
            "tag": item["id"].split(":")[-1].split("/")[0],
            "published": item["published"].split("T")[0],
        }
        for item in entries[:limit]
    ]

    print(arr)

    content = "\n".join(
        [
            f"| {item['published']} | {' '.join(item['title'].split(' ')[1:-1])} "
            f"{get_activity_emoji(item['tag'])} [{item['title'].split(' ')[-1]}]({item['url']}) |"
            for item in arr
        ]
    )

    content = "| Date | Title |\n| :-: | :---: |\n" + content

    return generate_new_readme(
        GITHUB_START_COMMENT, GITHUB_END_COMMENT, content, readme
    )


def generate_new_readme(
    start_comment: str, end_comment: str, content: str, readme: str
) -> str:
    """Generate a new Readme.md"""
    pattern = f"{start_comment}[\\s\\S]+{end_comment}"
    repl = f"{start_comment}\n{content}\n{end_comment}"
    if re.search(pattern, readme) is None:
        print(
            f"can not find section in your readme, please check it, it should be {start_comment} and {end_comment}"
        )

    return re.sub(pattern, repl, readme)
