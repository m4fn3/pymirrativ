import setuptools

setuptools.setup(
    name="pymirrativ",
    version="1.0.0",
    install_requires=open("requirements.txt").read().splitlines(),
    author="mafu",
    author_email="mafusukee@gmail.com",
    description="An unofficial api wrapper of internal mirrativ api",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/m4fn3/pymirrativ",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)