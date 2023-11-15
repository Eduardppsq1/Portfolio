import os
import PyPDF2

director = r'C:\Users\Example\Desktop\Director_rotate'
os.chdir(director)
fisier = 'Curs 2.pdf'

pdf_in = open(fisier, 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf_in)
pdf_writer = PyPDF2.PdfFileWriter()

for pagenum in range(pdf_reader.numPages):
    page = pdf_reader.getPage(pagenum)
    page.rotateClockwise(-90)
    pdf_writer.addPage(page)

pdf_out = open(os.path.join(director, 'rotated_pdf.pdf'), 'wb')
pdf_writer.write(pdf_out)
pdf_out.close()
pdf_in.close()
