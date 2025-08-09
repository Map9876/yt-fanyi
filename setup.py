from setuptools import setup, find_packages

setup(
    name="yt-fanyi",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'pytubefix',
        'requests',
        'tqdm',
    ],
    entry_points={
        'console_scripts': [
            'yt-fanyi=yt_fanyi.cli:main',
        ],
    },
    python_requires='>=3.7',
)
