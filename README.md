# batoid-phylogeny-blog

Code repository for phylogenetics tutorial on reconstructing batoid phylogeny with IQ-Tree. 

> [!NOTE]  
> Purely for educational purposes, not an authoritative source about batoid evolution or phylogenetics.

## Setting environment:
```shell
conda env create -f environment.yml -y && conda activate naylor-batoidea
# You may wish to specify an output directory as an env variable then use in script.
# IQ-Tree generates many files in the same directory it is run in.
```
## Running scripts

```shell
python3 scripts/prep_data.py -i data/Gene_table.csv -o output/PARTITION.nex
```

## Run IQ-Tree

```shell
iqtree2 -p PARTITION.nex
```

Output tree is in PARTITION.nex.iqtree 

## Links
- My Medium [blog](https://medium.com/@ch1ru/phylogenetics-tutorial-reconstructing-batoid-phylogeny-from-dna-sequences-7b33fe70ee1b)
- Original [paper](https://www.sciencedirect.com/science/article/abs/pii/S1055790311005252) by Naylor et al
- IQ-Tree [documentation](IQ-Tree documentation at http://www.iqtree.org/doc/)

