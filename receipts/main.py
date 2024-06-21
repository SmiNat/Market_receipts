import os

from receipts import excel_style
from receipts.excel_formatter import ExcelFormatter
from receipts.receipts import Invoices

invoice_file_path = (
    "receipts/receipts_data/example.csv"  # change desired data file path
)
invoice_excel_path = (
    "receipts/receipts_data/2024_04.xlsx"  # change excel filename or directory
)

invoice_data = Invoices(invoice_file_path)
excel_file = invoice_data.convert_invoice_report_to_excel(invoice_excel_path)


# Comment to run the file (from main diretory): python -m receipts.main

# Basic data
print("\nGiven csv data: \n", invoice_data.original_dataframe().head(), "\n")
# print(invoice_data.original_dataframe().info())

# Full daily statistics
print(
    "\nFull daily statistics from selected file: \n",
    invoice_data.generate_invoice_report().head(),
)

# Selected daily statistics
print(
    "\nSelected daily statistics from selected file: \n",
    invoice_data.generate_invoice_report_short().head(),
)

# Excel file
if os.path.exists(invoice_excel_path):
    print("\nExcel file created in given directory.")
else:
    print(
        "There was a problem with excel file. Contact controlling unit for more information."
    )


# Changing excel formatting (can be skipped or comment)

excel_file = ExcelFormatter(invoice_excel_path)

# Changing columns width
excel_file.column_width_adjustment("Dictionary")
excel_file.column_width_adjustment("Final_Report")

# First row (header) formatting
excel_file.sheet_formatter(
    "Final_Report",
    min_row=1,
    max_row=1,
    font=excel_style.RECEIPT_HEADER_FONT,
    alignment=excel_style.RECEIPT_REPORT_HEADER_ALIGNMENT,
    border=excel_style.RECEIPT_THIN_BORDER,
    fill=excel_style.RECEIPT_REPORT_HEADER_FILL,
)
excel_file.sheet_formatter(
    "Dictionary",
    min_row=1,
    max_row=1,
    font=excel_style.RECEIPT_HEADER_FONT,
    alignment=excel_style.RECEIPT_DICT_HEADER_ALIGNMENT_DICT,
    border=excel_style.RECEIPT_THIN_BORDER,
    fill=excel_style.RECEIPT_REPORT_HEADER_FILL,
)

# Cells formatting
excel_file.sheet_formatter(
    "Final_Report",
    min_row=2,
    max_row="max",
    min_col=1,
    max_col="max",
    border=excel_style.RECEIPT_THIN_BORDER,
    fill=excel_style.RECEIPT_REPORT_ROW_FILL,
)

# First column (date) formatting
excel_file.sheet_formatter(
    "Final_Report",
    min_row=2,
    max_row="max",
    min_col=1,
    max_col=1,
    border=excel_style.RECEIPT_THIN_BORDER,
    fill=excel_style.RECEIPT_REPORT_HEADER_FILL,
)

# Data type formatter
excel_file.column_type_formatter(
    "Final_Report", column_formatter=excel_style.RECEIPT_REPORT_TYPE_FORMATTER
)
