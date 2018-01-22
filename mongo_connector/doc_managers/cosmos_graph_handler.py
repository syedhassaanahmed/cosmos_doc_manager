import pydocumentdb.document_client as document_client

from mongo_connector.doc_managers.cosmos_repository import CosmosRepository


class GraphHandler(object):

    def __init__(self, url, **kwargs):
        database_id = kwargs["databaseId"]
        collection_id = kwargs["collectionId"]

        self.document_client = document_client.DocumentClient(url, {"masterKey": kwargs["masterKey"]})
        self.cosmos_repository = CosmosRepository(self.document_client)
        self.cosmos_repository.create_database(database_id)
        self.cosmos_repository.create_collection(database_id, collection_id)
        self.collection_link = "dbs/" + database_id + "/colls/" + collection_id

    def create_collection_link(self, namespace):
        return self.collection_link

    def upsert(self, doc, collection_link):
        self.document_client.UpsertDocument(collection_link, doc)

    def bulk_upsert(self, docs, collection_link):
        for doc in docs:
            self.document_client.UpsertDocument(collection_link, doc)
