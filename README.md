# Underwater-image-restoration
Implementation of Chongyi Li et.al algorithm for underwater image restoration.

Reference:
Li, C., Quo, J., Pang, Y., Chen, S., & Wang, J. (2016, March). Single underwater image restoration by blue-green channels dehazing and red channel correction. In Acoustics, Speech and Signal Processing (ICASSP), 2016 IEEE International Conference on (pp. 1731-1735). IEEE.

Run main.py and choose an image from the img folder to process. The result will show up in the result directory.

To use a differente window size for the local patch, run

$ python main.py -i {input image index} -w {window size}
