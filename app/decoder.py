from pyzbar import pyzbar
import cv2
from dbr import *
import app.config as config
import pytesseract as pt 
import pdf2image 
import os
from PyPDF2 import PdfFileReader
import aspose.words as aw

tesseract =config.tesseract
pt.pytesseract.tesseract_cmd = tesseract
poppler_path = config.poppler_path

base_dir = os.getcwd()
temp_image_path = os.path.join(base_dir, 'pdf_to_images')
if not os.path.exists(temp_image_path):
    os.makedirs(temp_image_path)
#------------------------------------------------------------------------#
#  This function is used for decoding single barcode or qr code          #
#------------------------------------------------------------------------#
def simple_decode(image):
    img = cv2.imread(image)
    decoded_objects = pyzbar.decode(img)
    code_list = []
    for obj in decoded_objects:
        code_list.append(obj.data)
    return code_list
#---------------------------------------------------------------------------------------------#
#  This function is used for decoding multiple barcode or qr code present in single image.    #
#  please generate the key to use below library from : https://www.dynamsoft.com/             #
#---------------------------------------------------------------------------------------------#
def decode_dynamo(image):
    BarcodeReader.init_license(config.dynamo_key)
    reader = BarcodeReader()
    settings = reader.get_runtime_settings()
    settings.barcode_format_ids = EnumBarcodeFormat.BF_ALL
    settings.barcode_format_ids_2 = EnumBarcodeFormat_2.BF2_POSTALCODE | EnumBarcodeFormat_2.BF2_DOTCODE
    settings.excepted_barcodes_count = 32
    reader.update_runtime_settings(settings)
    
    try:
        out_list = []
        text_results = reader.decode_file(image)
        if text_results != None:
            for text_result in text_results:
                out_list.append(text_result.barcode_text)
        return out_list
    except BarcodeReaderError as bre:
        print(bre)

#-------------------------------------#
# combining two decoder functions.    #
#-------------------------------------#
def get_output(image):
    result1 = simple_decode(image)
    if len(result1) == 0:
        result2 = decode_dynamo(image)
        if len(result2) != 0:
            return result2
        else:
            return "no barcode detected"
    else:
        return result1
#--------------------------------------------------------------------------------#
#  This function is used converting the pdf to images for further processing.    #
#--------------------------------------------------------------------------------#
def pdf_to_image(fullpath_pdf):
    temp_images = temp_image_path
    pdf_name =os.path.split(fullpath_pdf)[-1]
    print(pdf_name)
    try:
        pdf_reader = PdfFileReader(fullpath_pdf) 
        if pdf_reader.isEncrypted:
            pdf_reader.decrypt('')
        k=pdf_reader.getNumPages()
        pages=""
        for image_path in os.listdir(temp_images):
            os.remove(temp_images+"/"+image_path)

        pages = pdf2image.convert_from_path(pdf_path=fullpath_pdf,last_page=k, dpi=500, size=(1200,1200),output_folder=temp_images,fmt="jpeg", poppler_path=poppler_path,use_pdftocairo=True, output_file=str(pdf_name))
        return temp_images
    except Exception as e:
        raise e

#--------------------------------------------------------------------------------#
#  This function is used converting the docs to images for further processing.   #
#--------------------------------------------------------------------------------#
def doc_to_image(file_name):
    doc = aw.Document(file_name)
    temp_images = config.temp_image_path
    # set output image format
    options = aw.saving.ImageSaveOptions(aw.SaveFormat.PNG)
    for image_path in os.listdir(temp_images):
        os.remove(temp_images+"/"+image_path)
    # loop through pages and convert them to PNG images
    for pageNumber in range(doc.page_count):
        options.page_set = aw.saving.PageSet(pageNumber)
        doc.save(temp_images + '/' + str(pageNumber+1)+"_page.png", options)
    return temp_images

def barcode_decode(input_file):
    if input_file.endswith(".pdf"):
        image_path = pdf_to_image(input_file)
        output_list = []
        result = ''
        for img in os.listdir(image_path):
            img_path = os.path.join(image_path, img)
            result = get_output(img_path)
            try:
                result = ','.join(result)
            except:
                result = [data.decode() for data in result]
                result = ','.join(result)

            if result == "no barcode detected":
                continue
            else:
                output_list.append(result)
        return output_list
    
    if input_file.endswith(".docx"):
        output_list = []
        image_path = doc_to_image(input_file)
        result = ''
        for img in os.listdir(image_path):
            img_path = os.path.join(image_path, img)
            result = get_output(img_path)
            if result == "no barcode detected":
                continue
            else:
                output_list.append(result[0])
        return output_list

    else:
        for ext in ['.JPEG','.JPG','.PNG','.GIF','.TIFF','.PSD','.INDD','.RAW', '.WEBP']:
            if input_file.endswith(ext) or input_file.endswith(ext.lower()):
                result = get_output(input_file)
                if not len(result) == 0:   
                    return result
            else:
                continue

# image = r"C:\Users\sarwa\Documents\project\barcode image_decoder\images\barcode-generator-lg.webp"

# output = barcode_decode(image)
# print(output)