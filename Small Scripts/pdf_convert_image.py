import os
from PIL import Image
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

director = r'C:\Users\Example\Downloads\director_poze'

for fisier in os.listdir(director):
    f = os.path.join(director, fisier)
    try:
        image_1 = Image.open(f)
        im_1 = image_1.convert('RGB')
        im_1.save(f'{f}.pdf')
    except:
        continue
    finally:
        os.remove(f)
