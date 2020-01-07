# PyPDFSearcher
PDF Searcher that returns coordinate of the queried term and it's corresponding text

## Requirements
This Project requires pdfminer to run. If not installed try running

`pip install pdfminer`

If you wish to use highlighter.py you will need to install PyMuPDF

'pip install pymupdf`


## Overview
`PyPDFSearcher.py` finds term and text coordinate in given PDF File 
`highlighter.py` is used to highlight the coordinate found using PyPDFSearcher.

## Usage
`PyPDFSearcher.py` takes 6 arguments 

`<item-id> <file-path> <query-term> <callback> <css-or-abbyy>`

Ex) `1 C:/Users/user1/Desktop/test.pdf kyle 1 abbyy` 
