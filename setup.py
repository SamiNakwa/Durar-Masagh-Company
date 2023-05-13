from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in durar_masagh_company/__init__.py
from durar_masagh_company import __version__ as version

setup(
	name="durar_masagh_company",
	version=version,
	description="This is Custom app belongs to Durar Masagh Company",
	author="Samiulla Nakwa",
	author_email="info@dmgroupksa.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
