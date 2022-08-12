#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    :   src\core.py
# @Time    :   2022-08-12 22:21:32
# @Author  :   Bingjie Yan
# @Email   :   bj.yan.pa@qq.com
# @License :   Apache License 2.0

import os
import pytz
from github import Github
import utils


class Core(object):
    AUTH_TOKEN = os.getenv("AUTH_TOKEN")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    TIME_ZONE = os.getenv("TIME_ZONE", "Asia/Shanghai")

    def __init__(self):
        self.g = Github(self.AUTH_TOKEN)
        print("Github token:", self.GITHUB_TOKEN)
        print("Auth token:", self.AUTH_TOKEN)
        print("Time zone:", self.TIME_ZONE)

    def run(self):
        utils.cache_events(self.g, pytz.timezone(self.TIME_ZONE))

    def update(self):
        readme_path = os.path.join(os.path.dirname(__file__), "..", "README.md")
        readme = utils.get_readme(readme_path)
        readme = utils.update_readme(readme)
        utils.write_readme(readme_path, readme)
        utils.write_summary(readme)
