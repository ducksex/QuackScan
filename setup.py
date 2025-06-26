from setuptools import setup, find_packages

setup(
    name='quackscan',
    version='1.0.0',
    author='ducksex',
    packages=find_packages(exclude=['tests', 'wordlists', 'data']),
    include_package_data=True,
    install_requires=[
        'aiohttp',
        'dnspython',
        'httpx',
        'colorama'
    ],
    entry_points={
        'console_scripts': [
            'quackscan = quackscan.__main__:main'
        ]
    },
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Security',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)
