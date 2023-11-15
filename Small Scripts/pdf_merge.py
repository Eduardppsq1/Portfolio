import os
from PyPDF2 import PdfFileReader, PdfFileMerger


k = 0
director = r'C:\Users\Example\Downloads\director_merge'
file = PdfFileMerger(strict=True)

for fisier in os.listdir(director):
    f = os.path.join(director, fisier)
    if os.path.isfile(f):
        if k == 0:
            file.merge(position=k, fileobj=f)
            k += 1
        else:
            file.merge(position=len(file.pages), fileobj=f)

file.write(os.path.join(director, 'merged_pdf.pdf'))
file.close()

for fisier in os.listdir(director):
    if fisier != 'merged_pdf.pdf':
        os.remove(os.path.join(director, fisier))
