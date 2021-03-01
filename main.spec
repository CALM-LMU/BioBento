# -*- mode: python ; coding: utf-8 -*-

from ctypes.util import find_library
from pathlib import Path
from glob import glob

from PyInstaller.utils.hooks import get_package_paths
block_cipher = None

a = Analysis(['main.py'],
             pathex=['C:\\Users\\david\\Projects\\BioDetectron'],
             binaries=[],
             datas=[('C:\\Users\\david\\Projects\\BioDetectron\\osman_cpu', 'bento_cpu'),(get_package_paths('yacs')[1],"yacs"),(get_package_paths('portalocker')[1],"portalocker"),(get_package_paths('dask')[1],"dask"),(get_package_paths('py_zipkin')[1],"py_zipkin"),(get_package_paths('pythonjsonlogger')[1],"pythonjsonlogger"),(get_package_paths('bentoml')[1],"bentoml"),(get_package_paths('torchvision')[1],"torchvision"),(get_package_paths('fvcore')[1],"fvcore"),(get_package_paths('detectron2')[1],"detectron2"),(get_package_paths('matplotlib')[1],"matplotlib"),(get_package_paths('shapely')[1],"shapely"),(get_package_paths('tifffile')[1],"tifffile")],
             hiddenimports=['detectron2', 'py_zipkin', 'pythonjsonlogger', 'tabulate', 'termcolor', 'yacs', 'portalocker', 'scipy.special.cython_special', 'opencv-python', 'scikit-image', 'matplotlib', 'pcolor', 'pycocotools', 'imgaug', 'shapely', 'tifffile', "torchvision", "fvcore"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

MISSING_DYLIBS = [Path(find_library("libiomp5md")),
    Path(find_library("vcruntime140")),
    Path(find_library("msvcp140")),
    Path(find_library("asmjit"))]

dll = glob('C:\\Users\\david\\miniconda3\\Library\\bin\\*.dll')

for lib in dll:
    MISSING_DYLIBS.append(Path(lib))

a.binaries += TOC([
    (lib.name, str(lib.resolve()), 'BINARY') for lib in MISSING_DYLIBS
])

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='YeastMateDetector',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='YeastMateDetector')
