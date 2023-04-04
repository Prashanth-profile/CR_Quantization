import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
from scipy.fftpack import fft, fftshift
import cmath
import sionna

SAMPLE_RATE = 1000  # Hertz
#DURATION = 0.5  # Seconds

ts = 1.0/SAMPLE_RATE
t = np.arange(0,1,ts)

freq_array=[]
freq = 10
num_bits_per_symbol=1
ebno_db = 15 # Desired Eb/No in dB

for i in range(10):
    x = 1*np.sin(2*np.pi*freq*t)
    x_tf=tf.convert_to_tensor(np.array(x), dtype=tf.complex64, name=None)
    #print("Sine wave generated of length ", x_tf, "of type", x_tf.dtype)
    awgn = sionna.channel.AWGN()
    no = sionna.utils.ebnodb2no(ebno_db, num_bits_per_symbol, coderate=0.5)
    #print("Variance of the noise", no, "dB")
    y = awgn([x_tf, no])
    #print("Received symbols are", y)

    # Generate a 2 hertz sine wave that lasts for 5 seconds
    #x, A = generate_sine_wave(10, SAMPLE_RATE, DURATION)

    NFFT=1024 #NFFT-point DFT
    X=fftshift(fft(y.numpy(),NFFT)) #compute DFT using FFT


    ind = np.unravel_index(X.argmax(axis=0), X.shape)

    nVals = np.arange(start = -NFFT/2,stop = NFFT/2)*SAMPLE_RATE/NFFT #raw index for FFT plot
    r,ph=cmath.polar(X[ind])
    print("Peak power detected at Frequency ", abs(nVals[ind]), "Hz and power at max freq component is", round(20*np.log10(abs(X[ind])),3), "dB with phase offset of ", np.angle(X[ind], deg=True), " degrees")
    freq_array.append(abs(nVals[ind]))

fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(t, x)
ax1.set_xlabel('Sample points')
ax1.set_ylabel('Amplitude')

ax2.plot(nVals,np.abs(X))
ax2.set_xlabel('Sample points (N-point DFT)')
ax2.set_ylabel('DFT Values')
ax2.set_xlim(-50,50)

print("List of frequencies are", np.array(freq_array))

plt.show()