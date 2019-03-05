from distutils.core import setup

setup(
    # Application name:
    name="Automato",

    # Version number (initial):
    version="0.0.1",

    # Application author details:
    author="Henrique A Conzatti",
    author_email="henrique@conza.com.br",

    # Packages
    packages=["app"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    # url="",

    #
    # license="LICENSE.txt",
    description="Modulo facilita configurações de devices na rede.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[],
)
