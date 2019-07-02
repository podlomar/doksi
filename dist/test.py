from doksi import parseFile, toHTML
from sys import argv

with open(argv[1], encoding='utf-8') as file:
  document = parseFile(file)
  print(document)
  print(toHTML(document))

