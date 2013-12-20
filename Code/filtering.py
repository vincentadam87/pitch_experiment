from scipy.signal import kaiserord, butter, lfilter, firwin, freqz
from pylab import figure, clf, plot, xlabel, ylabel, xlim, ylim, title, grid, axes, show


# -------------- Kaiser

def make_low_pass_kaiser(cutoff_hz, w,rate):  
    # The Nyquist rate of the signal.
    nyq_rate = rate / 2.0
    width = w/nyq_rate
    # The desired attenuation in the stop band, in dB.
    ripple_db = 60.0
    # Compute the order and Kaiser parameter for the FIR filter.
    N, beta = kaiserord(ripple_db, width)
    taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
    return (taps,N,nyq_rate)

def apply_filter_fir(x,fir):
    # Use lfilter to filter x with the FIR filter.
    return lfilter(fir, 1.0, x)

# -------------- Butterworth


def make_low_pass_butterworth(cutoff_hz, order,rate):  
    nyq = 0.5 * rate
    low = cutoff_hz / nyq
    b, a = butter(order, low, btype='low')
    return (a,b)
def apply_filter(x,a,b):
    return lfilter(b, a, x)