import os


GITHUB_ACTIVITY = {
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


DATABASE_PATH = os.path.join(os.path.dirname(__file__), "..", "database")
REPORT_PATH = os.path.join(os.path.dirname(__file__), "..", "export")
FIGURE_PATH = os.path.join(REPORT_PATH, "figures")
