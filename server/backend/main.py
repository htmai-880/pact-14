"""
Backend module entrypoint.
"""
from os import getenv


# All the environments where sentry collect errors
sentry_envs = ["production"]


if __name__ == '__main__':
    if getenv("CI_ENVIRONMENT_NAME") in sentry_envs:
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration
        sentry_sdk.init(
            getenv("SENTRY_DSN"),
            integrations=[FlaskIntegration()],
            traces_sample_rate=1.0,
            environment=getenv("CI_ENVIRONMENT_NAME") + "/ai"
        )
    from app import main
    main()
else:
    print("[ERROR] Must be executed, not imported !")
