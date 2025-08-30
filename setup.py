from setuptools import setup, find_packages

setup(
    name="daddy-bank",
    version="0.1.0",
    description="Bank & CC application with T-mobile integration",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "python-dotenv>=0.19.0",
    ],
    python_requires=">=3.7",
)