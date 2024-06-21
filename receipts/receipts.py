"""A Python script for extracting and processing data from .csv invoice file
and returning outcome in Excel file.
A script will work on csv files with data included:
    - BON_DAT,
    - LOYALITY_CUSTOMER_ID,
    - RECEIPT_ID,
    - RECEIPT_VALUE.
Any other data layout in csv file may cause script errors or unexpected outcomes.
For adjusting Python script to other csv file structure contact the controlling office manager.
"""

import os

import pandas as pd
from pandas import DataFrame

from .exceptions import FileStructureError
from .utils import check_if_file_exists

desired_width = 320
pd.set_option("display.width", desired_width)
pd.set_option("display.max_columns", 15)


class Invoices:
    """Convert csv file with invoice data into dataframe and extract daily data
    in dataframe or excel file."""

    REQUIRED_FILE_HEADERS = [
        "BON_DAT",
        "LOYALITY_CUSTOMER_ID",
        "RECEIPT_ID",
        "RECEIPT_VALUE",
    ]
    RECEIPT_HEADERS = {
        "Date": "Data",
        "No_of_Receipt": "Liczba paragonów",
        "NoR_NLC": "Liczba paragonów klientów nielojalnościowych",
        "NoR_LC": "Liczba paragonów klientów nielojalnościowych",
        "Turnover": "Obrót",
        "Turnover_NLC": "Obrót klientów nielojalnościowych",
        "Turnover_LC": "Obrót klientów lojalnościowych",
        "Turnover_share_LC": "Udział klientów lojalnościowych w obrocie",
        "Avg_Receipt_Value": "Średnia wartość paragonu",
        "ARV_NLC": "Średnia wartość paragonu klienta nielojalnościowego",
        "ARV_LC": "Średnia wartość paragonu klienta lojalnościowego",
    }
    FINAL_REPORT_HEADERS = [
        "Date",
        "No_of_Receipt",
        "Turnover_share_LC",
        "Avg_Receipt_Value",
        "ARV_NLC",
        "ARV_LC",
    ]

    def __init__(self, file_path: str) -> None:
        check_if_file_exists(file_path)
        self.file_path = file_path

    def __str__(self) -> str:
        return f"Invoices for the file: '{os.path.basename(self.file_path)}'"

    def check_file_structure(self) -> None:
        """Validates if csv file has all required data."""
        file_headers = list(pd.read_csv(self.file_path, nrows=1).columns)
        if sorted(file_headers) != sorted(self.REQUIRED_FILE_HEADERS):
            raise FileStructureError(
                "The file structure is invalid.",
                "Required headers: %s" % self.REQUIRED_FILE_HEADERS,
            )

    def original_dataframe(self) -> DataFrame:
        """Converts csv file into Pandas DataFrame sorted by BON_DAT column."""
        # Verifying csv file
        self.check_file_structure()
        # Creating a DataFrame with data load form csv file
        df = pd.read_csv(self.file_path, delimiter=",")
        # Converting "BON_DAT" to datetime and sorting data by "BON_DAT" column
        df["BON_DAT"] = pd.to_datetime(df["BON_DAT"])
        df.sort_values(by="BON_DAT", inplace=True)
        return df

    def generate_invoice_report(self) -> DataFrame:
        """Generates full invoice report with data grouped by date."""
        # Creating a desired DataFrame
        df = self.original_dataframe().copy()
        # Converting BON_DAT to datetime
        df["BON_DAT"] = pd.to_datetime(df["BON_DAT"])
        # Grouping by date
        grouped = df.groupby("BON_DAT")

        data = []

        for date, group in grouped:
            no_of_receipts = group["RECEIPT_ID"].count()
            turnover = group["RECEIPT_VALUE"].sum()
            avg_receipt_value = round(group["RECEIPT_VALUE"].mean(), 2)

            lc_group = group.dropna(subset=["LOYALITY_CUSTOMER_ID"])
            nlc_group = group[group["LOYALITY_CUSTOMER_ID"].isna()]

            no_of_receipts_lc = lc_group["RECEIPT_ID"].count()
            no_of_receipts_nlc = nlc_group["RECEIPT_ID"].count()
            turnover_lc = lc_group["RECEIPT_VALUE"].sum()
            turnover_nlc = nlc_group["RECEIPT_VALUE"].sum()
            avg_receipt_value_lc = round(
                lc_group["RECEIPT_VALUE"].mean() if not lc_group.empty else 0, 2
            )
            avg_receipt_value_nlc = round(
                nlc_group["RECEIPT_VALUE"].mean() if not nlc_group.empty else 0, 2
            )
            turnover_share_lc = round(turnover_lc / turnover if turnover != 0 else 0, 2)

            data.append(
                {
                    "Date": date.strftime("%Y-%m-%d"),
                    "No_of_Receipt": no_of_receipts,
                    "NoR_NLC": no_of_receipts_nlc,
                    "NoR_LC": no_of_receipts_lc,
                    "Turnover": turnover,
                    "Turnover_NLC": turnover_nlc,
                    "Turnover_LC": turnover_lc,
                    "Turnover_share_LC": turnover_share_lc,
                    "Avg_Receipt_Value": avg_receipt_value,
                    "ARV_NLC": avg_receipt_value_nlc,
                    "ARV_LC": avg_receipt_value_lc,
                }
            )

        # Creating the DataFrame
        report = pd.DataFrame(data)
        return report

    def generate_invoice_report_short(self):
        """Generates short report from original DataFrame data."""
        report = self.generate_invoice_report()
        final_report = report[self.FINAL_REPORT_HEADERS].copy()
        return final_report

    def convert_invoice_report_to_excel(
        self,
        excel_path: str,
        full_report: bool = False,
    ) -> None:
        """Converts report into excel file. If no report provided, converts
        report with daily statistics short data."""
        with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
            # Write dictionary to the first sheet
            dict_df = pd.DataFrame(
                list(self.RECEIPT_HEADERS.items()), columns=["Nazwa", "Znaczenie"]
            )
            dict_df.to_excel(writer, sheet_name="Dictionary", index=False)

            # Write report to the second sheet
            report = (
                self.generate_invoice_report_short()
                if not full_report
                else self.generate_invoice_report()
            )
            report.to_excel(writer, sheet_name="Final_Report", index=False)
