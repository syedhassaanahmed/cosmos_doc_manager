import pydocumentdb.document_client as document_client

from mongo_connector.compat import u
from mongo_connector.doc_managers.cosmos_repository import CosmosRepository
from mongo_connector.doc_managers.formatters import DefaultDocumentFormatter


class SQLHandler(object):

    def __init__(self, url, unique_key, **kwargs):
        client = document_client.DocumentClient(url, {"masterKey": kwargs["masterKey"]})
        self._unique_key = unique_key
        self.cosmos_repository = CosmosRepository(client)
        self._offer_throughput = kwargs.get("offerThroughput", "400")
        self._formatter = DefaultDocumentFormatter()
        self._metadata = {}

    def _create_collection_link(self, namespace):
        database_id, collection_id = namespace.split(".", 1)
        collection_link = "dbs/" + database_id + "/colls/" + collection_id

        if database_id not in self._metadata:
            self.cosmos_repository.create_database(database_id)
            self._metadata[database_id] = []

        if collection_id not in self._metadata[database_id]:
            self.cosmos_repository.create_collection(database_id, collection_id, self._offer_throughput)
            self._metadata[database_id].append(collection_id)

        return collection_link

    def _cosmos_doc(self, doc, timestamp):
        doc_id = u(doc.pop(self._unique_key))
        doc = self._formatter.format_document(doc)
        doc["id"] = doc_id
        doc["_ts"] = timestamp
        return doc

    def upsert(self, doc, namespace, timestamp):
        collection_link = self._create_collection_link(namespace)
        doc = self._cosmos_doc(doc, timestamp)
        self.cosmos_repository.upsert_document(collection_link, doc)

    def bulk_upsert(self, docs, namespace, timestamp):
        collection_link = self._create_collection_link(namespace)
        for doc in docs:
            doc = self._cosmos_doc(doc, timestamp)
            self.cosmos_repository.upsert_document(collection_link, doc)