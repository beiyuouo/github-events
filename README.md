# github-events

First, run the clear command manually by `cd src && python main.py clear`, or trigger the claer action in `GitHub Actions` or manually clear the database directory.

Note: Cause the GitHub API has limits of authentication, so you need to set the `AUTH_TOKEN` in `GitHub Secrets` to run the action.

Note: You'd better start caching your GitHub events as early as possible in the year, because there is a limit on the number of GitHub event query entries.

Note: If you are not using the time zone of `Asia/Shanghai`, you need to manually modify the `TIME_ZONE` in the action files.
