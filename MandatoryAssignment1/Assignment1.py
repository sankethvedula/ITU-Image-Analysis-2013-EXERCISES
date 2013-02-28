import cv2
import cv
import pylab
from SIGBTools import RegionProps
from SIGBTools import getLineCoordinates
from SIGBTools import ROISelector
from SIGBTools import getImageSequence
import numpy as np
import sys




inputFile = "/Developer/GitRepos/ITU-Image-Analysis-2013-EXERCISES/MandatoryAssignment1/Sequences/eye1.avi"
outputFile = "eyeTrackerResult.mp4"

#--------------------------
#         Global variable
#--------------------------
global imgOrig,leftTemplate,rightTemplate,frameNr
imgOrig = []
#These are used for template matching
leftTemplate = []
rightTemplate = []
frameNr =0


def GetPupil(gray,thr):
    '''Given a gray level image, gray and threshold value return a list of pupil locations'''
    tempResultImg = cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR) #used to draw temporary results
    
    #cv2.circle(tempResultImg,(100,200), 2, (0,0,255),4)
    #cv2.imshow("TempResults",tempResultImg)

    props = RegionProps()
    val,binI = cv2.threshold(gray, thr, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow("Threshold",binI)
    #Calculate blobs
    sliderVals = getSliderVals() #Getting slider values
    contours, hierarchy = cv2.findContours(binI, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #Finding contours/candidates for pupil blob
    pupils = []
    pupilEllipses = []
    for cnt in contours:
        values = props.CalcContourProperties(cnt,['Area','Length','Centroid','Extend','ConvexHull']) #BUG - Add cnt.astype('int') in Windows
        if values['Area'] < sliderVals['maxSize'] and values['Area'] > sliderVals['minSize'] and values['Extend'] < 1.2:
            pupils.append(values)
            centroid = (int(values['Centroid'][0]),int(values['Centroid'][1]))
            cv2.circle(tempResultImg,centroid, 2, (0,0,255),4)
            pupilEllipses.append(cv2.fitEllipse(cnt))
    cv2.imshow("TempResults",tempResultImg)
    return pupilEllipses 
    
    
    
            
            
            
        
    
    
    # YOUR IMPLEMENTATION HERE !!!!

    return pupils

def GetGlints(gray,thr):
    ''' Given a gray level image, gray and threshold
    value return a list of glint locations'''
    # YOUR IMPLEMENTATION HERE !!!!
    pass

def GetIrisUsingThreshold(gray,pupil):
    ''' Given a gray level image, gray and threshold
    value return a list of iris locations'''
    # YOUR IMPLEMENTATION HERE !!!!
    pass

def circularHough(gray):
    ''' Performs a circular hough transform of the image, gray and shows the  detected circles
    The circe with most votes is shown in red and the rest in green colors '''
    #See help for http://opencv.itseez.com/modules/imgproc/doc/feature_detection.html?highlight=houghcircle#cv2.HoughCircles
    blur = cv2.GaussianBlur(gray, (31,31), 11)

    dp = 6; minDist = 30
    highThr = 20 #High threshold for canny
    accThr = 850 #accumulator threshold for the circle centers at the detection stage. The smaller it is, the more false circles may be detected
    maxRadius = 50
    minRadius = 155
    circles = cv2.HoughCircles(blur,cv2.cv.CV_HOUGH_GRADIENT, dp,minDist, None, highThr,accThr,maxRadius, minRadius)

    #Make a color image from gray for display purposes
    gColor = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    if (circles !=None):
    #print circles
        all_circles = circles[0]
        M,N = all_circles.shape
        k=1
        for c in all_circles:
            cv2.circle(gColor, (int(c[0]),int(c[1])),c[2], (int(k*255/M),k*128,0))
            k=k+1
    c=all_circles[0,:]
    cv2.circle(gColor, (int(c[0]),int(c[1])),c[2], (0,0,255),5)
    cv2.imshow("hough",gColor)

def GetIrisUsingNormals(gray,pupil,normalLength):
    ''' Given a gray level image, gray and the length of the normals, normalLength
    return a list of iris locations'''
    # YOUR IMPLEMENTATION HERE !!!!
    pass

def GetIrisUsingSimplifyedHough(gray,pupil):
    ''' Given a gray level image, gray
    return a list of iris locations using a simplified Hough transformation'''
    # YOUR IMPLEMENTATION HERE !!!!
    pass

def GetEyeCorners(leftTemplate, rightTemplate,pupilPosition=None):
    pass

def FilterPupilGlint(pupils,glints):
    ''' Given a list of pupil candidates and glint candidates returns a list of pupil and glints'''
    pass

def update(I):
    '''Calculate the image features and display the result based on the slider values'''
    #global drawImg
    global frameNr,drawImg
    img = I.copy()
    sliderVals = getSliderVals()
    gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    # Do the magic
    pupils = GetPupil(gray,sliderVals['pupilThr'])
    glints = GetGlints(gray,sliderVals['glintThr'])
    FilterPupilGlint(pupils,glints)

    #Do template matching
    global leftTemplate
    global rightTemplate
    GetEyeCorners(leftTemplate, rightTemplate)
    #Display results
    global frameNr,drawImg
    x,y = 15,10
    setText(img,(520,y+10),"Frame:%d" %frameNr)
    sliderVals = getSliderVals()

    # for non-windows machines we print the values of the threshold in the original image
    if sys.platform != 'win32':
        step=18
        cv2.putText(img, "pupilThr :"+str(sliderVals['pupilThr']), (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv2.CV_AA)
        cv2.putText(img, "glintThr :"+str(sliderVals['glintThr']), (x, y+step), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv2.CV_AA)
        cv2.putText(img, "maxSize :"+str(sliderVals['maxSize']), (x, y+2*step), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv2.CV_AA)
        cv2.putText(img, "minSize :"+str(sliderVals['minSize']), (x, y+3*step), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv2.CV_AA)
        cv2.putText(img, "minSize :"+str(sliderVals['minSize']), (x, y+4*step), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv2.CV_AA)

    for pupil in pupils:
        cv2.ellipse(img,pupil,(0,255,0),1)
        C = int(pupil[0][0]),int(pupil[0][1])
        cv2.circle(img,C, 2, (0,0,255),4)
    #for glint in glints:
        #C = int(glint[0]),int(glint[1])
        #cv2.circle(img,C, 2,(255,0,255),5)
    cv2.imshow("Result", img)

        #For Iris detection - Week 2
        #circularHough(gray)

    #copy the image so that the result image (img) can be saved in the movie
    drawImg = img.copy()


def printUsage():
    print "Q or ESC: Stop"
    print "SPACE: Pause"
    print "r: reload video"
    print 'm: Mark region when the video has paused'
    print 's: toggle video  writing'
    print 'c: close video sequence'

def run(fileName,resultFile='eyeTrackingResults.avi'):

    ''' MAIN Method to load the image sequence and handle user inputs'''
    global imgOrig, frameNr,drawImg
    setupWindowSliders()
    props = RegionProps()
    cap,imgOrig,sequenceOK = getImageSequence(fileName)
    videoWriter = 0

    frameNr =0
    if(sequenceOK):
        update(imgOrig)
    printUsage()
    frameNr=0
    saveFrames = False

    while(sequenceOK):
        sliderVals = getSliderVals()
        frameNr=frameNr+1
        ch = cv2.waitKey(1)
        #Select regions
        if(ch==ord('m')):
            if(not sliderVals['Running']):
                roiSelect=ROISelector(imgOrig)
                pts,regionSelected= roiSelect.SelectArea('Select left eye corner',(400,200))
                if(regionSelected):
                    leftTemplate = imgOrig[pts[0][1]:pts[1][1],pts[0][0]:pts[1][0]]

        if ch == 27:
            break
        if (ch==ord('s')):
            if((saveFrames)):
                videoWriter.release()
                saveFrames=False
                print "End recording"
            else:
                imSize = np.shape(imgOrig)
                videoWriter = cv2.VideoWriter(resultFile, cv.CV_FOURCC('D','I','V','3'), 15.0,(imSize[1],imSize[0]),True) #Make a video writer
                saveFrames = True
                print "Recording..."



        if(ch==ord('q')):
            break
        if(ch==32): #Spacebar
            sliderVals = getSliderVals()
            cv2.setTrackbarPos('Stop/Start','Threshold',not sliderVals['Running'])
        if(ch==ord('r')):
            frameNr =0
            sequenceOK=False
            cap,imgOrig,sequenceOK = getImageSequence(fileName)
            update(imgOrig)
            sequenceOK=True

        sliderVals=getSliderVals()
        if(sliderVals['Running']):
            sequenceOK, imgOrig = cap.read()
            if(sequenceOK): #if there is an image
                update(imgOrig)
            if(saveFrames):
                videoWriter.write(drawImg)

    videoWriter.release



#--------------------------
#         UI related
#--------------------------

def setText(dst, (x, y), s):
    cv2.putText(dst, s, (x+1, y+1), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness = 2, lineType=cv2.CV_AA)
    cv2.putText(dst, s, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv2.CV_AA)


def setupWindowSliders():
    ''' Define windows for displaying the results and create trackbars'''
    cv2.namedWindow("Result")
    cv2.namedWindow('Threshold')
    cv2.namedWindow("TempResults")
    #Threshold value for the pupil intensity
    cv2.createTrackbar('pupilThr','Threshold', 90, 255, onSlidersChange)
    #Threshold value for the glint intensities
    cv2.createTrackbar('glintThr','Threshold', 240, 255,onSlidersChange)
    #define the minimum and maximum areas of the pupil
    cv2.createTrackbar('minSize','Threshold', 20, 200, onSlidersChange)
    cv2.createTrackbar('maxSize','Threshold', 200,200, onSlidersChange)
    #Value to indicate whether to run or pause the video
    cv2.createTrackbar('Stop/Start','Threshold', 0,1, onSlidersChange)

def getSliderVals():
    '''Extract the values of the sliders and return these in a dictionary'''
    sliderVals={}
    sliderVals['pupilThr'] = cv2.getTrackbarPos('pupilThr', 'Threshold')
    sliderVals['glintThr'] = cv2.getTrackbarPos('glintThr', 'Threshold')
    sliderVals['minSize'] = 50*cv2.getTrackbarPos('minSize', 'Threshold')
    sliderVals['maxSize'] = 50*cv2.getTrackbarPos('maxSize', 'Threshold')
    sliderVals['Running'] = 1==cv2.getTrackbarPos('Stop/Start', 'Threshold')
    return sliderVals

def onSlidersChange(dummy=None):
    ''' Handle updates when slides have changed.
     This  function only updates the display when the video is put on pause'''
    global imgOrig
    sv=getSliderVals()
    if(not sv['Running']): # if pause
        update(imgOrig)

#--------------------------
#         main
#--------------------------
run(inputFile)