# Overview
[![PyPI version](https://badge.fury.io/py/cosmos-doc-manager.svg)](https://badge.fury.io/py/cosmos-doc-manager)

Cosmos Doc Manager takes MongoDB documents and makes them available in Azure Cosmos DB following the format specified by [Mongo Connector](https://github.com/mongodb-labs/mongo-connector/wiki/Writing-Your-Own-DocManager). It piggybacks on [Mongo Replica Set Oplog](https://docs.mongodb.com/manual/core/replica-set-oplog/) and is intended for near-realtime synchronizations. Currently it works for Cosmos DB SQL API. Partial MongoDB updates are handled with Stored Procedures and support the [following operations](https://github.com/syedhassaanahmed/cosmos_doc_manager/blob/10f19dace233a7e44c53a9eea3c44dcbd050f125/mongo_connector/doc_managers/cosmos_partial_update.py#L11).

# Disclaimer
The software in this repository is provided AS IS, with no guarantees of any kind. This project is an independent effort and is **NOT associated with Microsoft**. Having said that, Pull Requests are most welcome.

# Prerequisites
- You must have Python installed. Python 3 is recommended.
- `Mongo Connector` operates on a Mongo `Replica Set`. `Docker` is the easiest way to spin it up locally.
- For local testing, install [Azure Cosmos DB Emulator](https://docs.microsoft.com/en-us/azure/cosmos-db/local-emulator). Cosmos DB Emulator currently only supports SQL API.

## Local Mongo Replica Set
Run this to spin up a volume-mounted, single-node Mongo `Replica Set`;
```
docker run -it --rm -p 27017:27017 -v $HOME/mongodb:/data mongo --replSet myreplicaset
```

`Replica Set` needs to be initialized and re-configured because by default Mongo assigns container's inner address as `host`. Run this from Mongo Shell;
```javascript
rs.initiate(); 
conf = rs.conf();
conf.members[0].host = '127.0.0.1:27017';
rs.reconfig(conf, {force:true});
```

# Installation
- Install Mongo Connector `sudo pip install mongo-connector`
- Clone this repo `git clone https://github.com/syedhassaanahmed/cosmos_doc_manager.git`
- Let Mongo Connector locate our Doc Manager `cd cosmos_doc_manager && export PYTHONPATH=.`
- Disable `HTTPS` Certificate warning `export PYTHONWARNINGS="ignore:Unverified HTTPS request"`

# Run locally
`mongo-connector -c config.json`

`Mongo Connector`'s custom configuration is [specified here](https://github.com/mongodb-labs/mongo-connector/wiki/Configuration-Options). 

Below JSON is an example config file to sync data in Graph format with Cosmos DB Emulator.

```json
{
  "mainAddress": "localhost:27017",
  "docManagers": [
    {
      "docManager": "cosmos_doc_manager",
      "targetURL": "https://localhost:8081",
      "bulkSize": 100,
      "args": {
        "masterKey": "C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=="
      }
    }
  ]
}
```

# Future improvements
- Support for partitioned collections
- Support for other Cosmos DB APIs