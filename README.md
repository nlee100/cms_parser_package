# cms_parser

**A packaged Python parser to extract information from a webpage PDF into a .csv file. The settings of this package work best with the [2024 Advance Notice for the Medicare Advantage Capitation Rates and Part C and Part D Payment Policies](https://www.cms.gov/files/document/2024-advance-notice-pdf.pdf) released by CMS and can be adjusted accordingly for a given use case (see [Usage](#usage)).**

## Installation

Requires Python 3.6 or higher. Anaconda recommended.

1. Clone repo. 
```bash
$ git clone https://github.com/nlee100/cms_parser_package.git
```
2. Create and activate a conda virtual environment. Ensure you deactivate any other virtual environment you may have activated (e.g., `base`).
```bash
# create virtual environment named "myenv" (or another name of preference).
$ conda create --name myenv 
$ conda activate myenv 
```
3. Install the package. Ensure you're using the right pip version (i.e., the one from the virtual environment you just created) by calling `which pip`.
```bash
(myenv) $ pip install . # assumes directory is the current working directory. 
```
4. Call the parser. All outputs will be saved in the `cms_parser/output` directory.
```bash
(my_env) $ cms_parser [-h] [--start_page START_PAGE] [--end_page END_PAGE] url
```

## Usage
Examples of how the package can be used.

Run package with the required argument (i.e., webpage link to PDF) and optional arguments (i.e., start and stop page numbers).
```bash
(my_env) $ cms_parser "https://www.cms.gov/files/document/2024-advance-notice-pdf.pdf" --start_page 126 --end_page 137
```

Adjust default settings determining how PDF is parsed from the given webpage link, and view the parsing details of the PDF per parsed page. For more information on possible settings, refer to the `camelot` documentation [here](https://camelot-py.readthedocs.io/en/master/user/advanced.html#).
```py
from src.cms_parser.parser import CMSParser

CMSParser.set_table_settings(line_scale=15, split_text=False)

my_CMSParser = CMSParser("https://www.cms.gov/files/document/2024-advance-notice-pdf.pdf", 126, 137)
tables, titles, titled_tables = my_CMSParser.extract_data()
my_CMSParser.view_parsing_report(tables)
my_CMSParser.view_table_lines(tables)
```

## Support
Feel free to fork! If you find a bug or have a feature suggestions, please submit a new issue under the [Issues](https://github.com/nlee100/cms_parser_package/issues).

## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

cms_parser is available under the MIT License.