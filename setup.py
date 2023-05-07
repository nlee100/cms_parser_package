from setuptools import setup

with open("src/cms_parser/version.py") as fid:
     for line in fid:
         if line.startswith("__version__"):
             version = line.strip().split()[-1][1:-1]
             break

with open("requirements.txt") as fid:
    install_require = [l.strip() for l in fid.readlines() if l]

setup(
    name="cms_parser",
    version=version,
    description="A package for parsing CMS data",
    author="Naomi Lee",
    packages=["cms_parser"],
    package_dir={"cms_parser": "src/cms_parser"},
    install_requires=install_require,
    entry_points={
        'console_scripts': ['cms_parser=cms_parser.main:main']
    }
)