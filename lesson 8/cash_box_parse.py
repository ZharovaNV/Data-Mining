import shutil
import os
from os import path
import PyPDF2
from PyPDF2.utils import PdfReadError
from PIL import Image
import pytesseract
import time
import re

pdf_file_path = os.path.join('C:\Наталия\Geek\Data Mining\lesson 8\data_for_parse', '4696_4.pdf')
file_name = '5387_4.pdf'
IMAGE_FOLDER_PATH = 'C:\Наталия\Geek\Data Mining\lesson 8\data_for_parse\image'


# todo Извлеч JPG из PDF и сохранить в соответствующую папку

def extract_pdf_image(pdf_path):
    try:
        pdf_file = PyPDF2.PdfFileReader(open(pdf_path, 'rb'), strict=False)
    except PdfReadError as e:
        print(e)
        return None
    except FileNotFoundError as e:
        print(e)
        return None
    result = []
    for page_num in range(0, pdf_file.getNumPages()):
        page = pdf_file.getPage(page_num)
        page_obj = page['/Resources']['/XObject'].getObject()

        if page_obj['/Im0'].get('/Subtype') == '/Image':
            size = (page_obj['/Im0']['/Width'], page_obj['/Im0']['/Height'])
            data = page_obj['/Im0']._data

            mode = 'RGB' if page_obj['/Im0']['/ColorSpace'] == '/DeviceRGB' else 'P'

            decoder = page_obj['/Im0']['/Filter']
            if decoder == '/DCTDecode':
                file_type = 'jpg'
            elif decoder == '/FlateDecode':
                file_type = 'png'
            elif decoder == '/JPXDecode':
                file_type = 'jp2'
            else:
                file_type = 'bmp'

            result_sctrict = {
                'page': page_num,
                'size': size,
                'data': data,
                'mode': mode,
                'file_type': file_type,
            }

            result.append(result_sctrict)
    return result


def save_pdf_image(file_name, f_path, *pdf_strict):
    file_paths = []
    for itm in pdf_strict:
        name = f'{file_name}_#_{itm["page"]}.{itm["file_type"]}'
        file_path = path.join(f_path, name)

        with open(file_path, 'wb') as image:
            image.write(itm['data'])
        file_paths.append(file_path)
    return file_paths


def extract_number(file_path):
    numbers = []
    img_obj = Image.open(file_path)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(img_obj, 'rus')
    pattern_list = ['заводской (серийный) номер', 'заводской номер (номера)']
    pattern2 = '(если такие серия и номер имеються)'

    find_str = -1
    need_find = 'Y'
    for idx, line in enumerate(text.split('\n')):
        for pattern in pattern_list:
            if line.lower().find(pattern) + 1:
                text_en = pytesseract.image_to_string(img_obj, 'eng')
                # number = text_en.split('\n')[idx].split(' ')[-1]
                # numbers.append((number, file_path))
                for str_itm in text_en.split('\n')[idx].split(' '):
                    if str_itm.replace('-', '').isdigit() or re.search(r'^[A-Z][0-9]{2}[A-Z][0-9]{5}$', str_itm):
                        numbers.append((str_itm, file_path))
                        if pattern == pattern_list[1]:
                            need_find = 'N'
        if line.lower().find(pattern2) + 1:
            find_str = idx + 2
        if find_str == idx and need_find == 'Y':
            text_en = pytesseract.image_to_string(img_obj, 'eng')
            for str_itm in text_en.split('\n')[idx].split(' '):
                if str_itm.replace('-', '').isdigit() or re.search(r'^[A-Z][0-9]{2}[A-Z][0-9]{5}$', str_itm):
                    numbers.append((str_itm, file_path))

    return numbers


if __name__ == '__main__':
    a = extract_pdf_image(pdf_file_path)
    b = save_pdf_image(file_name, IMAGE_FOLDER_PATH, *a)
    c = [extract_number(itm) for itm in b]
    print(1)
