#!/usr/bin/python

#libraries
import Image
import sys
import glob
import time
import string
from string import join
#import matplotlib.pyplot as plt

#modules
import algorithms
import threshold 
import os
import hough
import imgUtils
import demod

class main:        
        def __init__(self,paths):
		self.paths=paths
                #paths = filter(lambda x: not(x.endswith('.db')),paths)
                #names = [os.path.basename(i) for i in paths]
                #self.codes = [self.process(paths[i]) for i in xrange(len(paths))]
#             for i in range(len(self.codes)):
#                        for j in range(len(self.codes)):
#                                a = self.codes[i]
#                                b = self.codes[j]
#                                hd = reduce(lambda x,y:x+y,[a[p]^b[p] for p in xrange(2048)])/2048.0
#                                print i,j,":",hd
                #writeString = ''
                #for i in range(len(names)):
                #        writeString += str(names[i]) + '\t' + str(self.codes[i]) + '\n'
                #writeString = reduce(lambda x,y:str(x)+'\n'+str(y),self.codes)
                #savePath = "out/"
                #with open('codes.txt','w') as f:
                #        print "Writing to file",f
                #        f.write(writeString)
                #f.close()

        def process(self,path):
                # Start timing  
                initTime = time.time()

                # Create path for saving
                pathArr = string.split(path,"/")
                ##savePath = "out/" + pathArr[1] + "/" + pathArr[2] + "/"
                savePath = "out/"

                # Make sure directory structure exists for saving
                self.ensure_dir(savePath)
                self.ensure_dir(savePath + "/polar/")
                self.ensure_dir(savePath + "/circles/")
                
                # Get the image name
                name = os.path.basename(path)

                # Windows is dumb and creates a Thumbs.db file for each directory with an image.
                # When doing batch processing, its a good idea to ignore this file.
                if name == "Thumbs.db":
                        sys.exit()

                print "Processing File: ",name

                # Open image
                inputImage = Image.open(path)

                w,h = inputImage.size
#                print "Size: ",w,h

                # If image is not 8-bit, grayscale it
                preGS = time.time()
                grayImageObject = algorithms.grayscaledImage(inputImage)
                grayscaleImage = grayImageObject.grayImage
                GStime = time.time() - preGS

                # Blur the image for pupil detection
                preB = time.time()
                blurredImageObject = algorithms.blurredImage(grayscaleImage,11)
                blurredImage = blurredImageObject.blurImage
                Btime = time.time() - preB

                prePT = time.time()
                hist = blurredImage.histogram()
                ind = range(256)
                threshObj = threshold.threshold(hist)
                pupilThreshold = threshObj.pupilThresh(0,70)
                lut = [255 if v > pupilThreshold else 0 for v in range(256)]
        
                pupilThreshImage = blurredImage.point(lut)
                PTtime = time.time() - prePT

                preB2 = time.time()
                iBlurredImageObject = algorithms.blurredImage(grayscaleImage,3)
                iBlurredImage = blurredImageObject.blurImage
                B2time = time.time() - preB2

                irisThresh = threshObj.irisThresh(pupilThreshold,240)

                lut = [255 if v > irisThresh else 0 for v in range(256)]

                irisThreshImage = iBlurredImage.point(lut)

                preSP = time.time()
                SobelPupilObject = algorithms.sobelFilter(pupilThreshImage)
                SobelPupilImage = SobelPupilObject.outputImage
                SPtime = time.time() - preSP


                ##################################################
                ###########Pre-hough pupil-processing.############
                #Looks for clusters of black to estimate the
                #pupil size and location. This is a quick hack and
                #does not work in all cases, such as an image with
                #a lot of areas as dark as the pupil##############
                ##################################################
                prePH = time.time()
                pupilPixels = pupilThreshImage.load()
                sumx = 0
                sumy = 0
                amount = 0

                for x in range(10,w):
                        for y in range(10,h):
                                if pupilPixels[x,y] == 0:
                                        sumx += x
                                        sumy += y
                                        amount += 1

                if sumx == 0 or sumy == 0:
                        print "Sorry brah, the pupil's gone"
                        sys.exit()

                sumx /= amount
                sumy /= amount

                pupilBoxCenter = (sumx, sumy)
                
                # sumx is the average x-location of the black pixels
                # sumy is the average y-location of the black pixels
                # A good idea would to have radii calculated for 4
                # directions, left and right, x and y, then average
                radiusXL = sumx
                while pupilPixels[radiusXL,sumy] == 0:
                        radiusXL += 1
                radiusXL -= sumx - 2

                radiusYD = sumy
                while pupilPixels[sumx,radiusYD] == 0:
                        radiusYD += 1
                radiusYD -= sumy - 2

                rad = (radiusXL,radiusYD)

                avgRad =  int((radiusXL+radiusYD)/2)

                HoughObject = hough.HoughTransform(SobelPupilImage,(sumx-1,sumy-1),(4,4),min(rad)-5,max(rad)+3)
                pX,pY,pR = HoughObject.pupilHough()

                PHtime = time.time() - prePH

                preSI = time.time() 
                SobelIrisObject = algorithms.sobelFilter(irisThreshImage)
                SobelIrisImage = SobelIrisObject.outputImage
                SItime = time.time() - preSI

                preIH = time.time()
                irisHoughObj = hough.HoughTransform(SobelIrisImage,(0,0),(0,0),0,0)
                iR = irisHoughObj.irisHough(pX,pY,pR)
                IHtime = time.time() - preIH

                preUW = time.time()
                unwrapObj = demod.unwrap(grayscaleImage,(pX,pY),pR,iR)
                polarImg = unwrapObj.unwrap()
                polarImg.save(savePath + "/polar/" + name)
                UWtime = time.time() - preUW

                gaborObj = demod.demod(polarImg)
                irisCode = gaborObj.demod()
               
                # Save various images.
                # Mainly used to debug in case of a failure.
                # This will be set in the prefences.
                self.saveImagePref = 0
                if (self.saveImagePref == 1):
                        grayscaleImage.save(savePath + "gray-" + name)
                        blurredImage.save(savePath + "blur-" + name)
                        pupilThreshImage.save(savePath + "threshp-" + name)
                        irisThreshImage.save(savePath + "threshi-" + name)
                        SobelPupilImage.save(savePath + "sobelp-"+name)
                        SobelIrisImage.save(savePath + "sobeli-"+name)

                self.saveHist = 0
                if (self.saveHist == 1):
                        plt.bar(ind,hist,color='b')
                        plt.savefig(savePath + "hist-" + name + ".png")

                # Draw circles on result image
                pupilDrawObject = imgUtils.Utils(inputImage)
                pupilDraw = pupilDrawObject.drawCircle(pX,pY,pR)
                irisDrawObject = imgUtils.Utils(inputImage)
                irisDraw = irisDrawObject.drawCircle(pX,pY,iR)
                inputImage.save(savePath + "/circles/" + name)

                #Clean-up
                del grayscaleImage
                del blurredImage
                del pupilThreshImage
                del irisThreshImage
                del SobelPupilImage
                del SobelIrisImage

                print "Done"
                segTime = time.time()-initTime
                print "It took %.3f" % (1000 * segTime),"ms\n"
                return irisCode, inputImage

        def ensure_dir(self,f):
                d = os.path.dirname(f)
                if not os.path.exists(d):
                        os.makedirs(d)



if __name__ == "__main__":
        argc = len(sys.argv)
        li = [sys.argv[i] for i in xrange(1,argc)]
        main(li)

