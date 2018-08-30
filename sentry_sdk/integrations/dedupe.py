from sentry_sdk.api import configure_scope
from sentry_sdk.utils import ContextVar

from . import Integration


last_seen = ContextVar("last-seen")


class DedupeIntegration(Integration):
    identifier = "dedupe"

    def install(self):
        with configure_scope() as scope:

            @scope.add_error_processor
            def processor(event, exc_info):
                exc = exc_info[1]
                if last_seen.get(None) is exc:
                    return
                seen = False
                last_seen.set(exc)
                return event
