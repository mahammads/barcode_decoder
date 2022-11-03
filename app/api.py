
import os
from fastapi import FastAPI ,File, Form, UploadFile
from app import config
from app.decoder import barcode_decode
barcode_extraction = FastAPI()

@barcode_extraction.get("/home/")
def read_root():
   return {"Status": "UP"}

@barcode_extraction.post("/get_barcode_data/")
async def get_barcode_data(uploaded_file: UploadFile = File(...)):
    path = config.input_file_path
    
    files_to_delete=os.listdir(path)
    for i in files_to_delete:
        os.remove(path+'/'+i)
    file_location = f"{path}/{uploaded_file.filename}"
    with open(file_location, "wb") as file_object:
        file_object.write(uploaded_file.file.read())
    try:          
        final_result = barcode_decode(file_location)

        if len(final_result)!=0:
            try:
                decoded_text = ','.join(final_result)        
                return {"barcode_data" : decoded_text}
            except:

                final_result = [data.decode() for data in final_result]
                decoded_text = ','.join(final_result)        
                return {"barcode_data" : decoded_text}
        else:
            return {"barcode_data" : 'no barocde detected.'}
    except Exception as e:
        raise(e)




    
