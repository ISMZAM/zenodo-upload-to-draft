# -*- coding: utf-8 -*-
"""
Upload a file to a Zenodo.org draft record
Can be useful for large files and avoiding the web interface

You will first need to create draft Zenodo record on Zenodo.org.
1.Fill in the inputs section
2.Run

Created on Tue Dec  5 16:17:37 2023
@author: ISMZAM
"""

import requests
from tqdm import tqdm
import os

""" 
##################### INPUTS ##################### 
"""
ACCESS_TOKEN = 'xxxxxx' #create one on Zenodo

filename = "filename.zip" # Specify the filename of your file
path = r"D:\%s" % filename  # Specify the directory where your file is stored (replace 'D:\')

DEPOSITION='1234567' #Get from URL in the browser when on the draft record page

"""
##################################################
"""
#%%
base_url='https://zenodo.org/api/deposit/depositions/'
deposition_url=base_url+DEPOSITION

r = requests.get(deposition_url,
                  params={'access_token': ACCESS_TOKEN})

if r.status_code == 200:
    data = r.json()
    bucket_url = data["links"]["bucket"]


    with open(path, "rb") as fp:
        params = {'access_token': ACCESS_TOKEN}
        file_size = os.path.getsize(path)

        ''' 
        The target URL is a combination of the bucket link with the desired filename
        separated by a slash.
        '''
        with tqdm.wrapattr(fp, "read", total=file_size, desc="Uploading", unit="B", unit_scale=True) as fileobj:
            response = requests.put(
                f"{bucket_url}/{filename}",
                data=fileobj,
                params=params,
            )

            # Check response status and content
            if response.status_code == 201:
                print("File uploaded successfully!")
            else:
                print(f"File upload failed with status code: {response.status_code}")
else:
    print("Failed to fetch deposition details.")