import lucene
from lucene import *

from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import \
    FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import NIOFSDirectory , SimpleFSDirectory


import json
import sys
import os

if len(sys.argv) != 3:
    print("Usage: python3 indexer.py <data_dir> <index_dir>")
    exit(1)

data_dir = sys.argv[1]
index_dir = sys.argv[2]

if not os.path.isdir(data_dir):
    print("Error: data_dir is not a directory")
    exit(1)
if not os.path.isdir(index_dir):
    os.mkdir(index_dir)

data = []

try:
    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            print(f"Reading {filename}")
            with open(os.path.join(data_dir, filename), "r") as f:
                data += json.load(f)
            print("JSON is valid")
except:
    print("Error: Invalid JSON")
    exit(1)

lucene.initVM(vmargs=['-Djava.awt.headless=true'])

store = SimpleFSDirectory(Paths.get(index_dir))
analyzer = StandardAnalyzer()
config = IndexWriterConfig(analyzer)
config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
writer = IndexWriter(store, config)

#define a few field types here
#should it be indexed? should it be tokenized? should it be stored?
#stored means that the field will be returned in the search results as it is stored in the index
#tokenized means that the field will be split into tokens
#indexed means that the field will be searchable

#here are all the fields we will be using
"""
title: indexed, tokenized, and stored
author: indexed, not tokenized, and stored
id: indexed, not tokenized, and not stored
body: indexed, tokenized, and stored //not a good practice to store body in index, but we will do it for this project
subreddit: indexed, not tokenized, and not stored
"""
type0 = FieldType()
type0.setStored(True)
type0.setTokenized(True)
#stores document, term frequency, and position
type0.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

type1 = FieldType()
type1.setStored(True)
type1.setTokenized(False)
type1.setIndexOptions(IndexOptions.DOCS)

print("Indexing...")
for doc in data:
    document = Document()
    document.add(Field("title", doc["title"], type0))
    document.add(Field("id", doc["id"], type1))
    document.add(Field("body", doc["body"], type0))
    document.add(Field("subreddit", doc["subreddit"], type1))
    document.add(Field("author", doc["author"], type1))
    writer.addDocument(document)
writer.commit()
writer.close()
print("Done indexing!")