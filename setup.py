import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="skillsnetwork",
    version="0.20.7-rc1",
    author="Rui Zhu",
    author_email="Rui.Zhu@ibm.com",
    description="SkillsNetwork Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
