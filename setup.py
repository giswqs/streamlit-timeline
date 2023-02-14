import setuptools

with open("README.md") as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name="streamlit-vis-timeline",
    version="0.2.1",
    author="Qiusheng Wu",
    author_email="giswqs@gmail.com",
    description="Streamlit component for rendering vis.js timeline",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/giswqs/streamlit-timeline",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "streamlit >= 0.63",
    ],
)
