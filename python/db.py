from tinydb import TinyDB, Query, where
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
import datetime, uuid
import cv2
import os
import numpy as np
import polars as pl
import time

def timestamp():
    return datetime.datetime.now().timestamp()

class DB:
    def __init__(self, file_name, is_caching=False):
        self.file_name = file_name + ".json"
        if is_caching:
            self.db = TinyDB(self.file_name, storage=CachingMiddleware(JSONStorage))
        else:
            self.db = TinyDB(self.file_name)

    def all(self):
        return self.db.all()
    
    def clear(self):
        for t in self.db.tables():
            self.db.drop_table(t)
        self.db.truncate()
        return True
    
    def close(self):
        self.db.close()
    
    def insert(self, obj):
        return self.db.insert(obj)
    
    def get(self, querie=None, doc_id=None):
        if doc_id is not None:
            return self.db.get(doc_id=doc_id)
        return self.db.get(querie)
    
    def upsert(self, obj, querie=None):
        return self.db.upsert(obj, querie)
    
    def table(self, name):
        return self.db.table(name)
    
    def remove(self, doc_ids):
        return self.db.remove(doc_ids=doc_ids)

class RixsDB:
    def __init__(self, root_path: str):
        self.file_db = DB(root_path + "/rixs_analysys_index")
        self.root_index = self.file_db.table('root')
        self.file_index = self.file_db.table('file')
        self.data_index = self.file_db.table('data')
        if len(self.root_index.all()) == 0:
            self.dbInit(root_path)
    
    def dbInit(self, root_path: str) -> None:
        self.root_index.insert({
            'root_path': root_path,
            'create_at': timestamp()
        })
    
    def clear(self):
        self.file_db.clear()
    
    def close(self):
        self.file_db.close()
    
    def show(self):
        self.file_db.all()
    
    def getFolderPath(self) -> dict[str, str]:
        return self.root_index.get(doc_id=1)['root_path']
    
    def setFilePaths(self, file_paths: list[str]) -> None:
        queries = Query()
        for fp in file_paths:
            result = self.file_index.get(queries.path == fp)
            if result is None:
                self.file_index.insert({
                    'id': str(uuid.uuid1()),
                    'path': fp,
                    'is_load': False,
                    'create_at': timestamp()
                })
    
    def getFilePaths(self) -> list[str]:
        fi= self.file_index.all()
        return sorted(fi, key=lambda x: x['path'])
    
    def getFullPath(self, id: str) -> str:
        queries = Query()
        root_path = self.getFolderPath()
        file_index = self.file_index.get(queries.id == id)
        if file_index is not None:
            return root_path + '/' + file_index['path']
        else:
            return None

    def getFile(self, id):
        queries = Query()
        return self.file_index.get(queries.id == id)

    def initImgesFils(self, id):
        queries = Query()
        file_index = self.file_index.get(
            (queries.id == id) & (queries.is_load == True)
        )
        if file_index is not None:
            file_path = file_index['file_path']
            os.remove(file_path)
    
    def setImages(self, id: str, np_array, bg_array, layer_size):
        folder_path = self.getFolderPath() + '/parquet_data'
        os.makedirs(folder_path, exist_ok=True)

        self.initImgesFils(id)

        if layer_size == 0:
            size = np.shape(np_array)[0:2]
            df = pl.DataFrame(
                {
                    "image": [cv2.imencode('.webp', np_array)[1]],
                    "index": [0],
                    "max": np.max(np_array)
                }
            )
        else:
            size = np.shape(np_array)[1:3]
            images_array = [cv2.imencode('.webp', na)[1] for na in np_array]
            max_array = [np.max(na) for na in np_array]
            bg_array = cv2.imencode('.webp', bg_array)[1]
            df = pl.DataFrame(
                {
                    "image": [bg_array] + images_array,
                    "index": range(-1, layer_size),
                    "max": [np.max(bg_array)] + max_array
                }
            )

        file_path = folder_path + '/' + id + '.parquet'
        df.write_parquet(file_path)

        queries = Query()
        self.data_index.insert({
            'id': id,
            'file_path': file_path,
            'size': size,
            'layer_size': layer_size,
            'create_at': timestamp()
        })
        self.file_index.upsert({
            'is_load': True,
            'update_at': timestamp()
        }, queries.id == id)

    def getData(self, id: str) -> dict[str, str]:
        queries = Query()
        data = self.file_index.get(queries.id == id)
        if data is None:
            return None
        if data['is_load']:
            file_data = self.data_index.get(queries.id == id)
            if file_data is not None:
                data.update(file_data)
        return data
    
    def getImage(self, id: str):
        data = self.getData(id)
        if data is None:
            return None
        df = pl.read_parquet(source=data['file_path'])
        images = [i.to_numpy() for i in df.get_column("image")]
        index = df.get_column("index").to_list()
        return images, index

    def getImageByLayer(self, id: str, index=0):
        t1 = time.time()
        data = self.getData(id)
        t2 = time.time()
        if data is None:
            return None
        df = pl.read_parquet(source=data['file_path']).filter(pl.col("index") == index)
        t3 = time.time()
        print(f"get db data：{t2-t1}")
        print(f"get image data：{t3-t2}")
        return df.get_column("image")[0].to_numpy(), df.get_column("max")[0]
