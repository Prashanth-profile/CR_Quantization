import scipy.special as special
import sk_dsp_comm.digitalcom as dc
import sk_dsp_comm.fec_conv as fec
import numpy as np
from numpy import sign
from numpy.random import randint
import errorcorrectioncode

N_bits_per_frame = 10000
EbN0 = 4
total_bit_errors = 0
total_bit_count = 0
#cc1 = fec.FECConv(('10000','10011'),25)
#cc1 = fec.FECConv(('1000', '0101', '1101'),2)
# Encode with shift register starting state of '0000'
#state = '0000'


def conv_block_encoding_3stage(input_byt, block_size):
    cc1 = fec.FECConv(('1000', '0111', '0101'), 2)
    state = '0000'

    x_block = np.array(errorcorrectioncode.bytearray_to_binarray(input_byt))
    encoded = []
    for i in range(0, len(x_block), block_size):
        y_block, state_enc = cc1.conv_encoder(x_block[i:i+block_size], state)
        print("block encoding y is", y_block)

        encoded.append(y_block)

    return encoded


while total_bit_errors < 100:
    # Create 100000 random 0/1 bits
    input_bytes = b"\x02\x51\x01"
    x = np.array(errorcorrectioncode.bytearray_to_binarray(input_bytes))
    #x=np.pad(x, (0,1))
    #x = randint(0,2,N_bits_per_frame)
    print("x is", x, "of length ", len(x))
    y = conv_block_encoding_3stage(input_bytes, 8)
    #y,state = cc1.conv_encoder(x,state)
    print("y is", y)
    parity = [y.astype(int)[a] for a in range(len(y)) if a % 3 != 0]
    print("parity is ", parity)
    # Add channel noise to bits, include antipodal level shift to [-1,1]
    #yn_soft = dc.cpx_awgn(2*y-1,EbN0-3,1) # Channel SNR is 3 dB less for rate 1/2
    yn_hard = ((sign(y.real)+1)/2).astype(int)
    print("Hard decoded", yn_hard, "of length", len(yn_hard))
    z = cc1.viterbi_decoder(yn_hard,'hard')
    print("z is", z.astype(int), "of length", len(z))
    # Count bit errors
    bit_count, bit_errors = dc.bit_errors(x,z)
    total_bit_errors += bit_errors
    total_bit_count += bit_count
    print('Bits Received = %d, Bit errors = %d, BEP = %1.2e' %\
          (total_bit_count, total_bit_errors,\
           total_bit_errors/total_bit_count))
print('*****************************************************')
print('Bits Received = %d, Bit errors = %d, BEP = %1.2e' %\
      (total_bit_count, total_bit_errors,\
       total_bit_errors/total_bit_count))