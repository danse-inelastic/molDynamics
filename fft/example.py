from scipy import *
from pylab import *

a = zeros((1000,1000))
a[:100][:100]=1


b = fft(a)
plot(abs(b))
show()
# do spatial fourier transform

# do time fourier transform

# write new file