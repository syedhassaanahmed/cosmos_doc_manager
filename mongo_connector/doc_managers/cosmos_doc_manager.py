import logging
import pydocumentdb.errors as cosmosdberrors

from mongo_connector import errors
from mongo_connector.constants import (
    DEFAULT_COMMIT_INTERVAL, DEFAULT_MAX_BULK)
from mongo_connector.doc_managers.doc_manager_base import DocManagerBase
from mongo_connector.doc_managers.formatters import DefaultDocumentFormatter
from mongo_connector.util import exception_wrapper

wrap_exceptions = exception_wrapper({
    cosmosdberrors.DocumentDBError: errors.OperationFailed,
    cosmosdberrors.HTTPFailure: errors.ConnectionFailed,
    cosmosdberrors.JSONParseFailure: errors.OperationFailed,
    cosmosdberrors.UnexpectedDataType: errors.OperationFailed})

LOG = logging.getLogger(__name__)

class DocManager(DocManagerBase):

    def __init__(self, url, auto_commit_interval=DEFAULT_COMMIT_INTERVAL,
                 unique_key='_id', chunk_size=DEFAULT_MAX_BULK, **kwargs):

        self.url = url
        self.auto_commit_interval = auto_commit_interval
        self.unique_key = unique_key
        self.chunk_size = chunk_size
        self._formatter = DefaultDocumentFormatter()
        self.kwargs = kwargs

    def stop(self):
        self.auto_commit_interval = None
