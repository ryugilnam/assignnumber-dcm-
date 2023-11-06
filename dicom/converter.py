import os
import numpy as np
import pydicom as ds
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
from pydicom import dcmread, dcmwrite
from pydicom.pixel_data_handlers.util import apply_color_lut
import math, time



# teeth labeling list

teeth_lis=[[7,0,255,255],[255,15,0,255],[23,128,255,255],[128, 255,31,255],         #t1~t4
           [64,39,128,255],[47,128,64,255],[128,64, 55,255],[0,255,63,255],         #t5~t8
           [255,71,128,255],[79,0,255,255],[255,87,0,255],[95,128,255,255],         #t9~t12
           [128,255,103, 255],[64,111,128,255],[119,128,64,255],[128,64,127,255],   #t13~t16
           [0,255,135,255],[255,143,128,255],[151,0,255,255],[255,159,0,255],       #t17~t20
           [167,128,255,255],[128,255,175,255],[64,183,128,255],[191,128,64,255],   #t21~t24
           [128,64,199,255],[0,255,207,255],[255,215,128,255],[223,0,255,255],      #t25~t28
           [255,231,0,255],[239,128,255,255],[128,255,247,255],[64,255,128,255]]    #t29~t32

start = time.time()

# raw file load

path = "C:/Users/GN/DICOM/dicom data/"

for k in range(len(os.listdir(path))) :

    dt = os.listdir(path)[k]
    data_path = os.path.join(path, dt)

    lbc_p = data_path + "/Labeling/DCM/"
    lbc = os.listdir(lbc_p)[0]

    
    lbc_path = os.path.join(lbc_p, lbc)
    input_path = data_path + "/raw/"
    output_path = data_path + "/Preprocessed/"


    raw_dicom = dcmread(input_path + "DCT0000.DCM", stop_before_pixels = True)
    raw_frames = len(os.listdir(input_path))
    raw_Rows = raw_dicom.Rows
    raw_Columns = raw_dicom.Columns

    data = np.fromfile(lbc_path, dtype= 'uint8')
    n_channels = 4
    reshape_data = data.reshape(raw_frames, raw_Columns, raw_Rows, n_channels)


# teeth labeling

    b=reshape_data[:,:,:,0] 
    g=reshape_data[:,:,:,1] 
    r=reshape_data[:,:,:,2] 


    for tl in range(len(teeth_lis)) : 
        
            bn = np.logical_and(b==teeth_lis[tl][0],g==teeth_lis[tl][1])
            bn_x = np.logical_and(bn,r==teeth_lis[tl][2])
            teeth_cd = np.where(bn_x)
            
            reshape_data[teeth_cd[0],teeth_cd[1],teeth_cd[2]] = tl+1
             

    slice_series = (reshape_data[:,:,:,0]+reshape_data[:,:,:,1]+reshape_data[:,:,:,2])/3


    value = 33

# save data


    for i in range(raw_frames) :
        
        slice_series[i] = np.where(slice_series[i] > value, 0, slice_series[i])
        
        n = '{0:04}'.format(i)
        tmp = np.int16(slice_series[i,:,:])
        t = tmp.tobytes()

        raw_metainfo = ds.dcmread(input_path + "DCT" + n + ".dcm")
        result_metainfo = raw_metainfo
        
        result_metainfo.PixelData = t
        result_metainfo.save_as(output_path + 'DCT'+ n +".dcm")
        
    
    print(k+1 , "time : ", time.time() - start)   

