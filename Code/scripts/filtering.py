from scipy.signal import butter, lfilter

def make_low_pass_butterworth(cutoff_hz, order,rate):  
    nyq = 0.5 * rate
    low = cutoff_hz / nyq
    b, a = butter(order, low, btype='low')
    return (a,b)
def apply_filter(x,a,b):
    return lfilter(b, a, x)