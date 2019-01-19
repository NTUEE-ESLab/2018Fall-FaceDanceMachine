Face Dance Machine on Raspberry Pi3
==
## Abstract
In this project, we have successfully developed a “face dancing machine” game on Raspberry Pi3. By “face dancing”, we simply make facial expressions identical to the cartoon emojis on the screen, just like what we do to our legs when playing traditional “dance dance revolution”. We integrated several OpenCV and Dlib functions with our own algorithms to meet the goal of recognizing facial expression in real-time. Moreover, the GUI interface is implemented via the Pygame package on Python3. The main contribution is that we have completed complex computations on an embedded system rather than on a pc, where the former only runs on ARM Cortex-A53 with 1024MB RAM.

## Demo video
 <iframe width="1280" height="720" src="https://www.youtube.com/watch?v=WfL82hLIuYI&feature=youtu.be" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen>
## Implementation
### Environment
* Raspberry Pi3
* Python 3
* OpenCV 3.4.3 (NOTE: turn on NEON and VPFV3 hardware optimizations when compiling via source)
* Pygame 1.9.3
* Imutils 0.5.2
* Dlib 19.16.99 (NOTE: turn on NEON and VPFV3 hardware optimizations when compiling via source)
* Numpy

The installation step of packages mentioned above are expanded in our Final Project Report.
### System structure 
