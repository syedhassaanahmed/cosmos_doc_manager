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
        try:
            self.document_client.CreateCollection("dbs/" + database_id, {"id": collection_id})

        except errors.HTTPFailure as e:
            if e.status_code != 409:
                raise errors.HTTPFailure(e.status_code)
