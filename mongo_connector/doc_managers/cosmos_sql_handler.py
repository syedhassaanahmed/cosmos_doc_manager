import pydocumentdb.document_client as document_client

from mongo_connector.doc_managers.cosmos_repository import CosmosRepository


class SQLHandler(object):

    def __init__(self, url, **kwargs):
        self.document_client = document_client.DocumentClient(url, {"masterKey": kwargs["masterKey"]})
        self.cosmos_repository = CosmosRepository(self.document_client)
        self.metadata = {}

    def create_collection_link(self, namespace):
        database_id, collection_id = namespace.split(".", 1)
        collection_link = "dbs/" + database_id + "/colls/" + collection_id

        if database_id not in self.metadata:
            self.cosmos_repository.create_database(database_id)
            self.metadata[database_id] = []

        if collection_id not in self.metadata[database_id]:
            self.cosmos_repository.create_collection(database_id, collection_id)
            self.metadata[database_id].append(collection_id)

        return collection_link

    def upsert(self, doc, collection_link):
        self.document_client.UpsertDocument(collection_link, doc)

    def bulk_upsert(self, docs, collection_link):
        for doc in docs:
            self.document_client.UpsertDocument(collection_link, doc)
