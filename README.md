# PDF preview maker

Make easy pdf preview

## Config env on windows

use conda

```
conda create -n poppler python
conda activate poppler
conda install -c conda-forge poppler
conda install cmake
conda install -c conda-forge pkg-config
pip install python-poppler
pip install pillow
```

## run

```
python make_previews.py
```

## example data

Contains in folder `data`