import logging
import pydocumentdb.document_client as document_client
import pydocumentdb.errors as cosmosdb_errors

from mongo_connector import errors
from mongo_connector.compat import u
from mongo_connector.constants import (
    DEFAULT_COMMIT_INTERVAL, DEFAULT_MAX_BULK)
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
        self.url = url
        self.auto_commit_interval = auto_commit_interval
        self.unique_key = unique_key
        self.chunk_size = chunk_size
        self._formatter = DefaultDocumentFormatter()
        self.kwargs = kwargs

        # TODO: Move hardcoded emulator masterkey to config file
        self.document_client = document_client.DocumentClient(url, {"masterKey": "C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=="})
        self.metadata = {}

    def stop(self):
        self.auto_commit_interval = None
        self.document_client = None

    def _create_database(self, database_id):
        try:
            self.document_client.CreateDatabase({"id": database_id})

        except cosmosdb_errors.DocumentDBError as e:
            if e.status_code != 409:
                raise cosmosdb_errors.HTTPFailure(e.status_code)            

    def _create_collection(self, database_id, collection_id):
        try:
            self.document_client.CreateCollection("dbs/" + database_id, {"id": collection_id})

        except cosmosdb_errors.DocumentDBError as e:
            if e.status_code != 409:
                raise cosmosdb_errors.HTTPFailure(e.status_code)

    def _create_collection_link(self, namespace):
        database_id, collection_id =  namespace.split(".", 1)
        collection_link = "dbs/" + database_id + "/colls/" + collection_id

        if database_id not in self.metadata:
            self._create_database(database_id)
            self.metadata[database_id] = []

        if collection_id not in self.metadata[database_id]:
            self._create_collection(database_id, collection_id)
            self.metadata[database_id].append(collection_id)

        return collection_link

    def _upsert(self, doc, collection_link, timestamp):
        doc_id = u(doc.pop(self.unique_key))
        doc = self._formatter.format_document(doc)
        doc["id"] = doc_id
        doc["_ts"] = timestamp
        self.document_client.UpsertDocument(collection_link, doc)

    @wrap_exceptions
    def upsert(self, doc, namespace, timestamp):
        collection_link = self._create_collection_link(namespace)
        self._upsert(doc, collection_link, timestamp)

    @wrap_exceptions
    def bulk_upsert(self, docs, namespace, timestamp):
        collection_link = self._create_collection_link(namespace)
        for doc in docs:
            self._upsert(doc, collection_link, timestamp)

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