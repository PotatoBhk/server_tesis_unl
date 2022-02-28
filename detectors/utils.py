from functools import cmp_to_key
from ctypes import wintypes, windll
from skimage.metrics import structural_similarity as ssim
from os import path
import cv2

class Utils:

    def __init__(self):
        print("init utils")

    def path_exists(self, root):
        return path.exists(root)

    def join_path(self, root, file):
        return path.realpath(path.join(root, file))

    def preprocess_img(self, img, shape = (300,300)):
        frame_resized = cv2.resize(img, shape, interpolation = cv2.INTER_CUBIC)
        return cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), 
                    (127.5, 127.5, 127.5), False)
    
    def winsort(self, data):
        _StrCmpLogicalW = windll.Shlwapi.StrCmpLogicalW
        _StrCmpLogicalW.argtypes = [wintypes.LPWSTR, wintypes.LPWSTR]
        _StrCmpLogicalW.restype  = wintypes.INT

        cmp_fnc = lambda psz1, psz2: _StrCmpLogicalW(psz1, psz2)
        return sorted(data, key=cmp_to_key(cmp_fnc))

    def equality(self, a, b):
        if(a.shape == b.shape):            
            a_gray = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
            b_gray = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
            return ssim(a_gray, b_gray)
        else:
            return 0.0