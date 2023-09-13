# Initialization
from reedsolo import RSCodec, ReedSolomonError
rsc = RSCodec(10)  # 10 ecc symbols


print(rsc.encode([255,2,3,4]))
print(rsc.encode(bytearray([255,2,3,4])))
print(rsc.encode(b'hello world'))