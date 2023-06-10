import sys, os, lucene, json, pandas as pd
import datetime
import itertools

from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.search.similarities import BM25Similarity
from org.apache.lucene.index import IndexReader

if len(sys.argv) != 3:
    print("Usage: python3 searchEx.py <index_dir> <query>")
    exit(1)

index_dir = sys.argv[1]
query = sys.argv[2]

if not os.path.isdir(index_dir) or len(os.listdir(index_dir)) == 0:
    print("Error: index_dir is not a directory or is empty")
    exit(1)

results = []
# hitDocs = []

lucene.initVM()
dir = SimpleFSDirectory(Paths.get(index_dir))
searcher = IndexSearcher(DirectoryReader.open(dir))
analyzer = StandardAnalyzer()
searcher.setSimilarity(BM25Similarity())
queryByBody = QueryParser("body", analyzer).parse(query)
queryByTitle = QueryParser("title", analyzer).parse(query)
queryByAuthor = QueryParser("author", analyzer).parse(query)
queryBySubreddit = QueryParser("subreddit", analyzer).parse(query)
queryByID = QueryParser("id", analyzer).parse(query)
regularQuery = QueryParser("", analyzer).parse(query)
hitDocs = searcher.search(queryByBody, 10).scoreDocs #returns top 10 results
snippetLen = 50
for document in hitDocs:
    doc = searcher.doc(document.doc)
    snippet = doc.get("body").split()
    if len(snippet) > snippetLen:
        snippet = ' '.join(snippet[:snippetLen]) + "..."
    else:
        snippet = ' '.join(snippet)
    results.append([doc.get("author"), doc.get("id"), doc.get("subreddit"), doc.get("url"), doc.get("timestamp"), document.score, doc.get("title"), snippet])


tmp = searcher.search(queryByTitle, 10).scoreDocs
for document in tmp:
    doc = searcher.doc(document.doc)
    snippet = doc.get("body").split()
    if len(snippet) > snippetLen:
        snippet = ' '.join(snippet[:snippetLen]) + "..."
    else:
        snippet = ' '.join(snippet)
    results.append([doc.get("author"), doc.get("id"), doc.get("subreddit"), doc.get("url"), doc.get("timestamp"), document.score, doc.get("title"), snippet])

hitDocs += tmp
tmp = searcher.search(queryByAuthor, 10).scoreDocs
for document in tmp:
    doc = searcher.doc(document.doc)
    snippet = doc.get("body").split()
    if len(snippet) > snippetLen:
        snippet = ' '.join(snippet[:snippetLen]) + "..."
    else:
        snippet = ' '.join(snippet)
    results.append([doc.get("author"), doc.get("id"), doc.get("subreddit"), doc.get("url"), doc.get("timestamp"), document.score, doc.get("title"), snippet])


tmp = searcher.search(regularQuery, 10).scoreDocs
for document in tmp:
    doc = searcher.doc(document.doc)
    snippet = doc.get("body").split()
    if len(snippet) > snippetLen:
        snippet = ' '.join(snippet[:snippetLen]) + "..."
    else:
        snippet = ' '.join(snippet)
    results.append([doc.get("author"), doc.get("id"), doc.get("subreddit"), doc.get("url"), doc.get("timestamp"), document.score, doc.get("title"), snippet])

tmp = searcher.search(queryBySubreddit, 10).scoreDocs
for document in tmp:
    doc = searcher.doc(document.doc)
    snippet = doc.get("body").split()
    if len(snippet) > snippetLen:
        snippet = ' '.join(snippet[:snippetLen]) + "..."
    else:
        snippet = ' '.join(snippet)
    results.append([doc.get("author"), doc.get("id"), doc.get("subreddit"), doc.get("url"), doc.get("timestamp"), document.score, doc.get("title"), snippet])

tmp = searcher.search(queryByID, 10).scoreDocs
for document in tmp:
    doc = searcher.doc(document.doc)
    snippet = doc.get("body").split()
    if len(snippet) > snippetLen:
        snippet = ' '.join(snippet[:snippetLen]) + "..."
    else:
        snippet = ' '.join(snippet)
    results.append([doc.get("author"), doc.get("id"), doc.get("subreddit"), doc.get("url"), doc.get("timestamp"), document.score, doc.get("title"), snippet])

hashTable = {}
for i in results:
    if i[1] in hashTable:
        hashTable[i[1]][5] = hashTable[i[1]][5] + i[5]
    else:
        hashTable[i[1]] = i
for i in results:
    i[5] = round(i[5] * int(i[4]) / 1000000000, 3)
    i[4] = datetime.datetime.fromtimestamp(int(i[4])).strftime('%Y-%m-%d %H:%M:%S')
results = sorted(results, key=lambda x: x[5], reverse=True)
# print("%s total matching documents." % len(results))
    #TODO: decide whether we need score or not
    #TODO: search by different fields if we can't get enough results
    #TODO: Maybe search by different field and add the score together?
    #TODO: generate a snippet as well? maybe?
df = pd.DataFrame(results, columns=['author', 'id', 'subreddit', 'url', 'timestamp', 'score', 'title', 'snippet'])
print(df.to_json(orient='records', indent=4))
    
