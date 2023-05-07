import src.cms_parser.parser as CMSParser 
import camelot

my_CMSParser = CMSParser.CMSParser(
    "https://www.cms.gov/files/document/2024-advance-notice-pdf.pdf", 126, 137
)

def test_table_settings_is_dict():
    assert isinstance(my_CMSParser.table_settings, dict)

def test_title_settings_is_dict():
    assert isinstance(my_CMSParser.title_settings, dict)

def test_start_page_is_int():
    ast = my_CMSParser.start_page
    assert isinstance(ast, int) and ast == 126  # 126 is the start page number for the example PDF file.   

def test_end_page_is_int():
    ast = my_CMSParser.end_page
    assert isinstance(ast, int) and ast == 137  # 137 is the end page number for the example PDF file.

def test_url_is_string():
    assert isinstance(my_CMSParser.url, str)

def test_tables_is_TableList():
    tables, titles, titled_tables = my_CMSParser.extract_data()
    assert isinstance(tables, camelot.core.TableList)

def test_titles_is_TableList():
    tables, titles, titled_tables = my_CMSParser.extract_data()
    assert isinstance(titles, camelot.core.TableList)

def test_titled_tables_is_list():
    tables, titles, titled_tables = my_CMSParser.extract_data()
    assert isinstance(titled_tables, list)