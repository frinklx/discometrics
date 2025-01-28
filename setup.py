from setuptools import setup, find_packages

setup(
    name="dmetrics",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests==2.31.0",
        "typer==0.9.0",
        "rich==13.7.0",
        "python-dotenv==1.0.0",
        "plotext==5.2.8",
        "PyGithub==2.1.1",
        "pandas==2.1.4",
        "termcolor==2.3.0",
    ],
    entry_points={
        "console_scripts": [
            "dmetrics=dmetrics.cli:app",
        ],
    },
) 