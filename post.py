import requests
import sys

file_name = sys.argv[1]
myurl = 'https://cat-detect.herokuapp.com/get_plant_status/'

image_file = file_name

files = {'uploaded_file': open(image_file, 'rb')}
getdata = requests.post(myurl, files=files)
print(getdata.text)
