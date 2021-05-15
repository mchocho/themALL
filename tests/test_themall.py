import unittest
from src.themall.themall import * 

item     = "power bank"
maxPages = 1

class test_themall(unittest.TestCase):
  def testbidorbuy(self):
    results = [];
    searchBidorbuy(results, item, maxPages)
    length  = len(results)
    self.assertNotEqual(length, 0)

  def testBuilders(self):
    results = []
    searchBuilders(results, item, maxPages)
    length  = len(results)
    self.assertNotEqual(length, 0)

  def testCashCrusaders(self):
    results = []
    searchCashcrusaders(results, item, maxPages)
    length  = len(results)
    self.assertNotEqual(length, 0)

  def testEvetech(self):
    search  = "desktop"
    results = []
    searchEvetech(results, search)
    length  = len(results)
    self.assertNotEqual(length, 0)

  def testGame(self):
    results = []
    searchGame(results, item, maxPages)
    length  = len(results)
    self.assertNotEqual(length, 0)

  def testHificorp(self):
    results = []
    searchHificorp(results, item, maxPages)
    length  = len(results)
    self.assertNotEqual(length, 0)

  def testIncredible(self):
    results = []
    searchIncredible(results, item, maxPages)
    length  = len(results)
    self.assertNotEqual(length, 0)

  def testLoot(self):
    results = []
    searchLoot(results, item, maxPages)
    length  = len(results)
    self.assertNotEqual(length, 0)

  def testMakro(self):
    results = []
    searchMakro(results, item, maxPages)
    length  = len(results)
    self.assertNotEqual(length, 0)

  def testPnp(self):
    results = []
    searchPnp(results, item, maxPages)
    length  = len(results)
    self.assertNotEqual(length, 0)

  def testRaru(self):
    results = []
    searchRaru(results, item, maxPages)
    length  = len(results)
    self.assertNotEqual(length, 0)

  def testTakealot(self):
    results = []
    searchTakealot(results, item, maxPages)
    length  = len(results)
    self.assertNotEqual(length, 0)

  def testTKZ(self):
    search  = "xbox"
    results = []
    searchTKZ(results, search, maxPages)
    length  = len(results)
    self.assertNotEqual(length, 0)

  def testWantitall(self):
    results = []
    searchWantitall(results, item, maxPages)
    length  = len(results)
    self.assertNotEqual(length, 0)

unittest.main(argv=['first-arg-is-ignored'], exit=False)
