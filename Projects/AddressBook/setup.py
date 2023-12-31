from setuptools import setup

setup(
    name="alfred",
    version="1.0.0",
    description="CLI Bot assistant. Package for adding data to address book, read/update/delete it, adding notes etc.",
    url="",
    author="'Gotham Devs': Katarzyna Drajok, Katarzyna Czempiel, Rafał Pietras, Dawid Radzimski, Adrian Karwat",
    author_email="katarzyna.drajok@gmail.com; katarzyna.czempiel@gmail.com; rafal.radx@gmail.com; dawid.radzimski@gmail.com; adr.karwat@gmail.com",
    readme="README.md",
    license="MIT",
    package_data={"package_c-stubs": ["__init__.pyi", "lib.pyi"]},
    packages=["alfred", "package_c-stubs"],
    requires=["thefuzz"],
    entry_points={"console_scripts": ["alfred=addressbook:Main"]},
)