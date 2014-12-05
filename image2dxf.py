import sys, getopt 
import os 
from subprocess import call
import scipy as sp
from PIL import Image
from PIL import ImageFilter 

def mappoint (i):
   if i > 127: return 255
   else: return 0

if __name__ =="__main__":
    print sys.argv 
    greyscalein = sys.argv[1]
    smoothbnw = sys.argv[2]
    traced = sys.argv[3]
    dxfout = sys.argv[4] 
    stlout = sys.argv[5] 
    # smooth the image 
    print "# smoothing #"
    im = Image.open(greyscalein)
#    im = im.filter(ImageFilter.GaussianBlur(8)) 
    # convert to bilevel (black and white) bitmap 
    print "# thresholding #" 
    im = im.point(mappoint)
    im = im.convert("1",dither=None)
    im.save(smoothbnw)
    #trace the bitmap and export eps
    print "# tracing #"
    call("potrace -e -O 0.005 -W 12 -H 12 -r 800 %s -o %s" % (smoothbnw, traced), shell=True)
    print "# converting to dxf #" 
    # convert the eps to a dxf -polyaslines
    call('pstoedit -flat 0.01 -f "dxf:-mm -polyaslines" %s %s' % (traced, dxfout), shell=True)
    call("potrace -s -O 0.01 %s -o %s" % (smoothbnw, traced+".svg"), shell=True)

    print "# extruding with openscad #"
    fscadname = "part-%d.scad" % os.getpid()
    fscad = open(fscadname, "w")
    fscad.write('linear_extrude(height=1,center=true,convexity=10) import("%s");' % dxfout)
    fscad.close()
    call("openscad %s -o %s" % (fscadname, stlout), shell=True) 

