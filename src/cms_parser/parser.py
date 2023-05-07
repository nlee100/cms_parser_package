import os
import camelot
import pandas as pd
import matplotlib.pyplot as plt


class CMSParser:
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
        """
        Read data from given url and parse it.
        """
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
        for i, (table, title) in enumerate(zip(tables, titles)):
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

        for titled_table in titled_tables:
            csv_file = os.path.join(output_dir, f"{titled_table[0]}.csv")
            titled_table[1].to_csv(csv_file, index=True, mode="w")

        return tables, titles, titled_tables

    def view_table_lines(self, tables: camelot.core.TableList):
        for i, table in enumerate(tables):
            camelot.plot(table, kind="grid")
            plt.title(f"table_{i+1}")
            plt.show()

    def view_parsing_report(self, tables: camelot.core.TableList):
        for i, table in enumerate(tables):
            print(f"table_{i+1}:", table.parsing_report)

    @classmethod
    def set_table_settings(
        cls,
        flavor: str = "stream",
        line_scale: int = 45,
        split_text: bool = True,
        strip_text: str = "\n",
        backend: str = "ghostscript",
    ):
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
        cls.table_settings["flavor"] = flavor
        cls.table_settings["edge_tol"] = edge_tol
        cls.table_settings["split_text"] = split_text
        cls.table_settings["strip_text"] = strip_text
        cls.table_settings["backend"] = backend
        cls.table_settings["table_areas"] = table_areas
