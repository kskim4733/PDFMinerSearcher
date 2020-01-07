import fitz

def main():
#-----------------------------------------------------------------------------------------------------------------------
    doc = fitz.open("C:/Users/kskim/iCloudDrive/library/Projects/Python_PDF/test_files/RS13196.pdf") # RS13196
    page_num = 3
    page = doc[page_num]
    page_size = page.bound()
    print("page size:", page_size[2], page_size[3])
    inst = fitz.Rect(277.10400,687.99600,314.69500,672.29900) # top row fer
    page.addHighlightAnnot(inst)
    doc.save("output.pdf", garbage=4, deflate=True, clean=True)

if __name__ ==  "__main__":
    main()
