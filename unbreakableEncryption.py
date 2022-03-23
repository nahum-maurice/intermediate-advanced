from secrets import token_bytes
from typing import Tuple

def random_key(length: int) -> int:
    #generates <length> random bytes
    tb: bytes = token_bytes(length)
    #convert those bytes into a big string and return it
    return int.from_bytes(tb, "big")


def encrypt(original: str) -> Tuple[int, int]:
    # transform the original text into bytes
    original_bytes: bytes = original.encode()
    # generate the random keys
    dummy: int = random_key(len(original_bytes))
    original_key: int = int.from_bytes(original_bytes, "big")
    # generate by the rule : A ^ B = C 
    encrypted: int = original_key ^ dummy
    return dummy, encrypted


def decrypt(key1: int, key2: int) -> str:
    decrypted: int = key1 ^ key2
    temp: bytes = decrypted.to_bytes((decrypted.bit_length() + 7) // 8, "big")
    return temp.decode()


if __name__ == "__main__":
    key1, key2 = encrypt("The world is just encrypted.")
    result : str = decrypt(key1, key2)
    print(result)

