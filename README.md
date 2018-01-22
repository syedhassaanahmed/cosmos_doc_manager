# Overview
Cosmos Doc Manager takes MongoDB documents and makes them available in Azure Cosmos DB following the format specified by [Mongo Connector](https://github.com/mongodb-labs/mongo-connector/wiki/Writing-Your-Own-DocManager). It piggybacks on [Mongo Replica Set Oplog](https://docs.mongodb.com/manual/core/replica-set-oplog/) and is intended for live one-way synchronization. Currently it supports Cosmos DB SQL and Graph API.

**This project is currently a work-in-progress!!!**

# Disclaimer
The software in this repository is provided AS IS, with no guarantees of any kind. This project is an independent effort and is **NOT associated with Microsoft**.

# Prerequisites
- You must have `Python 3` installed.
- If you need a MongoDB IDE, install [Studio3T](https://studio3t.com/download/).
- `Mongo Connector` requires a Mongo `Replica Set`. Install `Docker` if you'd like a local `Replica Set`.
- For local testing, install [Azure Cosmos DB Emulator](https://docs.microsoft.com/en-us/azure/cosmos-db/local-emulator). Cosmos DB Emulator currently only supports SQL API, however you'll still be able to see the internal `JSON` Document representation of other APIs.

## Local Mongo Replica Set
Run this to spin up a volume-mounted, single-node Mongo `Replica Set`;
```
docker run -it --rm -p 27017:27017 -v $HOME/mongodb:/data/db mongo --replSet myreplicaset
```

`Replica Set` needs to be initialized and re-configured because by default Mongo assigns container's inner address as `host`. Run this from Mongo Shell;
```javascript
rs.initiate(); 
conf = rs.conf();
conf.members[0].host = '127.0.0.1:27017';
rs.reconfig(conf, {force:true});
```

# Installation
- Install Mongo Connector `pip install mongo-connector`
- Clone this repo `git clone https://github.com/syedhassaanahmed/cosmos_doc_manager.git`
- Let Mongo Connector locate our Doc Manager `cd cosmos_doc_manager && export PYTHONPATH=.`
- Disable `HTTPS` Certificate warning `export PYTHONWARNINGS="ignore:Unverified HTTPS request"`

# Run locally
`mongo-connector -c config.json`

Mongo Connector's custom configuration is [specified here](https://github.com/mongodb-labs/mongo-connector/wiki/Configuration-Options). 

Below JSON is an example config file to sync data in Graph format with Cosmos DB Emulator. Possible values for `apiType` are `SQL` (default) and `Graph`. `Graph` requires specifying `databaseId` and `collectionId`.

```json
{
  "mainAddress": "localhost:27017",
  "docManagers": [
    {
      "docManager": "cosmos_doc_manager",
      "targetURL": "https://localhost:8081",
      "args": {
        "masterKey": "C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==",
        "apiType": "Graph",
        "databaseId": "graphdb",
        "collectionId": "graphcoll"
      }
    }
  ]
}
```
