import pytest
import camelot
import src.cms_parser.parser as CMSParser


@pytest.fixture
def cms_parser():
    """Returns a CMSParser instance."""
    return CMSParser.CMSParser(
        "https://www.cms.gov/files/document/2024-advance-notice-pdf.pdf", 126, 137
    )


def test_table_settings_is_dict(cms_parser):
    assert isinstance(cms_parser.table_settings, dict)


def test_title_settings_is_dict(cms_parser):
    assert isinstance(cms_parser.title_settings, dict)


def test_start_page_is_int(cms_parser):
    ast = cms_parser.start_page
    assert isinstance(ast, int) and ast == 126


def test_end_page_is_int(cms_parser):
    ast = cms_parser.end_page
    assert isinstance(ast, int) and ast == 137


def test_url_is_string(cms_parser):
    assert isinstance(cms_parser.url, str)


def test_tables_is_TableList(cms_parser):
    tables, titles, titled_tables = cms_parser.extract_data()
    assert isinstance(tables, camelot.core.TableList)


def test_titles_is_TableList(cms_parser):
    tables, titles, titled_tables = cms_parser.extract_data()
    assert isinstance(titles, camelot.core.TableList)


def test_titled_tables_is_list(cms_parser):
    tables, titles, titled_tables = cms_parser.extract_data()
    assert isinstance(titled_tables, list)
