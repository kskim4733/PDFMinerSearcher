# PyPDFSearcher
PyPDFSearcher returns coordinate of the queried term and coordinates of it's corresponding text.  
The code was designed to work with [Bookreader Plugin for Resourcespace](https://github.com/leslie-lau/bookreader) and uses the following [API](https://openlibrary.org/dev/docs/api/search_inside).  
PyPDFSearcher will get called by [search_inside.php](https://github.com/leslie-lau/bookreader/blob/master/search_inside.php).  
This project was based on [this](https://github.com/leslie-lau/fulltextsearch/tree/master/src/fulltextsearch) project.  

## Requirements
This project requires [python 3.7]((https://linuxize.com/post/how-to-install-python-3-7-on-ubuntu-18-04/)) and pdfminer to work.  
Install pip for python 3,7 (python3.7 -m pip install pip).  
Make sure that pdfminer library is accessible from the python that PHP is using.  
You can install pdfminer by typing `pip install pdfminer` on your terminal.  
Please replace existing search_inside.php with the [new one](https://github.com/kskim4733/PyPDFSearcher/blob/master/search_inside.php) from this repository.  


## Overview
`PyPDFSearcher.py` finds term and text coordinate in given PDF File.  
`highlighter.py` this code is OPTIONAL. It is used to test the found coordinate by highlighting the given coordinates. It will need PyMuPDF to run.  

## Usage
`PyPDFSearcher.py` takes 6 arguments.  

`<item-id> <file-path> <query-term> <callback> <css-or-abbyy>`

Ex) `1 C:/Users/user1/Desktop/test.pdf kyle 1 abbyy` 

## Coordinate Explanation
FoundTerm class represent each term that matches the query and contains information such as coordinates.

x0: the distance from the left of the page to the left edge of the box.  
y0: the distance from the bottom of the page to the lower edge of the box.  
x1: the distance from the left of the page to the right edge of the box.  
y1: the distance from the bottom of the page to the upper edge of the box.  

In PyPDFSearcher, term(actual queried word) coordinates will be returned in order of x1, y0, y1, x0  
In PyPDFSearcher, text(the phrase that contains the term) coordinates will be returned in order of y0, y1, x1, x0  
