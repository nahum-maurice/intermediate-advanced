class CompressedGene:
    def __init__(self, gene: str) -> None:
        self._compress(gene)

    def _compress(self, gene: str) -> None:
        self.bit_string : int = 1  #start with a sentinel
        for nucleotide in gene.upper():
            """AAT = 0b1000011"""

            self.bit_string <<= 2  #shift left two bits
            if nucleotide == "A":
                self.bit_string |= 0b00  
            elif nucleotide == "C":
                self.bit_string |= 0b01  
            elif nucleotide == "G":
                self.bit_string |= 0b10
            elif nucleotide == "T":
                self.bit_string |= 0b11
            else:
                raise ValueError("Invalid Nucleotide: {}".format(nucleotide))
    
    def decompress(self) -> str:
        gene: str = ""
        for i in range(0, self.bit_string.bit_length() -1, 2): # - 1 to exclude sentinel
            bits: int = self.bit_string >> i & 0b11 #gets two relevant bits
            if bits == 0b00:
                gene += "A"
            elif bits == 0b01:
                gene += "C"
            elif bits == 0b10:
                gene += "G"
            elif bits == 0b11:
                gene += "T"
            else: 
                raise ValueError("Invalid bits: {}".format(bits))
        return gene[::-1]  #reverses string by slicing backward

    def __str__(self) -> str:
        """String representation for pretty printing"""
        return self.decompress() 

if __name__ == "__main__":
    from sys import getsizeof
    original : str = "AATGGCCGAATTGAGCCTGAAGTCAGTTGCAGTAGCTAGAATCATGCCTAGCTAGGATCGATCATGCATGC" * 100
    print(original)
    print("Original size: {} bytes.".format(getsizeof(original)))
    compressed : CompressedGene = CompressedGene(original)
    print("Compressed size: {} bytes.".format(getsizeof(compressed.bit_string)))
    print("Original and decompressed are the same: {}.".format(original == compressed.decompress()))


