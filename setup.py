from setuptools import setup, find_namespace_packages

with open("README.md", "r") as readme:
    long_desc = readme.read()

setup(
    name="valaw",
    version="0.0.4",
    author="Jet612",
    description="An asynchronous API wrapper for VALORANT's API",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/Jet612/valaw",
    project_urls={
        "Documentation": "https://valaw.readthedocs.io",
        "Issue Tracker": "https://github.com/Jet612/valaw/issues",
        "Chat/Support": "https://discord.gg/mVXpvunBbF",
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers"
    ],
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
                    'aiohttp==3.8.3',
                    'setuptools==67.6.0'
                    ]
)