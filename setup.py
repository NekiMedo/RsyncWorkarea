import setuptools

# run this as: python(3)  setup.py  bdist_wheel
#          +   pip install <wheel>

with open( 'README.org', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='brsync',
    version='0.0.1',
    scripts=['brsync.py',] ,
    author='Neki Medo',
    author_email="bb.mail@exemail.com.au",
    description="Copy the directory contents to a remote location",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NekiMedo/RsyncWorkarea",
    packages=setuptools.find_packages(),
    classifiers=[ "Programming Language :: Python :: 3",
                  "License :: OSI Approved :: GPL 3",
                  "Operating System :: OS Independent",
                ],
)
