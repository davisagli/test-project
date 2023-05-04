"""Init and utils."""
from zope.i18nmessageid import MessageFactory

import logging


_ = MessageFactory("test_project")

logger = logging.getLogger("test_project")
