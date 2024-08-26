from setuptools import setup, find_namespace_packages

with open("README.md", "r") as readme:
    long_desc = readme.read()

url = "https://github.com/Jet612/valaw"

setup(
    name="valaw",
    version="0.1.05",
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
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
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
                    'aiohttp==3.10.5',
                    'dataclass_wizard==0.22.3',
                    'setuptools==70.3.0'
                    ]
)