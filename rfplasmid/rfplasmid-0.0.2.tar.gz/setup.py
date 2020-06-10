from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='rfplasmid',
    version='0.0.2',
    scripts=['rfplasmid.py'] ,
    author="Aldert Zomer",
    author_email="A.L.Zomer@uu.nl",
    description="RFPlasmid Predicting plasmid contigs",
    packages=find_packages(),
	package_data = {'': ['Bacillus.rfo', 'Bacteria.rfo', 'Borrelia.rfo', 'Burkholderia.rfo', 'Campylobacter.rfo', 'classification.R', 'Clostridium.rfo', 'Corynebacterium.rfo', 'Cyanothece.rfo', 'Enterobacteriaceae.rfo', 'Enterococcus.rfo', 'getdb.sh', 'kmer.txt', 'Lactobacillus.rfo', 'Lactococcus.rfo', 'Listeria.rfo', 'plasmiddb_cge.dmnd', 'plasmiddb_cge.faa', 'Pseudomonas.rfo', 'Rhizobium.rfo', 'specieslist.txt', 'Staphylococcus.rfo', 'Streptomyces.rfo', 'training.R', 'Vibrio.rfo']},
    data_files=[('.', ['Bacillus.rfo', 'Bacteria.rfo', 'Borrelia.rfo', 'Burkholderia.rfo', 'Campylobacter.rfo', 'classification.R', 'Clostridium.rfo', 'Corynebacterium.rfo', 'Cyanothece.rfo', 'Enterobacteriaceae.rfo', 'Enterococcus.rfo', 'getdb.sh', 'kmer.txt', 'Lactobacillus.rfo', 'Lactococcus.rfo', 'Listeria.rfo', 'plasmiddb_cge.dmnd', 'plasmiddb_cge.faa', 'Pseudomonas.rfo', 'Rhizobium.rfo', 'specieslist.txt', 'Staphylococcus.rfo', 'Streptomyces.rfo', 'training.R', 'Vibrio.rfo'])],
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aldertzomer/RFPlasmid",
    install_requires=['numpy', 'matplotlib', 'pysam', 'checkm-genome'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)