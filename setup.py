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
    python_requires=">=3.7",
    author="Your Name",
    description="A beautiful dark-mode GitHub analytics CLI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dmetrics",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 