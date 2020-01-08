import sys
import copy
try:
    import pdfminer
    from pdfminer.pdfparser import PDFParser
    from pdfminer.pdfdocument import PDFDocument
    from pdfminer.pdfpage import PDFPage
    from pdfminer.pdfpage import PDFTextExtractionNotAllowed
    from pdfminer.pdfinterp import PDFResourceManager
    from pdfminer.pdfinterp import PDFPageInterpreter
    from pdfminer.layout import LAParams
    from pdfminer.converter import PDFPageAggregator
    from pdfminer.pdfinterp import resolve1
except ImportError:
    sys.exit("""You need pdfminer!
                try running `pip install -U pdfminer` """)


class FoundTerm:
    def __init__(self, term, start_index, end_index, x0, y0, x1, y1, page_num, page_size_x, page_size_y, text_obj):
        self.term = term
        self.start_index = start_index
        self.end_index = end_index
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.page_num = page_num
        self.page_size_x = page_size_x
        self.page_size_y = page_size_y
        self.text_obj = text_obj

    def get_term_bound(self):
        return self.x0, self.y0, self.x1, self.y1

    def get_page_num(self):
        return self.page_num

    def get_page_size(self):
        return self.page_size_x, self.page_size_y

    def get_text_bound(self):
        return self.text_obj.bbox[0], self.page_size_y - self.text_obj.bbox[1], self.text_obj.bbox[2], self.page_size_y - self.text_obj.bbox[3]

    def get_marked_text(self):
        text = self.text_obj.get_text().replace('\n', '')
        new_text = text[:self.start_index] + "{{{" + text[self.start_index:self.end_index] + "}}}" + text[
                                                                                                     self.end_index:]
        return new_text

    def print_info(self):
        print("text:%s" % (self.get_marked_text()))
        print("page_num:%d" % (self.get_page_num()))
        print("page_size:%.5f,%.5f" % (self.get_page_size()))
        print("text-bound:%.5f,%.5f,%.5f,%.5f" % (self.get_text_bound()))
        print("term-bound:%.5f,%.5f,%.5f,%.5f\n" % (self.get_term_bound()))


class PDFTermSearch:
    all_matches = []

    def __init__(self, cb, ia, term, file_path):
        self.cb = cb
        self.ia = ia
        self.search_term = term
        self.fp = open(file_path, 'rb')
        try:
            self.parser = PDFParser(self.fp)
            self.document = PDFDocument(self.parser)
            # Check if the document allows text extraction. If not, abort.
            if not self.document.is_extractable:
                raise PDFTextExtractionNotAllowed
            self.total_page_num = (resolve1(self.document.catalog['Pages'])['Count'])
        except:
            print("ERROR: Cannot open PDF File")
            self.fp.close()
            exit(1)

    def print_result(self):
        print("callback:%s" % str(self.cb))
        print("ia:%s" % str(self.ia))
        print("term:%s" % self.search_term)
        print("pages:%d\n" % self.total_page_num)
        for ft in self.all_matches:
            ft.print_info()

    def fix_list(self, chr_list):
        # this function is used to separate occasional mis assignment of multiple character in to one LTChar class
        new_list = []
        for index in range(0, len(chr_list)):
            character = chr_list[index]
            if len(character.get_text()) > 1:
                sub_list = []
                for sub_index in range(0, len(character.get_text())):
                    sub_chr_text = character.get_text()[sub_index]
                    sub_chr = copy.deepcopy(character) # used to copy object
                    sub_chr._text = sub_chr_text
                    sub_list.append(sub_chr)
                new_list.extend(sub_list)
            else:
                new_list.append(character)
        return new_list

    def find_term_coord(self, term, text_obj, page_num, page_size_x, page_size_y):
        term_length = len(term)
        text = text_obj.get_text().lower()
        chr_list = text_obj._objs
        search_start = 0
        search_end = len(text)

        if len(chr_list) != len(text):
            chr_list = self.fix_list(chr_list)

        while term in text[search_start: search_end]:
            term_start_index = text.lower().find(term.lower(), search_start, search_end)
            term_end_index = term_start_index + term_length
            term_start = chr_list[term_start_index]
            term_end = chr_list[term_end_index - 1]

            self.all_matches.append(FoundTerm(term=term, start_index=term_start_index, end_index=term_end_index,
                                              x0=term_start.x0, y0=page_size_y - term_start.y0,
                                              x1=term_end.x1, y1=page_size_y - term_end.y1,
                                              page_num=page_num, page_size_x=page_size_x, page_size_y=page_size_y,
                                              text_obj=text_obj))
            search_start = term_end_index

    def parse_obj(self, lt_objs, page_num, search_term, page_size_x, page_size_y):
        # loop over the object list
        for obj in lt_objs:
            if isinstance(obj, pdfminer.layout.LTTextLine):
                if search_term in obj.get_text().lower():
                    self.find_term_coord(search_term, obj, page_num, page_size_x, page_size_y)

            # if it's a textbox, also recurse
            if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
                self.parse_obj(obj._objs, page_num, search_term, page_size_x, page_size_y)

            # if it's a container, recurse
            elif isinstance(obj, pdfminer.layout.LTFigure):
                self.parse_obj(obj._objs, page_num, search_term, page_size_x, page_size_y)

    def search_pdf(self):
        # Create a PDF resource manager object that stores shared resources.
        rsrcmgr = PDFResourceManager()

        # BEGIN LAYOUT ANALYSIS
        # Set parameters for analysis.
        laparams = LAParams()

        # Create a PDF page aggregator object.
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)

        # Create a PDF interpreter object.
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        page_num = 0
        # loop over all pages in the document
        for page in PDFPage.create_pages(self.document):
            # read the page into a layout object
            interpreter.process_page(page)
            layout = device.get_result()

            # extract text from this object
            self.parse_obj(layout._objs, page_num, self.search_term.lower(), page.mediabox[2], page.mediabox[3])
            page_num += 1

        self.print_result()
        self.fp.close()


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("ERROR: Invalid Arguments Length")
        print("Usage: <item-id> <file-path> <query-term> <callback> <css-or-abbyy>")
        exit(1)

    item_id = sys.argv[1]
    path = sys.argv[2]
    query_term = sys.argv[3]
    callback = sys.argv[4]
    pdf_style = sys.argv[5]

    pdf_searcher = PDFTermSearch(callback, item_id, query_term, path)
    pdf_searcher.search_pdf()
