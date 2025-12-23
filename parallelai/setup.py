from setuptools import setup, find_packages

setup(
    name="parallelai",
    version="1.0.0",
    description="Multi-LLM Security Analysis Framework",
    author="ParallelAI Research",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.0.0",
        "requests>=2.28.0",
        "python-dotenv>=0.19.0",
        "colorama>=0.4.4",
    ],
    entry_points={
        "console_scripts": [
            "parallelai=parallelai.cli.main:cli",
        ],
    },
    python_requires=">=3.8",
)
