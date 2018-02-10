import mongo_connector.doc_managers.cosmos_bulk_upsert as bulk_upsert
import mongo_connector.doc_managers.cosmos_partial_update as partial_update
import pydocumentdb.errors as errors


class CosmosRepository(object):

    def __init__(self, document_client):
        self.document_client = document_client
    
    def create_database(self, database_id):
        try:
            self.document_client.CreateDatabase({"id": database_id})
        except errors.HTTPFailure as e:
            if e.status_code != 409:
                raise errors.HTTPFailure(e.status_code)

    def create_collection(self, database_id, collection_id):
        database_link = "dbs/" + database_id
        collection_link = database_link + "/colls/" + collection_id
        try:
            self.document_client.CreateCollection(database_link, {"id": collection_id})
            self.document_client.CreateStoredProcedure(collection_link,
                                                       {"id": partial_update.SPROC_NAME, "body": partial_update.SPROC_BODY})
            self.document_client.CreateStoredProcedure(collection_link,
                                                       {"id": bulk_upsert.SPROC_NAME, "body": bulk_upsert.SPROC_BODY})
        except errors.HTTPFailure as e:
            if e.status_code != 409:
                raise errors.HTTPFailure(e.status_code)

    def upsert_document(self, collection_link, doc):
        self.document_client.UpsertDocument(collection_link, doc)

    def upsert_documents(self, collection_link, docs):
        sproc_link = collection_link + "/sprocs/" + bulk_upsert.SPROC_NAME
        self.document_client.ExecuteStoredProcedure(sproc_link, { "docs": docs })