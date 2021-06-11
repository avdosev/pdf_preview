import json
from poppler import load_from_file, PageRenderer
from PIL import Image
import os

def save_image(image, filename, width, height):
    # трансформируем изображения в удобный формат
    pil_image = Image.frombytes(
        "RGBA",
        (image.width, image.height),
        image.data,
        "raw",
        str(image.format),
    )
    # если нужно чтобы изображения были с темже соотношением сторон, то меняй комментирование
    # pil_image.thumbnail((width, height), Image.ANTIALIAS)
    pil_image = pil_image.resize((width, height), Image.ANTIALIAS)

    pil_image.save(filename)


def make_previews(settings):
    renderer = PageRenderer()
    pdf_document = load_from_file(settings['data_path'])
    print('make output folder')

    name_format: str = settings['preview_name_template']
    output_folder = settings['output_path']
    
    # создаем нужную папку для превьюшек
    os.makedirs(output_folder, exist_ok=True)
    
    # данные для с размерами страниц
    output_data = {'pages': []}

    for page in settings['pages']:
        index = page['index']
        print('start page', index+1)

        # рендер страницы
        pdf_page = pdf_document.create_page(index)
        image = renderer.render_page(pdf_page)

        # сохраняем превьюшки в нужных размерах
        for size in page['sizes']:
            width = size['width']
            height = size['height']
            filename = name_format.format(page_number=index+1, width=width, height=height)
            path = os.path.join(output_folder, filename)
            print('save preview', filename)
            save_image(image, path, width, height)
        
        output_data['pages'].append({'number': index+1, 'width': image.width, 'height': image.height})

    # сохраняем json файл с данными оригинальных размерах страниц
    pdf_info_filename = os.path.join(output_folder, 'pdf_data.json')
    print('save pdf info to', pdf_info_filename)
    with open(pdf_info_filename, 'w') as f:
        json.dump(output_data, f)

if __name__ == '__main__':
    with open('data/json.json', 'r') as f:
        settings = json.load(f)
        make_previews(settings)