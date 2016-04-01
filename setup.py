import os
from setuptools import setup, find_packages

def read_file(path):
    with open(os.path.join(os.path.dirname(__file__), path), "r") as fobj:
        return fobj.read()

setup(
    name="videosequence",
    version="1.0.0",
    packages=find_packages(),

    install_requires=["future", "pillow"],

    author="Rich Wareham",
    author_email="rich.videosequence@richwareham.com",
    url="https://github.com/rjw57/videosequence",
    description="Read from and seek into video files as if they were Python "
                "sequences of PIL.Image-s.",
    long_description=read_file("README.rst"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Topic :: Multimedia :: Video",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    license="MIT",
)
