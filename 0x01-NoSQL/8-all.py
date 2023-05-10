#!/usr/bin/env python3
"""
8. List all documents in Python
"""


def list_all(mongo_collection):
    """
    A Python function that lists all documents in a collection
    """
    if mongo_collection is None:
        return []

    docs = mongo_collection.find()
    return [doc for doc in docs]
