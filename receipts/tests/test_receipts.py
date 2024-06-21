import os

import pandas as pd
import pandas.testing as pdt
import pytest

from ..exceptions import FileStructureError
from ..receipts import Invoices


def test_str_method(test_file):
    invoice = Invoices(test_file)
    assert invoice.__str__() == "Invoices for the file: '2024-04.csv'"


def test_init_with_invalid_file_path():
    with pytest.raises(FileNotFoundError):
        invoice = Invoices("some_file_path")


def test_check_file_structure_ok(test_file):
    invoice = Invoices(test_file)
    assert invoice.check_file_structure() is None


def test_check_file_structure_invalid_structure(test_file_invalid):
    invoice = Invoices(test_file_invalid)
    with pytest.raises(FileStructureError) as exc_info:
        invoice.check_file_structure()
    assert "The file structure is invalid" in str(exc_info.value)
    assert "Required headers:" in str(exc_info.value)


def test_original_dataframe_ok(test_file):
    invoice = Invoices(test_file)
    actual_df = invoice.original_dataframe()

    exp_df = pd.read_csv(test_file)
    exp_df["BON_DAT"] = pd.to_datetime(exp_df["BON_DAT"])
    exp_df.sort_values("BON_DAT", inplace=True)

    pdt.assert_frame_equal(actual_df, exp_df)


def test_original_dataframe_diff(test_file):
    invoice = Invoices(test_file)
    exp_df = pd.read_csv(test_file)
    exp_df.sort_values("BON_DAT", inplace=True)

    # Changing expecting outcome to differ from actual one (breaking the test)
    exp_df.iloc[0, exp_df.columns.get_loc("LOYALITY_CUSTOMER_ID")] = "DIFFERENT_VALUE"

    actual_df = invoice.original_dataframe()
    with pytest.raises(AssertionError):
        pdt.assert_frame_equal(actual_df, exp_df)


def test_generate_invoice_report_ok(test_file):
    invoice = Invoices(test_file)
    actual_df = invoice.generate_invoice_report()
    exp_df = pd.read_excel(
        "receipts/tests/test_data/solutions.xlsx", sheet_name="2024-04_full"
    )
    # Ensure the expected data has the same formatting of "Date" column as actual data
    exp_df["Date"] = pd.to_datetime(exp_df["Date"]).dt.strftime("%Y-%m-%d")

    pdt.assert_frame_equal(actual_df, exp_df, check_dtype=False)


def test_generate_invoice_report_short_ok(test_file):
    invoice = Invoices(test_file)
    actual_df = invoice.generate_invoice_report_short()
    exp_df = pd.read_excel(
        "receipts/tests/test_data/solutions.xlsx", sheet_name="2024-04_full"
    )
    exp_df.drop(
        columns=["Turnover_LC", "Turnover_NLC", "Turnover", "NoR_LC", "NoR_NLC"],
        inplace=True,
    )
    # Ensure the expected data has the same formatting of "Date" column as actual data
    exp_df["Date"] = pd.to_datetime(exp_df["Date"]).dt.strftime("%Y-%m-%d")

    pdt.assert_frame_equal(actual_df, exp_df, check_dtype=False)


def test_convert_invoice_report_to_excel_file_exist(test_file):
    invoice = Invoices(test_file)
    new_file_path = "receipts/tests/temp_file.xlsx"
    invoice.convert_invoice_report_to_excel("receipts/tests/temp_file.xlsx")
    assert os.path.exists(new_file_path) is True

    os.remove(new_file_path)
    assert os.path.exists(new_file_path) is False


def test_convert_invoice_report_to_excel_sheet_with_final_report(test_file):
    invoice = Invoices(test_file)
    new_file_path = "receipts/tests/temp_file.xlsx"

    exp_df = pd.read_excel(
        "receipts/tests/test_data/solutions.xlsx", sheet_name="2024-04_full"
    )
    exp_df.drop(
        columns=["Turnover_LC", "Turnover_NLC", "Turnover", "NoR_LC", "NoR_NLC"],
        inplace=True,
    )
    # Ensure the expected data has the same formatting of "Date" column as actual data
    exp_df["Date"] = pd.to_datetime(exp_df["Date"]).dt.strftime("%Y-%m-%d")

    invoice.convert_invoice_report_to_excel(new_file_path)
    created_excel = pd.read_excel(new_file_path, sheet_name="Final_Report")

    pdt.assert_frame_equal(created_excel, exp_df, check_dtype=False)

    os.remove(new_file_path)
    assert os.path.exists(new_file_path) is False


def test_convert_invoice_report_to_excel_sheet_with_dictionary(test_file):
    invoice = Invoices(test_file)
    new_file_path = "receipts/tests/temp_file.xlsx"
    invoice.convert_invoice_report_to_excel(new_file_path)

    data = [(k, v) for k, v in invoice.RECEIPT_HEADERS.items()]
    exp_df = pd.DataFrame(data=data, columns=["Nazwa", "Znaczenie"])

    created_excel = pd.read_excel(new_file_path, sheet_name="Dictionary")

    pdt.assert_frame_equal(created_excel, exp_df, check_dtype=False)

    os.remove(new_file_path)
    assert os.path.exists(new_file_path) is False
