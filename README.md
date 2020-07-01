KBSearchEngine - capable of answering from documents like word, pdfs, ppts, pptx and excel sheets

For now - focus only on PDF files

1.Make sure python v2 and v3 is installed with pip.

Skip 2 and 3 if you have already done once

2. Install virtualenv package (For first time use)

    pip install virtualenv

3. Create python virtual environment (For first time use only because we can use already existing virtualenv if not first time)

    virtualenv mypython
    
4. Activate the virtual environment

    For MAC users: source mypython/bin/activate
    
    For windows users: mypython/Scripts/activate

5. Command to install all the requirements for this project

   pip install -r requirements.txt (For first time use)
          
6. when you want to come out of virtual env - deactivate it... If you want to keep running the program no need to deactivate.

7. Run application

    python app.py 

    Comment out below lines if you have already run app.py once.(To save time)

    nltk.download('punkt') # first-time use only
    nltk.download('wordnet') # first-time use only
    nltk.download('words')# first-time use only
    
    Downloading them once is sufficient.


-------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------

Step1 :
Use Python modules to Read the documents.

Different Python modules available to work individually
1. PDFs - by pip install PyPDF2(didn't use* for this project) OR pip install pdfminer (used* this for our project)
2. Word - by pip install python-docx (didn't use* for this project)
3. PPTx - pip install python-pptx
4. ppt - brew install tika
5. xlsx - reading and writing Excel 2010 files(new files) - pip install openpyxl
6. xls - read older excel files - pip install xlrd 

Alternate option for Word
1. pip install textract - for both docx and doc
2. brew install antiword - for doc (didn't use* for this project)

For Mac users: Install Homebrew by

/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"