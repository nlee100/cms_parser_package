import os
import camelot
import pandas as pd
import matplotlib.pyplot as plt


class CMSParser:

    """CMSParser class for extracting tables from a given PDF.

    Attributes:
        url (str): Link to webpage PDF for text extraction.
        start_page (int, optional): Page number of PDF to start text extraction.
        end_page (int, optional): Page number of PDF to end text extraction.

    """

    table_settings = {
        "flavor": "lattice",
        "line_scale": 45,
        "split_text": True,
        "strip_text": "\n",
        "backend": "ghostscript",
    }
    title_settings = {
        "flavor": "stream",
        "edge_tol": 500,
        "split_text": True,
        "strip_text": "\n",
        "backend": "ghostscript",
        "table_areas": ["0,842,595,0"],
    }

    def __init__(self, url: str, start_page: int = None, end_page: int = None):
        self.url = url
        self.start_page = start_page
        self.end_page = end_page

    def extract_data(self):
        """Read data from the given url and parse it into respective .csv files."""
        output_dir = "src/cms_parser/output"
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        if self.start_page is not None and self.end_page is not None:
            tables = camelot.read_pdf(
                self.url,
                pages=f"{self.start_page}-{self.end_page}",
                **CMSParser.table_settings,
            )
            titles = camelot.read_pdf(
                self.url,
                pages=f"{self.start_page}-{self.end_page}",
                **CMSParser.title_settings,
            )
        else:
            tables = camelot.read_pdf(self.url, pages="all", **CMSParser.table_settings)
            titles = camelot.read_pdf(self.url, pages="all", **CMSParser.title_settings)

        # zip tables and titles together based on same index for respective labeling.
        titled_tables = []
        for table, title in zip(tables, titles):
            title_stripped = title.df.iat[1, 0].split(".")[0].replace(" ", "")
            if title_stripped.startswith("Table"):
                titled_tables.append((title_stripped, table))
            else:
                # keep column names if starts with table and add new entry. otherwise, delete (remove redundance in column names). add to previous table if exists. otherwise, add new entry.
                table.df = table.df.drop(index=0)
                if titled_tables[-1][1] is None:
                    titled_tables.append((None, table))
                else:
                    titled_tables[-1][1].df = pd.concat(
                        [titled_tables[-1][1].df, table.df], axis=0, ignore_index=True
                    )
        # write each table to a .csv file labeled with the appropriate title.
        for titled_table in titled_tables:
            csv_file = os.path.join(output_dir, f"{titled_table[0]}.csv")
            titled_table[1].to_csv(csv_file, index=True, mode="w")

        return tables, titles, titled_tables

    # helpful for debugging table parsing errors and increasing accuracy.
    def view_table_lines(self, tables: camelot.core.TableList):
        """Plot the parsing of table lines/boundaries for each particular PDF page."""
        for table in tables:
            camelot.plot(table, kind="grid")
            page_num = table.parsing_report["page"]
            plt.title(f"page {page_num}")
            plt.show()

    def view_parsing_report(self, tables: camelot.core.TableList):
        """Print the parsing report for each particular PDF page, including the accuracy of text extraction, percentage of whitespace in table, table number, and page number."""
        [print(f"table_{i+1}:", table.parsing_report) for i, table in enumerate(tables)]

    @classmethod
    def set_table_settings(
        cls,
        flavor: str = "stream",
        line_scale: int = 45,
        split_text: bool = True,
        strip_text: str = "\n",
        backend: str = "ghostscript",
    ):
        """Set table settings."""
        cls.table_settings["flavor"] = flavor
        cls.table_settings["line_scale"] = (line_scale,)
        cls.table_settings["split_text"] = split_text
        cls.table_settings["strip_text"] = strip_text
        cls.table_settings["backend"] = backend

    @classmethod
    def set_title_settings(
        cls,
        flavor: str = "stream",
        edge_tol: int = 500,
        split_text: bool = True,
        strip_text: str = "\n",
        backend: str = "ghostscript",
        table_areas: list = ["0,842,595,0"],
    ):
        """Set title settings."""
        cls.title_settings["flavor"] = flavor
        cls.title_settings["edge_tol"] = edge_tol
        cls.title_settings["split_text"] = split_text
        cls.title_settings["strip_text"] = strip_text
        cls.title_settings["backend"] = backend
        cls.title_settings["table_areas"] = table_areas
