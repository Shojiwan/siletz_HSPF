# Main control file for building HSPF model files
import os, csv, pickle, datetime
import math as math
import pandas as pd
import shapefile
from pyhspf import Subbasin, Watershed, HSPFModel, WDMUtil
from array import *

dir1  = 'G:/005_model/001_SLZ/'

# Source the functions for processing and builing model
exec(open(dir1 + '04_scripts/01_hspf/01_python/fnct_build_hspf.py').read())

strD = datetime.datetime(2004, 1, 1)
endD = datetime.datetime(2018, 1, 1)

# Specify the land cover (HRU) file and path
hruF = dir1 + '01_inputs/01_hspf/lulc/hru_2011.csv'

# Specify the precipitation file and path
pcpF = dir1 + '01_inputs/01_hspf/pcp/pcp_base.csv'

# Specify the PET file and path
petF = dir1 + '01_inputs/01_hspf/pet/pet_base.csv'

# Specify the fTable file and path
fTab = dir1 + '01_inputs/01_hspf/ftab/ftab.csv'

# Specify the basin shapefile and path
bsnF = dir1 + '01_inputs/01_hspf/shp/basins.shp'

# Specify the reach shapefile and path
rchF = dir1 + '01_inputs/01_hspf/shp/reaches.shp'

# Specify the model file and path (where to write the model)
modF = dir1 + '03_models/01_hspf/siletz.hspf'

# BUILD THE MODEL
build_hspf_model(hruF, pcpF, petF, fTab, bsnF, rchF, modF)
