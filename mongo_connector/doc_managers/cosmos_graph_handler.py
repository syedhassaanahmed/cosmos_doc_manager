import pydocumentdb.document_client as document_client

from mongo_connector.compat import u
from mongo_connector.doc_managers.cosmos_repository import CosmosRepository
from mongo_connector.doc_managers.formatters import DefaultDocumentFormatter


class GraphHandler(object):

    def __init__(self, url, unique_key, **kwargs):
        database_id = kwargs["databaseId"]
        collection_id = kwargs["collectionId"]
        offer_throughput = kwargs.get("offerThroughput", "400")

        client = document_client.DocumentClient(url, {"masterKey": kwargs["masterKey"]})
        self.cosmos_repository = CosmosRepository(client)
        self.cosmos_repository.create_database(database_id)
        self.cosmos_repository.create_collection(database_id, collection_id, offer_throughput)

        self._collection_link = "dbs/" + database_id + "/colls/" + collection_id
        self._unique_key = unique_key
        self._formatter = DefaultDocumentFormatter()

    @staticmethod
    def _doc_type(namespace):
        index, doc_type = namespace.split('.', 1)[0]
        return index.lower(), doc_type

    def upsert(self, doc, namespace, timestamp):
        index, doc_type = self._index_and_doctype(namespace)
        vertices_and_edges = self._build_vertices_and_edges(doc, doc_type, timestamp)
        self.cosmos_repository.upsert_documents(self._collection_link, vertices_and_edges)

    def bulk_upsert(self, docs, namespace, timestamp):
        index, doc_type = self._index_and_doctype(namespace)
        for doc in docs:
            vertices_and_edges = self._build_vertices_and_edges(doc, doc_type, timestamp)
            self.cosmos_repository.upsert_documents(self._collection_link, vertices_and_edges)

    def _build_vertices_and_edges(self, doc, doc_type, timestamp):
        doc_id = u(doc.pop(self._unique_key))
        root_doc = {"id": doc_id, "_ts": timestamp}
        vertices_and_edges = [root_doc]

        for key in doc.keys():
            pass

        return vertices_and_edges

