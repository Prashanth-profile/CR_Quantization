# Import TensorFlow and NumPy
import tensorflow as tf
import numpy as np

try:
    import sionna
except ImportError as e:
    # Install Sionna if package is not already installed
    import os
    #os.system ("pip install sionna")
    import sionna

# For plotting
#%matplotlib inline
# IPython "magic function" for inline plots
#matplotlib inline
import matplotlib.pyplot as plt
import time
# For the implementation of the Keras models
#from tensorflow.keras import Model

batch_size = 10 # Number of symbols we want to generate
num_bits_per_symbol = 2 # 16-QAM has four bits per symbol
binary_source = sionna.utils.BinarySource()
#k = 12
n = 1000   # Codeword length per transmitted codeword
coderate=0.5    # Coderate

EBN0_DB_MIN = -3.0 # Minimum value of Eb/N0 [dB] for simulations
EBN0_DB_MAX = 5.0 # Maximum value of Eb/N0 [dB] for simulations

k=int(coderate * n) #Number of information bits per codeword

'''class CodedSystemAWGN(tf.keras.Model): # Inherits from Keras Model
    def __init__(self, num_bits_per_symbol, n, coderate):
        super().__init__() # Must call the Keras model initializer

        self.num_bits_per_symbol = num_bits_per_symbol
        self.n = n
        self.k = int(n*coderate)
        self.coderate = coderate
        self.constellation = sionna.mapping.Constellation("qam", self.num_bits_per_symbol)

        self.mapper = sionna.mapping.Mapper(constellation=self.constellation)
        self.demapper = sionna.mapping.Demapper("app", constellation=self.constellation)

        self.binary_source = sionna.utils.BinarySource()
        self.awgn_channel = sionna.channel.AWGN()

        self.encoder = sionna.fec.ldpc.LDPC5GEncoder(self.k, self.n)
        self.decoder = sionna.fec.ldpc.LDPC5GDecoder(self.encoder, hard_out=True)

    #@tf.function # activate graph execution to speed things up
    def __call__(self, batch_size, ebno_db):
        no = sionna.utils.ebnodb2no(ebno_db, num_bits_per_symbol=self.num_bits_per_symbol, coderate=self.coderate)

        bits = self.binary_source([batch_size, self.k])
        codewords = self.encoder(bits)
        print("Encoded bytes", codewords)
        x = self.mapper(codewords)
        y = self.awgn_channel([x, no])
        llr = self.demapper([y,no])
        print("Decoded bytes", llr)
        bits_hat = self.decoder(llr)
        return bits, bits_hat

model_coded_awgn = CodedSystemAWGN(num_bits_per_symbol=num_bits_per_symbol,
                                   n=2048,
                                   coderate=coderate)'''
################################## Get BER results ##################################################
'''model_coded_awgn = CodedSystemAWGN(num_bits_per_symbol=num_bits_per_symbol,
                                   n=2048,
                                   coderate=coderate)
# we use the built-in ber simulator function from Sionna which uses and early stop after reaching num_target_errors
sionna.config.xla_compat=True
ber_plots = sionna.utils.PlotBER("AWGN")
ber_mc,_=ber_plots.simulate(model_coded_awgn,
                   ebno_dbs=np.linspace(EBN0_DB_MIN, EBN0_DB_MAX, 15),
                   batch_size=2000,
                   num_target_block_errors=500,
                   legend="Coded",
                   soft_estimates=False,
                   max_mc_iter=15,
                   show_fig=True,
                   forward_keyboard_interrupt=False)
sionna.config.xla_compat=False
sionna.utils.plotting.plot_ber(np.linspace(EBN0_DB_MIN, EBN0_DB_MAX, 15),
                               ber_mc,
                               legend="E2E Model",
                               ylabel="Coded BER");'''
################################################     Get BER results end here ####################################'''
b = binary_source([batch_size, k])
print("binary symbols source", b, " of length ", len(b))

#LDPC encoding
# instantiate a new encoder for codewords of length n
encoder = sionna.fec.ldpc.LDPC5GEncoder(k, n)
print("Encoder configuration is ", encoder)
# the decoder must be linked to the encoder (to know the exact code parameters used for encoding)
decoder = sionna.fec.ldpc.LDPC5GDecoder(encoder,
                                    hard_out=True, # binary output or provide soft-estimates
                                    return_infobits=True, # or also return (decoded) parity bits
                                    num_iter=20, # number of decoding iterations
                                    cn_type="boxplus-phi") # also try "minsum" decoding
c = encoder(b)
print("Encoded bits are", c.numpy())

constellation = sionna.mapping.Constellation("qam", num_bits_per_symbol)
constellation.show()

mapper = sionna.mapping.Mapper(constellation=constellation)
# The demapper uses the same constellation object as the mapper
demapper = sionna.mapping.Demapper("app", constellation=constellation)
x = mapper(c)
print("mapped data is ", x)

awgn = sionna.channel.AWGN()
ebno_db = 15 # Desired Eb/No in dB
no = sionna.utils.ebnodb2no(ebno_db, num_bits_per_symbol, coderate=coderate)
print("noise power spectral density is", no)
y = awgn([x, no])
print("Received data is ", len(y))

llr = demapper([y, no])
print("Received qam symbols are", llr.numpy())

bits_hat=decoder(llr)
print("Received bits are ", bits_hat)


# Visualize the received signal
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(7,7))
ax = fig.add_subplot(111)
plt.scatter(np.real(y), np.imag(y))
ax.set_aspect("equal", adjustable="box")
plt.xlabel("Real Part")
plt.ylabel("Imaginary Part")
plt.grid(True, which="both", axis="both")
plt.title("Received Symbols")
plt.show()