from Numeric import *
from FFT import fft,inverse_fft
import Numeric

# Use FFTW if available, FFTPACK otherwise. In older releases, the
# FFTW module is called dfftw.

try:
    import fftw
except ImportError:
    fftw = None

if fftw is None:
    try:
        import dfftw
        fftw = dfftw
    except ImportError:
        pass

if fftw is None:
    import FFT


if fftw is None:

    def fft(series, lock=None):
        return FFT.fft(series)

    def inverse_fft(series, lock=None):
        return FFT.inverse_fft(series)

    def acf(series, padding=1, lock=None):
        if padding:
            n = 1
            while n < 2*len(series):
                n = n*2    
        else:
            n = 2*len(series)
        FFTSeries = FFT.fft(series,n,0)
        FFTSeries = FFTSeries*conjugate(FFTSeries)
        FFTSeries = FFT.inverse_fft(FFTSeries,len(FFTSeries),0)
        return FFTSeries.real[:len(series)]

    def CorrelationFunction(series1, series2, lock=None):
        n = 1
        while n < 2*len(series1):
            n = n*2
        FFTSeries1 = FFT.fft(series1,n,0)
        FFTSeries2 = FFT.fft(series2,n,0)
        FFTSeries1 = conjugate(FFTSeries1)*FFTSeries2
        FFTSeries1 = FFT.inverse_fft(FFTSeries1,len(FFTSeries1),0)
        return FFTSeries1.real[:len(series1)] / \
                  (len(series1)-arange(len(series1)))

else:

    fftw_plans = {}

    def get_fftw_plans(shape, lock):
        if lock is not None: lock.acquire()
        try:
            plan_f, plan_b = fftw_plans[shape]
        except KeyError:
            dummy1 = Numeric.zeros(shape, Numeric.Complex)
            dummy2 = Numeric.zeros(shape, Numeric.Complex)
            plan_f = fftw.fftw_create_plan_specific(shape[0],
                                                    fftw.FFTW_FORWARD,
                                                    fftw.FFTW_THREADSAFE,
                                                    dummy1, 1, dummy2, 1)
            plan_b = fftw.fftw_create_plan_specific(shape[0],
                                                    fftw.FFTW_BACKWARD,
                                                    fftw.FFTW_THREADSAFE,
                                                    dummy1, 1, dummy2, 1)
            fftw_plans[shape] = plan_f, plan_b
        if lock is not None: lock.release()
        return plan_f, plan_b

    def fft(series, lock=None):
        shape = series.shape
        plan_f, plan_b = get_fftw_plans(shape, lock)
        temp = Numeric.zeros(shape, Numeric.Complex)    
        if len(shape) == 1:
            nseries = 1
        else:
            nseries = shape[1]
        fftw.fftw(plan_f, nseries, series+0.j, nseries, 1,
                  temp, nseries, 1)
        return temp

    def inverse_fft(series, lock=None):
        shape = series.shape
        plan_f, plan_b = get_fftw_plans(shape, lock)
        temp = Numeric.zeros(shape, Numeric.Complex)    
        if len(shape) == 1:
            nseries = 1
        else:
            nseries = shape[1]
        fftw.fftw(plan_b, nseries, series+0.j, nseries, 1,
                  temp, nseries, 1)
        return temp/shape[0]

    def acf(series, padding=1, lock=None):
        if padding:
            n = 1
            while n < 2*len(series):
                n = n*2    
        else:
            n = 2*len(series)
        shape = (n,) + series.shape[1:]
        plan_f, plan_b = get_fftw_plans(shape, lock)

        array1 = Numeric.zeros(shape, Numeric.Complex)
        array2 = Numeric.zeros(shape, Numeric.Complex)
        if len(shape) == 1:
            nseries = 1
        else:
            nseries = shape[1]
        array1[:len(series), ...] = series+0j
        fftw.fftw(plan_f, nseries, array1, nseries, 1,
                  array2, nseries, 1)
        Numeric.multiply(array2, Numeric.conjugate(array2), array2)
        fftw.fftw(plan_b, nseries, array2, nseries, 1,
                  array1, nseries, 1)

        return array1[:len(series)].real/n

    def CorrelationFunction(series1, series2, lock=None):
        n = 1
        while n < 2*len(series1):
            n = n*2
        shape = (n,) + series1.shape[1:]
        plan_f, plan_b = get_fftw_plans(shape, lock)

        array1 = Numeric.zeros(shape, Numeric.Complex)
        array2 = Numeric.zeros(shape, Numeric.Complex)
        array3 = Numeric.zeros(shape, Numeric.Complex)
        if len(shape) == 1:
            nseries = 1
        else:
            nseries = shape[1]
        array1[:len(series1), ...] = series1+0j
        fftw.fftw(plan_f, nseries, array1, nseries, 1,
                  array2, nseries, 1)
        array1[:] = 0.
        array1[:len(series2), ...] = series2+0j
        fftw.fftw(plan_f, nseries, array1, nseries, 1,
                  array3, nseries, 1)
        Numeric.multiply(array3, Numeric.conjugate(array2), array3)
        fftw.fftw(plan_b, nseries, array3, nseries, 1,
                  array1, nseries, 1)

        return array1[:len(series1)].real / \
               (float(n)*(len(series1)-Numeric.arange(len(series1))))

def GaussianWindow(series,alpha=0.):
 
    series1=zeros((2*len(series)-2,),Float)
    res = series*exp(-0.5*(alpha*arange(len(series))/(len(series)-1))**2)
    series1[:len(series)] = res
    series1[len(series):] = res[-2:0:-1]
    return series1
