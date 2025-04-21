from setuptools import setup, find_namespace_packages

with open("README.md", "r") as readme:
    long_desc = readme.read()

url = "https://github.com/Jet612/valaw"

setup(
    name="valaw",
    version="0.1.07",
    author="Jet612",
    description="An asynchronous API wrapper for VALORANT's API",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/Jet612/valaw",
    project_urls={
        "Source": url,
        "Documentation": "https://valaw.readthedocs.io",
        "Issue Tracker": url + "/issues",
        "Chat/Support": "https://discord.gg/mVXpvunBbF",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
    ],
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
                    'dataclass_wizard==0.23.0',
                    'aiohttp==3.10.10',
                    'setuptools==79.0.0'
                    ]
)
