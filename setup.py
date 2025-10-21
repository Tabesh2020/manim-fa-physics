
from setuptools import setup, find_packages

setup(
    name="manim-fa-physics",
    version="0.1.0",
    author="Tabesh Alli",
    packages=find_packages(),  # پیدا کردن خودکار پوشه manim-fa-physics
    install_requires=["manim>=0.19.0", "numpy>=1.24"],
    python_requires=">=3.10",

    description="افزونه فیزیک برای Manim (مکانیک، گرانش، اوپتیک، الکترومغناطیس، الکترواستاتیک)",
    url="https://github.com/Tabesh2020/manim-fa-physics",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Graphics",
    ],
)
