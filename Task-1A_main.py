#classes and subclasses to import
import cv2
import numpy as np
import os

filename = 'result1A_1167.csv'
#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
img1 = cv2.imread('sampleShapes\\rhombus.png')
img2 = cv2.imread('sampleShapes\\trapezium.png')
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
ret, thresh1 = cv2.threshold(gray1,127,255,0)
ret, thresh2 = cv2.threshold(gray2,127,255,0)
_,conR,hierarchy = cv2.findContours(thresh1,2,1)
_,conT,hierarchy = cv2.findContours(thresh2,2,1)
lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])
lower_green = np.array([50, 50, 120])
upper_green = np.array([70, 255, 255])
lower_red = np.array([0, 100, 100])
upper_red = np.array([20, 255, 255])
#subroutine to write results to a csv
font = cv2.FONT_HERSHEY_COMPLEX
def writecsv(color,shape,(cx,cy)):
    global filename
    #open csv file in append mode
    filep = open(filename,'a')
    # create string data to write per image
    datastr = "," + color + "-" + shape + "-" + str(cx) + "-" + str(cy)
    #write to csv
    filep.write(datastr)

def detectShape(i):
    approx = cv2.approxPolyDP(i,0.01*cv2.arcLength(i,True),True)
    x = len(approx)
    if x==4:
        global conR
        global conT
        ret1=cv2.matchShapes(conR[1],i,1,0.0)
        ret2=cv2.matchShapes(conT[1],i,1,0.0)
        if ret1<ret2:
            return "rhombus"
        else :
            return "trapezium"
    elif x==3:
        return "triangle"
    elif x==5:
        return "pentagon"
    elif x==6:
        return "hexagon"
    else:
        return "circle"

def detectCentroid(i):
    M = cv2.moments(i)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    return cx,cy

def detectColor(i):
    hsv = cv2.cvtColor(i, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, lower_blue, upper_blue)
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    mask3 = cv2.inRange(hsv, lower_green, upper_green)
    ret, threshS1 = cv2.threshold(mask1,127,255,0)
    _,contoursS1,hierarchy = cv2.findContours(threshS1,2,1)
    ls=[]
    red=[]
    green=[]
    for i in contoursS1:
        blue=[]
        blue.append("blue")
        blue.append(detectShape(i))
        cx,cy=detectCentroid(i)
        writecsv(blue[0],blue[1],(cx,cy))
        blue.append(str(detectCentroid(i)))
        ls.append(blue)
    ret, threshS2 = cv2.threshold(mask2,127,255,0)
    _,contoursS2,hierarchy = cv2.findContours(threshS2,2,1)
    for i in contoursS2:
        red=[]
        red.append("red")
        red.append(detectShape(i))
        cx,cy=detectCentroid(i)
        writecsv(red[0],red[1],(cx,cy))
        red.append(str(detectCentroid(i)))
        ls.append(red)
    ret, threshS3 = cv2.threshold(mask3,127,255,0)
    _,contoursS3,hierarchy = cv2.findContours(threshS3,2,1)
    for i in contoursS3:
        green=[]
        green.append("green")
        green.append(detectShape(i))
        cx,cy=detectCentroid(i)
        writecsv(green[0],green[1],(cx,cy))
        green.append(str(detectCentroid(i)))
        ls.append(green)
    return ls

def tupleToInt(t):
    ls=[]
    num=0
    for i in t:
        if((i==",")):
            ls.append(num)
            num=0
        elif((i==' ')):
            continue
        elif((i=='(')):
            continue
        elif((i==')')):
            ls.append(num)
        else:
            num=num*10+int(i)
    return ls

def stringToName(s):
    ans=''
    for i in s[2:]:
        if(i=='.'):
            return ans
        else:
            ans=ans+i
def main(path):
#####################################################################################################
    #Write your code here!!!
    imgS = cv2.imread(path)
    ls=detectColor(imgS)
    for i in ls:
        new=tupleToInt(i[2])
        cv2.putText(imgS,i[0],(new[0]-30,new[1]-30),font,0.5,(0,0,0))
        cv2.putText(imgS,i[1],(new[0]-10,new[1]+10),font,0.5,(0,0,0))
        cv2.putText(imgS,i[2],(new[0]+10,new[1]+20),font,0.5,(0,0,0))
    name=stringToName(path)
    name=name+'output.png'
    cv2.imwrite(name,imgS)
        
    return ls
    cv2.imshow('frame',imgS)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
#####################################################################################################


#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#main where the path is set for the directory containing the test images
if __name__ == "__main__":
    finalAns=[]
    mypath = '.'
    #getting all files in the directory
    onlyfiles = [os.path.join(mypath, f) for f in os.listdir(mypath) if f.endswith(".png")]
    #iterate over each file in the directory
    for fp in onlyfiles:
        #Open the csv to write in append mode
        filep = open(filename,'a')
        #this csv will later be used to save processed data, thus write the file name of the image 
        filep.write(fp)
        #close the file so that it can be reopened again later
        filep.close()
        #process the image
        data = main(fp)
        print data
        #open the csv
        filep = open(filename,'a')
        #make a newline entry so that the next image data is written on a newline
        filep.write('\n')
        #close the file
        filep.close()
