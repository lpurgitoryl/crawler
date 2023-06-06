import lucene
from lucene import *

from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import \
    FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import NIOFSDirectory


import json
import sys
import os

if len(sys.argv) != 3:
    print("Usage: python3 indexer.py <data_dir> <index_dir>")
    exit(1)

data_dir = sys.argv[1]
index_dir = sys.argv[2]
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

lucene.initVM()
store = NIOFSDirectory.open(Paths.get(index_dir))
analyzer = StandardAnalyzer()
config = IndexWriterConfig(analyzer)
config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
writer = IndexWriter(store, config)
for doc in data:
    document = Document()
    metaType = FieldType()
    metaType.setStored(True)
    metaType.setTokenized(True)
    document.add(Field("title", doc["title"], metaType))
    metaType.setStored(True)
    metaType.setTokenized(False)
    document.add(Field("score", str(doc["score"]), metaType))
    metaType.setStored(True)
    document.add(Field("id", doc["id"], metaType))
    document.add(Field("url", doc["url"], metaType))
    document.add(Field("num_comments", str(doc["num_comments"]), metaType))
    metaType.setStored(True)
    metaType.setTokenized(True)
    # metaType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS_AND_OFFSETS)
    document.add(Field("body", doc["body"], metaType))
    metaType.setStored(True)
    metaType.setTokenized(False)
    document.add(Field("created", str(doc["created"]), metaType))
    # metaType.setStored(True)
    # document.add(Field("links", , metaType))
    # metaType.setStored(True)
    # metaType.setTokenized(True)
    # document.add(Field("comments", " ".join(doc["comments"]),  metaType))
    writer.addDocument(document)