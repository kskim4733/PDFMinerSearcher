import fitz

def main():
#-----------------------------------------------------------------------------------------------------------------------
    doc = fitz.open("C:/Users/kskim/iCloudDrive/library/Projects/PyPDFSearcher/test_files/RS13170.pdf") # RS13196
    page_num = 2
    page = doc[page_num]
    page_size = page.bound()
    print("page size:", page_size[2], page_size[3])
    inst = fitz.Rect(36.00000,715.60550,63.17000,702.39450) # top row fer
    page.addHighlightAnnot(inst)
    doc.save("output.pdf", garbage=4, deflate=True, clean=True)

if __name__ ==  "__main__":
    main()
