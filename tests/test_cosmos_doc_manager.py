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
    self.docman = DocManager('https://localhost:8081', auto_commit_interval=0)
    self.cosmos_repository = self.docman.cosmos_repository

  def setUp(self):
    self.cosmos_repository.delete_all()
    return

  def tearDown(self):
    self.cosmos_repository.delete_all()
    self.docman = DocManager('https://localhost:8081', auto_commit_interval=0)
    self.cosmos_repository = self.docman.cosmos_repository

  def test_update(self):
    """Test the update method. Simple cause, single parameter to update with set"""
    docc = doc_test
    update_spec = {"$set": {'room': 'Auditorium2'}}
    self.docman.update(doc_id, update_spec, 'test.talks', 1)
    expected_doc = {'_id': doc_id, 'session': {'title': '12 Years of Spring: An Open Source Journey', 'abstract': 'Spring emerged as a core open source project in early 2003 and evolved to a broad portfolio of open source projects up until 2015. This keynote reflects upon the journey so far, with a focus on the open source ecosystem that Spring lives within, including stories and anecdotes from the old days as well as from recent times. Not getting stuck in history, we’ll also look at the continuity of Spring’s philosophy and its immediate applicability to Java development challenges in 2015 and beyond.'}, 'room': 'Auditorium2', 'topics': ['keynote', 'spring'], 'speaker': {'twitter': 'https://twitter.com/springjuergen', 'name': 'Juergen Hoeller', 'picture': 'http://www.springio.net/wp-content/uploads/2014/11/juergen_hoeller-220x220.jpeg', 'bio': 'Juergen Hoeller is co-founder of the Spring Framework open source project and has been serving as the project lead and release manager for the core framework since 2003. Juergen is an experienced software architect and consultant with outstanding expertise in code organization, transaction management and enterprise messaging.'}, 'timeslot': 'Wed 29th, 09:30-10:30'}
    node = self.cosmos_repository.find("talks", "room", "Auditorium2")
    self.assertIsNot(node, None)
    self.tearDown()

  def test_update_new_property(self):
    """Test the update method. Set creating a new property"""
    docc = doc_without_id
    update_spec = {"$set": {'room': 'Auditorium2', 'level': 'intermediate'}}
    self.docman.update(doc_id, update_spec, 'test.talkss', 1)
    expected_doc = {'_id': doc_id, 'session': {'title': '12 Years of Spring: An Open Source Journey', 'abstract': 'Spring emerged as a core open source project in early 2003 and evolved to a broad portfolio of open source projects up until 2015. This keynote reflects upon the journey so far, with a focus on the open source ecosystem that Spring lives within, including stories and anecdotes from the old days as well as from recent times. Not getting stuck in history, we’ll also look at the continuity of Spring’s philosophy and its immediate applicability to Java development challenges in 2015 and beyond.'}, 'room': 'Auditorium2', 'level': 'intermediate', 'topics': ['keynote', 'spring'], 'speaker': {'twitter': 'https://twitter.com/springjuergen', 'name': 'Juergen Hoeller', 'picture': 'http://www.springio.net/wp-content/uploads/2014/11/juergen_hoeller-220x220.jpeg', 'bio': 'Juergen Hoeller is co-founder of the Spring Framework open source project and has been serving as the project lead and release manager for the core framework since 2003. Juergen is an experienced software architect and consultant with outstanding expertise in code organization, transaction management and enterprise messaging.'}, 'timeslot': 'Wed 29th, 09:30-10:30'}
    node = self.cosmos_repository.find("talks", "level", "intermediate")
    self.assertIsNot(node, None)
    self.tearDown()

  def test_update_empty(self):
    """Test the update method. No set or unset; all older properties must be erased"""
    docc = doc_without_id
    update_spec = {'level': 'intermediate'}
    self.docman.update(doc_id, update_spec, 'test.talkss', 1)
    node = self.cosmos_repository.find_one("talkss", "room", "Auditorium")
    self.assertEqual(node, None)
    self.tearDown()

  def test_update_unset_property(self):
    """Test the update method. Simple case test for unset"""
    docc = doc_without_id
    update_spec = {"$unset": {'timeslot': True}}
    self.docman.update(doc_id, update_spec, 'test.talksunset', 1)
    node = self.cosmos_repository.find_one("talksunset", "timeslot")
    self.assertIs(node, None)
    self.tearDown()

  def test_update_many_properties(self):
    """Test the update method. Many properties being sent at once"""
    docc = doc_without_id
    update_spec = {"$set": {'room': 'Auditorium2', 'timeslot': 'Wed 29th, 09:00-10:30'}}
    self.docman.update(doc_id, update_spec, 'test.talkss', 1)
    expected_doc = {'_id': doc_id, 'session': {'title': '12 Years of Spring: An Open Source Journey', 'abstract': 'Spring emerged as a core open source project in early 2003 and evolved to a broad portfolio of open source projects up until 2015. This keynote reflects upon the journey so far, with a focus on the open source ecosystem that Spring lives within, including stories and anecdotes from the old days as well as from recent times. Not getting stuck in history, we’ll also look at the continuity of Spring’s philosophy and its immediate applicability to Java development challenges in 2015 and beyond.'}, 'room': 'Auditorium2', 'level': 'intermediate', 'topics': ['keynote', 'spring'], 'speaker': {'twitter': 'https://twitter.com/springjuergen', 'name': 'Juergen Hoeller', 'picture': 'http://www.springio.net/wp-content/uploads/2014/11/juergen_hoeller-220x220.jpeg', 'bio': 'Juergen Hoeller is co-founder of the Spring Framework open source project and has been serving as the project lead and release manager for the core framework since 2003. Juergen is an experienced software architect and consultant with outstanding expertise in code organization, transaction management and enterprise messaging.'}, 'timeslot': 'Wed 29th, 09:00-10:30'}
    node = self.cosmos_repository.find("talks", "room", "Auditorium2")
    self.assertIsNot(node, None)
    self.tearDown()

  def test_update_nested_properties(self):
    """Test the update method for nested properties. A new node and a new relationship must be created."""
    docc = double_nested_doc
    update_spec = {"$set": {'details': {'model': '14Q3', 'make': 'xyz'}, 'level': 'intermediate'}}
    self.docman.update(doc_id, update_spec, 'test.talksnesteds', 1)
    node = self.cosmos_repository.find("details", "model", "14Q3")
    self.assertIsNot(node, None)
    labels = self.cosmos_repository.node_labels
    self.assertIn("details", labels)
    self.tearDown()

  def test_bulk_upsert(self):
    self.docman.bulk_upsert([], 'test.talksbulk', 1)
    docs = ({"_id": i} for i in range(1000))
    self.docman.bulk_upsert(docs, 'test.talksbulk', 1)
    result = self.cosmos_repository.node_labels
    self.assertIn("talksbulk", result)
    nodes = self.cosmos_repository.find("talksbulk")
    total_nodes = 0
    for i, node in enumerate(nodes):
        self.assertEqual(node['_id'], str(i))
        total_nodes += 1
    self.assertEqual(total_nodes, 1000)
    self.tearDown()

  def test_upsert(self):
    docc = doc_test
    self.docman.upsert(docc, 'test.talksone', 1)
    result = self.cosmos_repository.node_labels
    self.assertIn("talksone", result)
    self.assertIn("speaker", result)
    self.assertIn("session", result)
    self.assertIn("Document", result)
    self.assertEqual(self.cosmos_repository.size, 2)
    root = self.cosmos_repository.find_one("talksone")['timeslot']
    self.assertEqual("Wed 29th, 09:30-10:30", root)
    inner = self.cosmos_repository.find_one("speaker")['name']
    self.assertEqual("Juergen Hoeller", inner)
    inner = self.cosmos_repository.find_one("session")['title']
    self.assertEqual("12 Years of Spring: An Open Source Journey", inner)
    ts = self.cosmos_repository.find_one("talksone")['_ts']
    self.assertIsNot(ts, None)
    self.tearDown()

  def test_upsert_inner_nested(self):
    docc = doc_test_double_nested
    self.docman.upsert(docc, 'test.innernestedtalks', 1)
    result = self.cosmos_repository.node_labels
    self.assertIn("session", result)
    self.assertIn("conference", result)
    self.assertIn("Document", result)
    node = self.cosmos_repository.find("conference", "city", "London")
    self.assertIsNot(node, None)
    self.assertEqual(self.cosmos_repository.size, 3)
    self.tearDown()

  def test_upsert_with_explicit_id(self):
    docc = doc_rel
    self.docman.upsert(docc, 'test.places', 1)
    docc2 = doc_explicit_rel_id
    self.docman.upsert(docc2, 'test.people', 1)
    result = self.cosmos_repository.node_labels
    self.assertIn("places", result)
    self.assertIn("people", result)
    self.assertIn("Document", result)
    self.assertEqual(self.cosmos_repository.size, 1)
    self.tearDown()

  def test_upsert_with_special_chracter_type_on_property(self):
    docc = {'_id': "123a456b", 'session-main': {'main-title': 'simple title'}, 'room': "Auditorium" }
    self.docman.upsert(docc, 'test.specialcharproperty', 1)
    result = self.cosmos_repository.node_labels
    self.assertIn("Document", result)
    self.assertIn("session-main", result)
    self.assertEqual(self.cosmos_repository.size, 1)
    node = self.cosmos_repository.find("session-main", "main-title", "simple title")
    for n in node:
      self.assertIsNot(n["main-title"], "simple title")
    self.tearDown()

  def test_upsert_doc_with_objectid(self):
    '''
    Test that ObjectId properties in a document can be parsed and handled properly
    '''
    test_doc = {'_id': 'mydocid', 'name': 'Bob'}
    test_doc['some_objectid'] = ObjectId()
    print(test_doc)
    self.docman.upsert(test_doc, 'test.docwithobjectid', 1)
    #self.assertGreaterEqual(self.graph.size, 1)
    nodes = self.cosmos_repository.find('docwithobjectid')
    self.assertIsNotNone(nodes)
    for n in nodes:
      print(n)
      self.assertIn('some_objectid', n.properties.keys())
    self.tearDown()

  def test_remove(self):
    docc = simple_doc
    id = docc['_id']
    self.docman.upsert(docc, 'test.samples', 1)
    self.docman.remove(id, 'test.samples', 1)
    self.assertEqual(self.cosmos_repository.size, 0)
    self.tearDown()

if __name__ == '__main__':
  unittest.main()