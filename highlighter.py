import fitz

def main(x0, y0, x1, y1, pdfPath, page_num):
#-----------------------------------------------------------------------------------------------------------------------
    doc = fitz.open(pdfPath) # RS13196
    page = doc[page_num]
    page_size = page.bound()
    print("page size:", page_size[2], page_size[3])
    inst = fitz.Rect(x0, y0, x1, y1) # top row fer
    page.addHighlightAnnot(inst)
    doc.save("output.pdf", garbage=4, deflate=True, clean=True)

if __name__ ==  "__main__":
    # Provide x0, y0, x1, y1 input from the PyPDFSearcher.py from either textbound or termbound
    main()
