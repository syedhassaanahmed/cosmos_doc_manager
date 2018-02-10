import logging
import pydocumentdb.errors as cosmosdb_errors

from mongo_connector import errors
from mongo_connector.constants import (DEFAULT_COMMIT_INTERVAL, DEFAULT_MAX_BULK)
from mongo_connector.doc_managers.cosmos_sql_handler import SQLHandler
from mongo_connector.doc_managers.doc_manager_base import DocManagerBase
from mongo_connector.util import exception_wrapper

wrap_exceptions = exception_wrapper({
    cosmosdb_errors.DocumentDBError: errors.OperationFailed,
    cosmosdb_errors.HTTPFailure: errors.ConnectionFailed,
    cosmosdb_errors.JSONParseFailure: errors.OperationFailed,
    cosmosdb_errors.UnexpectedDataType: errors.OperationFailed})

LOG = logging.getLogger(__name__)


class DocManager(DocManagerBase):

    def __init__(self, url, auto_commit_interval=DEFAULT_COMMIT_INTERVAL,
                 unique_key="_id", chunk_size=DEFAULT_MAX_BULK, **kwargs):

        self._api_handler = SQLHandler(url, unique_key, **kwargs)

    def stop(self):
        self._api_handler.cosmos_repository.document_client = None

    @wrap_exceptions
    def upsert(self, doc, namespace, timestamp):
        self._api_handler.upsert(doc, namespace)

    @wrap_exceptions
    def bulk_upsert(self, docs, namespace, timestamp):
        self._api_handler.bulk_upsert(docs, namespace)

    def update(self, document_id, update_spec, namespace, timestamp):
        self._api_handler.update(document_id, update_spec, namespace)

    def remove(self, document_id, namespace, timestamp):
        self._api_handler.remove(document_id, namespace)

    def search(self, start_ts, end_ts):
        return None

    def commit(self):
        pass

    def get_last_doc(self):
        pass

    def handle_command(self, doc, namespace, timestamp):
        pass

    def insert_file(self, f, namespace, timestamp):
        pass
