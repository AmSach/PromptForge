from setuptools import setup, find_packages

setup(
    name="promptforge",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "promptforge=promptforge.cli:main",
        ]
    },
    author="Aman Sachan",
    author_email="amansachan92905@gmail.com",
    description="Version control for LLM prompts",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    python_requires=">=3.8",
)
