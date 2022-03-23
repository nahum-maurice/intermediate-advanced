from enum import IntEnum
from typing import Tuple, List

# Nucleotide is of type IntEnum because it gives comparison operators
# such as (<, >=...)
Nucleotide : IntEnum = IntEnum('Nucleotide', ('A', 'C', 'G', 'T'))

# Types aliases 
Condon = Tuple[Nucleotide, Nucleotide, Nucleotide]
Gene = List[Condon]

gene_str : str = "ACATGCATGTAGCATCGGCATAACTGACTCGATGAGTAGCATGCATGCAT"


def string_to_gene(s: str) -> Gene:
    gene: Gene = []
    for i in range(0, len(s), 3):
        if(i+2) >= len(s):
            return gene
        # initialize condon out with three nucleotides 
        condon: Condon = (Nucleotide[s[i]], Nucleotide[s[i + 1]], Nucleotide[s[i + 2]])
        gene.append(condon)
    return gene

studied_gene : Gene = string_to_gene(gene_str)


# performs linear search
def linear_contains(gene: Gene, key_condon: Condon) -> bool:
    for condon in gene:
        if condon == key_condon:
            return True
    return False


acg: Condon = (Nucleotide.A, Nucleotide.C, Nucleotide.G)
gat: Condon = (Nucleotide.G, Nucleotide.A, Nucleotide.T)

print(linear_contains(studied_gene, acg)) # print(acg in studied_gene)
print(linear_contains(studied_gene, gat))


def binary_contains(gene: Gene, key_condon: Condon) -> bool:
    # indexes for extremes
    low: int = 0
    hight: int = len(gene) - 1

    while low <= high: #  meaning while there is still a search space
        mid: int = (low + high) // 2
        if gene[mid] < key_condon:
            low = mid + 1
        elif gene[mid] > key_condon:
            high = mid - 1
        else:
            return True
    return False



