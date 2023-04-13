import eel
import tkinter.filedialog
import tkinter.messagebox
import numpy as np
import platform
import cv2
from igorwriter import IgorWave
import time
import polars as pl

from .clean import *
from .centering import *
from .db import RixsDB
from .api import *

import faulthandler
faulthandler.enable()

db = None


@eel.expose
def openLocalFolder():
    global db
    folder_path = startTkDialog()
    if folder_path == "break":
        return None

    db = RixsDB(folder_path)

    file_paths = searchFiles(folder_path, "hdf5")
    db.setFilePaths(file_paths)

    return folder_path

@eel.expose
def dbClear():
    if db:
        db.clear()

@eel.expose
def test():
    np.random.seed(334)
    A = np.arange(7)
    wave_A = IgorWave(A, name='A')
    print(wave_A)
    file_name = startTkSaveWindow()
    wave_A.save_itx(file_name + '.itx')
    return file_name + '.itx'

@eel.expose
def saveCSV(title, data):
    file_name = startTkSaveWindow()
    result = {}
    data = np.array(data).T
    for i in range(len(title)):
        result[title[i]] = data[i]
    df = pl.DataFrame(result)
    df.write_csv(file_name + ".csv")
    return file_name + ".csv"

@eel.expose
def saveIgor(title, data):
    file_name = startTkSaveWindow()
    result = []
    for i in range(len(title)):
        result.append(IgorWave(data[i], name=title[i]))
    with open(file_name + '.itx', mode='w') as f:
        for r in result:
            r.save_itx(f)
    return file_name + ".itx"

@eel.expose
def loadFile(id):
    result = db.getFile(id)
    if not result or not result['is_load']:
        full_path = db.getFullPath(id)
        dset, bg_dset, layer_size = convartH5pyFile(full_path)
        if dset is None:
            return {"error": "No such file."}
        eel.spawn(asyncSetImages(id, dset, bg_dset, layer_size))
        return
    else:
        eel.spawn(asyncLoadImages(id))
        return

@eel.expose
def setCurrentFile(id, index):
    current_id = id
    current_index = index
    data, max = db.getImageByLayer(current_id, current_index)
    dset = cv2.imdecode(data, cv2.IMREAD_GRAYSCALE)
    return {"size": np.shape(dset)}

def asyncSetImages(id, dset, bg_dset, layer_size):
    db.setImages(id, dset, bg_dset, layer_size)
    asyncLoadImages(id)

def asyncLoadImages(id):
    image_data, index = db.getImage(id)
    images = [imageToBase64(id) for id in image_data]
    distribution = [imgValues(cv2.imdecode(id, cv2.IMREAD_GRAYSCALE)) for id in image_data]
    eel.setImage([[images[i], index[i], distribution[i]]
                 for i in range(len(index))])

def loadImage(id, layer=0):
    image_data, max = db.getImageByLayer(id, layer)
    if image_data is None:
        return None, None
    image = imageToBase64(image_data)
    data = db.getData(id)
    return image, data['size']

@eel.expose
def autoFindRange():
    auto_range = findRect(dset)
    return auto_range

@eel.expose
def clipImage(id, current_index, range):
    data, max = db.getImageByLayer(id, current_index)
    dset = cv2.imdecode(data, cv2.IMREAD_GRAYSCALE)
    clip_dset = clip_image(dset, range)
    dset_max = int(np.max(clip_dset))
    image = saveImage(clip_dset)
    distribution = imgValues(clip_dset)
    return {"img": image, "size": np.shape(clip_dset), "dist": distribution, "max": dset_max}

@eel.expose
def clipImageProfiles(id, range):
    image_data, _ = db.getImage(id)
    distribution = [
        imgValues(clip_image(cv2.imdecode(dset, cv2.IMREAD_GRAYSCALE), range))
    for dset in image_data]
    return distribution

@eel.expose
def photonCount(current_id, current_index, clip_range, thres_range):
    # t1 = time.time()
    print("photonCount", current_id, current_index, "clip_range", clip_range)
    data, max = db.getImageByLayer(current_id, current_index)
    # t2 = time.time()
    raw_thres_range = np.array(thres_range) * (max / 255)
    print("max", max, "thres_range", thres_range,
          "raw_thres_range", raw_thres_range)
    dset = cv2.imdecode(data, cv2.IMREAD_GRAYSCALE)
    # t3 = time.time()
    clip_dset = clip_image(dset, clip_range)
    # t4 = time.time()
    result_dset, single_count_list = Centering(clip_dset, raw_thres_range)
    # t5 = time.time()
    # result_img = saveImage(result_dset)
    # crip_img = saveImage(clip_dset)
    # dset_max = int(np.max(clip_dset))
    # t6 = time.time()
    # print(f"load file：{t2-t1}")
    # print(f"set data：{t3-t2}")
    # print(f"clip image：{t4-t3}")
    # print(f"centering：{t5-t4}")
    # print(f"get image：{t6-t5}")
    return {"index": current_index, "raw_img": "", "result_img": "", "size": np.shape(clip_dset), "results": single_count_list, "max": 255}

@eel.expose
def showDb():
    global db
    return db.show()

@eel.expose
def loadFiles():
    return db.getFilePaths()

def startTkDialog():
    root = tkinter.Tk()
    root.geometry("0x0")
    root.overrideredirect(1)
    root.withdraw()
    system = platform.system()

    if system == "Windows":
        root.deiconify()
    root.update()
    root.lift()
    root.focus_force()

    current_dir = os.path.abspath(os.path.dirname(__file__))
    folder_path = tkinter.filedialog.askdirectory(
        title="Open Folder", initialdir=current_dir)
    root.update()
    root.destroy()

    if system == "Windows":
        root.withdraw()
    if folder_path == "":
        return "break"
    return folder_path


def startTkSaveWindow():
    root = tkinter.Tk()
    root.geometry("0x0")
    root.overrideredirect(1)
    root.withdraw()
    system = platform.system()

    if system == "Windows":
        root.deiconify()
    root.update()
    root.lift()
    root.focus_force()

    current_dir = os.path.abspath(os.path.dirname(__file__))
    file_name = tkinter.filedialog.asksaveasfilename(initialdir=current_dir)

    root.update()
    root.destroy()

    print(file_name)

    if system == "Windows":
        root.withdraw()
    if file_name == "":
        return "break"
    return file_name

def close(*args):
    print("close")
    if db:
        db.close()
    exit()

def build():
    eel.init("web")
    eel.start("index.html", port=0, close_callback=close, cmdline_args=[
              "-–disable-background-mode", "-–disable-sync", "-–start-maximized"])
