# Overview
Cosmos Graph Doc Manager takes MongoDB documents and makes them available in an Azure Cosmos DB graph structure, following the format specified by [Mongo Connector](https://github.com/10gen-labs/mongo-connector). It piggybacks on [Mongo Replica Set Oplog](https://docs.mongodb.com/manual/core/replica-set-oplog/) and is intended for live one-way synchronization. 

**This project is currently a work-in-progress!!!**

# Disclaimer
The software in this repository is provided AS IS, with no guarantees of any kind. This project is an independent effort and is not associated with `Microsoft`.

# Prerequisites
- You must have `Python` installed in order to use this project. `Python 3` is recommended.
- If you need a MongoDB IDE, install [Studio3T](https://studio3t.com/download/).
- `Mongo Connector` requires a Mongo `Replica Set`. Install `Docker` if you'd like to do it locally.
- For local testing, install [Azure Cosmos DB Emulator](https://docs.microsoft.com/en-us/azure/cosmos-db/local-emulator). Cosmos DB Emulator currently doesn't support Graph API, however you'll still be able to see the internal `JSON` Document representation.

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
- Clone this repo `git clone https://github.com/syedhassaanahmed/cosmos_graph_doc_manager.git`
- Let Mongo Connector locate our Doc Manager `cd cosmos_graph_doc_manager && export PYTHONPATH=.`

# Run locally
`mongo-connector -m localhost:27017 -t https://localhost:8081 -d cosmos_graph_doc_manager`