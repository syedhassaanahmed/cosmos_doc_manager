#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""Unit tests - Cosmos DB DocManager."""
import sys
sys.path[0:0] = [""]

from bson.objectid import ObjectId
from tests import unittest, doc_test_double_nested, double_nested_doc, doc_without_id, doc_test, doc_id, doc_array_test, simple_doc, doc_rel, doc_explicit_rel_id
from mongo_connector.doc_managers.cosmos_doc_manager import DocManager


class CosmosTestCase(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    docman_args = {"masterKey": "C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=="}
    self.docman = DocManager('https://localhost:8081', auto_commit_interval=0, kwargs=docman_args)
    self.cosmos_repository = self.docman.cosmos_repository

  def setUp(self):
    self.cosmos_repository.delete_all()

  def tearDown(self):
    self.cosmos_repository.delete_all()

  def test_upsert(self):

    actual_doc = self.cosmos_repository.get_document("talks", "room", "Auditorium2")
    #self.assertIsNot(node, None)
    self.tearDown()

if __name__ == '__main__':
  unittest.main()