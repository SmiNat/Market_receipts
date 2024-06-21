from openpyxl.styles import Side, numbers

# Basic receipt sheet style
RECEIPT_HEADER_FONT = {"bold": True}
RECEIPT_DICT_HEADER_ALIGNMENT_DICT = {"horizontal": "left"}
RECEIPT_REPORT_HEADER_ALIGNMENT = {"horizontal": "center"}
RECEIPT_THIN_BORDER = {
    "left": Side(style="thin"),
    "right": Side(style="thin"),
    "top": Side(style="thin"),
    "bottom": Side(style="thin"),
}
RECEIPT_REPORT_HEADER_FILL = {
    "start_color": "C2E44E",
    "end_color": "C2E44E",
    "fill_type": "solid",
}
RECEIPT_REPORT_ROW_FILL = {
    "start_color": "ECFEC0",
    "end_color": "ECFEC0",
    "fill_type": "solid",
}
RECEIPT_REPORT_FIRST_COLUMN_FILL = {
    "start_color": "C2E44E",
    "end_color": "C2E44E",
    "fill_type": "solid",
}
RECEIPT_REPORT_TYPE_FORMATTER = {
    "A": numbers.FORMAT_DATE_YYYYMMDD2,  # Date column
    "B": "0",  # No_of_Receipt column
    "other": "0.00",  # Float columns
}
