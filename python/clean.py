import h5py
import cv2
import numpy as np
from PIL import Image
import base64
import os
import glob
import json
from json import JSONEncoder

def convartH5pyFile(file_name):
    f = h5py.File(file_name, 'r')
    dset = np.array(f[list(f.keys())[0]])
    dim = dset.ndim
    if dim == 3:
        bg_dset = dset[0][:][:]
        dset = dset[1: np.shape(dset)[0] - 1][:][:] - bg_dset
        dset = np.multiply(dset, np.where(dset < 10000, True, False))
        return dset, bg_dset, np.shape(dset)[0]
    elif dim == 2:
        return dset, [], 0
    elif dim < 2 or dim >= 3:
        print("load error")
        return None, None, None

def imageToBase64(image):
    img_base64 = base64.b64encode(image)
    return 'data:image/webp;base64,' + img_base64.decode()

def writeImage(dset, name):
    current_dir = current_dir = os.path.abspath(os.path.dirname(__file__))
    if np.max(dset) != 0:
        dset = 255 - dset * (255 / np.max(dset))
    cv2.imwrite(current_dir + "/result/" + name + ".png", dset)

def saveImage(dset, path="", is_simple=False):
    # if not is_simple:
    #     mask = np.where(dset == 0, True, False)
    if np.max(dset) != 0:
        dset = 255 - dset * (255 / np.max(dset))
    result, dst_data = cv2.imencode('.webp', dset)
    # if is_simple:
    #     img_base64 = base64.b64encode(dst_data)
    #     return 'data:image/png;base64,' + img_base64.decode()
    # dst_data = cv2.imdecode(dst_data, cv2.IMREAD_UNCHANGED)
    # dst_data = cv2.cvtColor(dst_data, cv2.COLOR_BGR2BGRA)
    # dst_data[mask, 3] = 0
    # dst_data[~mask, 0:2] = 0
    # result, dst_data = cv2.imencode('.webp', dst_data)
    img_base64 = base64.b64encode(dst_data)
    return 'data:image/png;base64,' + img_base64.decode()

def imgValues(dset):
    new_dset = dset[np.nonzero(dset)]
    new_dset = np.ravel(new_dset)
    key_dset, value_dset = np.unique(new_dset, return_counts=True)
    key_dset = key_dset.tolist()
    value_dset = value_dset.tolist()
    return dict(zip(key_dset, value_dset))

def cahngeColormap(path, colormap="COLORMAP_RAINBOW"):
    pic = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    pseudo_color = cv2.applyColorMap(pic, cv2.COLORMAP_RAINBOW)
    cv2.imwrite(path, np.array(pseudo_color))

def clip_image(array, obserbed_range):
    [x_range_min, x_range_max], [y_range_min, y_range_max] = (obserbed_range)
    array = np.array(array)
    new_array = array[x_range_min:x_range_max, y_range_min:y_range_max]
    return new_array

def findRect(dset, threshold=0.1, blur_size=5, min_area=50):
    if np.max(dset) != 0:
        dset = dset * (255 / np.max(dset))
    dset = np.where(dset > threshold*255, 255.0, 0.0)
    dst_data = Image.fromarray(dset).convert("L")
    # dst_data.save("./tmp/test1.png")

    blur = cv2.GaussianBlur(np.array(dst_data), (blur_size, blur_size), 1)
    # Image.fromarray(blur).convert("L").save("./tmp/test2.png")
    
    contours, hierarchy = cv2.findContours(
        blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = [c for c in contours if cv2.contourArea(c) >= min_area]
    # img = np.array(dst_data)
    # for c in contours:
    #     x, y, w, h = cv2.boundingRect(c)
    #     img = cv2.rectangle(img, (x, y), (x+w-1, y+h-1), (255, 255, 255), 2)
    # Image.fromarray(img).convert("L").save("./tmp/test3.png")
    
    # img = np.array(dst_data)
    min_x = min(cv2.boundingRect(c)[0] for c in contours)
    max_x = max(cv2.boundingRect(c)[0] +
                cv2.boundingRect(c)[2] for c in contours)
    min_y = min(cv2.boundingRect(c)[1] for c in contours)
    max_y = max(cv2.boundingRect(c)[1] +
                cv2.boundingRect(c)[3] for c in contours)
    # img = cv2.rectangle(
    #     img, (min_x, min_y), (max_x-1, max_y-1), (255, 255, 255), 2)
    # Image.fromarray(img).convert("L").save("./tmp/test4.png")

    return [[min_y, max_y-1], [min_x, max_x-1]]


def searchFiles(root_path, file_type, include_subfolder=False):
    file_paths = []
    condition = root_path + ('/**/*.' if include_subfolder else '/*.') + file_type
    for name in glob.glob(condition):
        file_paths.append(os.path.split(name)[1])
    return file_paths