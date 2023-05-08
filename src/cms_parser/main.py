from argparse import ArgumentParser

from .parser import CMSParser

my_parser = ArgumentParser(description="Process user input.")
my_parser.add_argument("url", help="URL to the PDF file", type=str)
my_parser.add_argument(
    "--start_page", required=False, help="Start page number", type=int
)
my_parser.add_argument("--end_page", required=False, help="End page number", type=int)


def main():
    """Read in user input from the command line and call the CMSParser."""
    args = my_parser.parse_args()
    if bool(args.start_page) ^ bool(args.end_page):
        my_parser.error("--start_page and --end_page must both be given.")
    my_cmsparser = CMSParser(
        url=args.url, start_page=args.start_page, end_page=args.end_page
    )
    my_cmsparser.extract_data()
