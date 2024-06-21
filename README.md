# Invoice manager for extracting data from csv file.

Desirable csv file structure requires columns:
- "BON_DAT",
- "LOYALITY_CUSTOMER_ID",
- "RECEIPT_ID",
- "RECEIPT_VALUE",

## Project setup

File receipts/main.py demonstrates how Invoice class and ExcelFormatter class
works on given dane_Python.csv file.

### To run the code you must first:

1) Downolad GitHub repository or unpack zip file.

2) Install necessary packages from requirements.txt file

    (For conducting tests you must also install packages from requirements_dev.txt file)

3) Inside main folder (in zip file named Supermarket) run commend:

    python -m receipts.main

    (For tests run commend: pytest)


### To change the csv file you must first:

1) Upload file to desirable directory
2) Change file directory for 'invoice_file_path' variable in receipts/main.py file
3) [Optionaly] Change excel file name and directory by changing
    'invoice_excel_path' variable in receipts/main.py file
4) Run the file again (commend: python -m receipts.main)


# Required
Python 3.10