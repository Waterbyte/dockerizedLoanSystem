from pymongo import MongoClient as mc
from flask import g



def get_db_client():
    if 'dbcl' not in g:
        g.dbcl = mc('mongodb://localhost:27017/')
    return g.dbcl


def get_db():
    return get_db_client()['loans_db']

def get_collection(coll_name = None):
    if coll_name is not None:
        return get_db()[coll_name]
    else:
        return None


def close_dbcl(e=None):
    dbcl = g.pop('dbcl', None)
    if dbcl is not None:
        dbcl.close()


def init_app(app):
    app.teardown_appcontext(close_dbcl)
	
def count_doc(coll, argsDict):
    cln = get_collection(coll)
    return cln.count_documents(argsDict)


def insert_one_doc(coll, doc):
    cln = get_collection(coll)
    res = cln.insert_one(doc)
    return res



def upsert_one(coll, filt, updt):
    cln = get_collection(coll)
    return cln.update_one(filt, updt, upsert=True).modified_count #this will contain the number of modified docs, monitor its behaviour


def del_docs(coll, filter):
    cln = get_collection(coll)
    return cln.delete_many(filter).deleted_count # returns number of deleted docs


def find_docs_count(coll, expr):
    return find_docs(coll,expr).count()

def find_docs(coll,expr):
    cln = get_collection(coll)
    return cln.find(expr)

def find_docs_projection(coll,expr,proj):
    cln = get_collection(coll)
    return cln.find(expr,proj)

def edit_single_doc(coll, filter, update):
    cln = get_collection(coll)
    return cln.update_one(filter, update).modified_count  # will return number of documents updated

