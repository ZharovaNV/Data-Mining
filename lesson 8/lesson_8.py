"""
Задача:
Извлечь серийные номера из файлов ( приложены в материалах урока)

Ваша задача разобрать все фалы, распознать на них серийный номер и
создать коллекцию в MongoDB с четким указанием из какого файла был
взят тот или иной серийный номер.

Дополнительно необходимо создать коллекцию и отдельную папку для хранения файлов
в которых вы не смогли распознать серийный номер, если в файле встречается несколько
зображений необходимо явно указать что в файле таком-то страница такая
серийный номер не найден.
"""

import os
import shutil
from pymongo import MongoClient
from cash_box_parse import extract_number, extract_pdf_image, save_pdf_image, IMAGE_FOLDER_PATH

WRONG_FILE_DIR = 'C:\Наталия\Geek\Data Mining\lesson 8\data_for_parse\wrong'

def after_extract(db, root, name, num_list):
    if num_list:
        for num in num_list:
            item = {'dir': root,
                    'file': name,
                    'numb': num[0]}
            collection = db['correct']
            collection.insert_one(item)
            print(os.path.join(root, name), ' ### ', num_list)
            print(item)
    else:
        item = {'dir': root,
                'file': name,
                'str': 1}
        collection = db['wrong']
        collection.insert_one(item)
        shutil.copyfile(os.path.join(root, name), os.path.join(WRONG_FILE_DIR, name))


if __name__ == '__main__':
    client = MongoClient('mongodb://localhost:27017/')
    db = client['file_parse']

    file_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data_for_parse')
    for root, dirs, files in os.walk(file_dir, topdown=False):
        for name in files:
            if name.endswith('.jpg'):
                num_list = extract_number(os.path.join(root, name))
                after_extract(db, root, name, num_list)


            elif name.endswith('.pdf'):
                extr_img = extract_pdf_image(os.path.join(root, name))
                img_list = save_pdf_image(name, IMAGE_FOLDER_PATH, *extr_img)
                for itm in img_list:
                    num_list = extract_number(itm)
                    after_extract(db, root, name, num_list)

            # else:
            #     after_extract(db, root, name, [])

