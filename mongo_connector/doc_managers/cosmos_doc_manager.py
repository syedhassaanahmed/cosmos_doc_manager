import logging
import pydocumentdb.errors as cosmosdb_errors

from mongo_connector import errors
from mongo_connector.compat import u
from mongo_connector.constants import (DEFAULT_COMMIT_INTERVAL, DEFAULT_MAX_BULK)
from mongo_connector.doc_managers.cosmos_sql_handler import SQLHandler
from mongo_connector.doc_managers.cosmos_graph_handler import GraphHandler
from mongo_connector.doc_managers.doc_manager_base import DocManagerBase
from mongo_connector.doc_managers.formatters import DefaultDocumentFormatter
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

        self.unique_key = unique_key
        self._formatter = DefaultDocumentFormatter()

        if kwargs.get("apiType") == "Graph":
            self._api_handler = GraphHandler(url, **kwargs)
        else:
            self._api_handler = SQLHandler(url, **kwargs)

    def stop(self):
        self._api_handler.document_client = None

    def _cosmos_doc(self, doc, timestamp):
        doc_id = u(doc.pop(self.unique_key))
        doc = self._formatter.format_document(doc)
        doc["id"] = doc_id
        doc["_ts"] = timestamp
        return doc

    @wrap_exceptions
    def upsert(self, doc, namespace, timestamp):
        collection_link = self._api_handler.create_collection_link(namespace)
        doc = self._cosmos_doc(doc, timestamp)
        self._api_handler.upsert(doc, collection_link)

    @wrap_exceptions
    def bulk_upsert(self, docs, namespace, timestamp):
        collection_link = self._api_handler.create_collection_link(namespace)
        for doc in docs:
            doc = self._cosmos_doc(doc, timestamp)
            self._api_handler.upsert(doc, collection_link)

    @wrap_exceptions
    def update(self, document_id, update_spec, namespace, timestamp):
        pass

    @wrap_exceptions
    def remove(self, document_id, namespace, timestamp):
        pass

    @wrap_exceptions
    def search(self, start_ts, end_ts):
        return None

    def commit(self):
        pass

    @wrap_exceptions
    def get_last_doc(self):
        pass

    def handle_command(self, doc, namespace, timestamp):
        pass

    def insert_file(self, f, namespace, timestamp):
        pass
