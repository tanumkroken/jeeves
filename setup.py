from setuptools import setup, find_packages

setup(
    name='jeeves',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask', 'spacy',
    ],
    url='',
    license='MIT',
    author='Ole Chr. Astrup',
    author_email='tanumkroken@astrup.info',
    description='Ask Jeeves - A natural language processor'
)

