import sys
from themall import *

results  = []
maxPages = 3
offset   = 0

if __name__ == "__main__":
  if len(sys.argv) == 1: 
    print("Please enter a search iterm.")
  else:
    print("Searching...")
    item = sys.argv[1]
    searchTakealot(results, item)
    searchBidorbuy(results, item, maxPages, offset)
    searchBuilders(results, item, maxPages, offset)
    searchCashcrusaders(results, item, maxPages, offset)
    searchEvetech(results, item)
    searchGame(results, item, maxPages, offset)
    searchHificorp(results, item, maxPages, offset)
    searchIncredible(results, item, maxPages, offset)
    searchLoot(results, item, maxPages, offset)
    searchMakro(results, item, maxPages, offset)
    searchPnp(results, item, maxPages, offset)
    searchRaru(results, item, maxPages, offset)
    searchTKZ(results, item, maxPages, offset)
    searchWantitall(results, item, maxPages, offset)
    printTable(results)
