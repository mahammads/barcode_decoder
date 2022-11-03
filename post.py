import requests
myurl = 'http://localhost:9080/get_barcode_data/'

image_file = r"C:\Users\sarwa\Documents\project\barcode image_decoder\images\WhatsApp Image 2022-11-03 at 01.39.38.jpg"

files = {'uploaded_file': open(image_file, 'rb')}
getdata = requests.post(myurl, files=files)
print(getdata.text)
