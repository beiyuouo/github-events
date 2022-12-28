#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    :   src\report.py
# @Time    :   2022-08-21 13:55:09
# @Author  :   Bingjie Yan
# @Email   :   bj.yan.pa@qq.com
# @License :   Apache License 2.0

import os
from constants import *
import yaml
import pandas as pd
import datetime
import github
import re
import matplotlib.pyplot as plt


class ReportTemplate(object):
    def __init__(self):
        self.df = pd.DataFrame(
            {"date": [], "time": [], "activity": [], "repository": [], "link": []}
        )

        # self.df.columns = [
        #     "date",
        #     "time",
        #     "activity",
        #     "repository",
        #     "link",
        # ]

        self.avatar_url = None

        self.items = {}

    def read(self, year: int):
        data_path = os.path.join(DATABASE_PATH, f"{year}")

        print(f"Reading {data_path}...")

        files = os.listdir(data_path)
        files.sort()

        for file in files:
            file_path = os.path.join(data_path, file)

            print(f"Reading {file_path}...")

            with open(file_path, "r") as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                self.read_data(data)

    def read_data(self, data_items):
        for data_id in data_items.keys():

            data = data_items[data_id]
            print(f"Reading {data}...")

            date_ = data["created_at"].split("T")[0]
            time_ = data["created_at"].split("T")[1].split("Z")[0]
            activity_ = data["type"]
            repository_ = data["repo"]["name"]

            if activity_ == "PushEvent":
                link_ = f"https://github.com/{data['repo']['name']}/commit/{data['payload']['head']}"
            else:
                try:
                    link_ = (re.findall(r"https://*.+", yaml.dump(data["payload"]))[0],)
                except:
                    link_ = link_ = f"https://github.com/{repository_}"

            entry = {
                "date": date_,
                "time": time_,
                "activity": activity_,
                "repository": repository_,
                "link": link_,
            }

            self.df = pd.concat([self.df, pd.DataFrame(entry, index=[0])])

            if self.avatar_url is None:
                self.avatar_url = (
                    data["actor"]["avatar_url"]
                    if "avatar_url" in data["actor"]
                    else None
                )

    def generate(self, year: int = None):
        if year is None:
            year = datetime.datetime.now().year

        self.REPORT_PATH = os.path.join(REPORT_PATH, f"{year}")
        self.FIGURE_PATH = os.path.join(self.REPORT_PATH, f"figures")

        if not os.path.exists(self.REPORT_PATH):
            os.makedirs(self.REPORT_PATH)

        if not os.path.exists(self.FIGURE_PATH):
            os.makedirs(self.FIGURE_PATH)

        self.read(year)

        # analyze data
        self.df["date"] = pd.to_datetime(self.df["date"])
        # self.df["time"] = "xx:xx:xx"
        self.df["activity"] = self.df["activity"].astype("category")
        self.df["repository"] = self.df["repository"].astype("category")
        self.df["hour"] = self.df["time"].apply(lambda x: int(x.split(":")[0]))

        # count by event type
        self.items["count_by_event_type"] = self.df["activity"].value_counts().to_dict()
        # plot a pie chart
        plt.figure(figsize=(10, 5))
        plt.pie(
            self.df["activity"].value_counts(),
            labels=self.df["activity"].value_counts().index,
            autopct="%.2f%%",
        )
        plt.savefig(os.path.join(self.FIGURE_PATH, "count_by_event_type.png"))

        # count by repository
        self.items["count_by_repository"] = (
            self.df["repository"].value_counts().to_dict()
        )
        # plot a bar chart, only show top 20
        plt.figure(figsize=(10, 10))
        plt.bar(
            self.df["repository"].value_counts().index[:20],
            self.df["repository"].value_counts()[:20],
        )
        plt.xticks(rotation=90)
        # give more space to the x axis
        plt.subplots_adjust(bottom=0.5)
        plt.savefig(os.path.join(self.FIGURE_PATH, "count_by_repository.png"))

        # count by date
        self.items["count_by_date"] = self.df["date"].value_counts().to_dict()
        # plot a histogram
        plt.figure(figsize=(10, 5))
        plt.hist(self.df["date"], bins=30)
        plt.savefig(os.path.join(self.FIGURE_PATH, "count_by_date.png"))

        # count by time
        self.items["count_by_hour"] = self.df["hour"].value_counts().to_dict()
        # plot a bar
        plt.figure(figsize=(10, 5))
        plt.bar(self.df["hour"].value_counts().index, self.df["hour"].value_counts())
        plt.savefig(os.path.join(self.FIGURE_PATH, "count_by_hour.png"))

        print(self.items)

    def export(self, to_html: bool = False, to_csv: bool = False, to_md: bool = False):
        if to_csv:
            self.df.to_csv(os.path.join(self.REPORT_PATH, "report.csv"), index=False)
