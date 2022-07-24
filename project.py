 #Project 
import numpy as np , cv2 , matplotlib.pyplot as mlt , cv2.aruco as aruco ,math,os #importing essential libraries

#part 1 findind the countours i.e squares

def countorfind(img):
    _, thrash=cv2.threshold(img , 240,255,cv2.THRESH_BINARY)
    contours, _=cv2.findContours(thrash,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        approx=cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour, True),True) #approximates the given image into a polygon with precision
        if len(approx)== 4:
            x1,y1,w,h=cv2.boundingRect(approx)
            asp_rat=float(w/h)
            if asp_rat>=0.98 and asp_rat<=1.02:
                rect = cv2.minAreaRect(contour)
                box = cv2.boxPoints(rect)
                box1 = np.int0(box)
                return box


#rotation of aruco marker images to crop if properly
            
def rotate_img(img,angle,rotpoint):
    (height,width)=img.shape[:2]
    
    mat=cv2.getRotationMatrix2D(rotpoint,angle,1.0)#to make the transformation matrix M which will be used for rotating a image
    dimensions=(width,height)
    return cv2.warpAffine(img,mat,dimensions)



# pasting the aruco marker images on the original image

def augmenting(corners,ids,img,imgaug):
    tl=corners[0][0] , corners[0][1]
    tr=corners[1][0] , corners[1][1]
    br=corners[2][0] , corners[2][1]
    bl=corners[3][0] , corners[3][1]
    h,w,c=imgaug.shape
    pts1=np.array([tl,tr,br,bl])
    pts2=np.float32([[0,0],[w,0],[w,h],[0,h]])
    matrix,_=cv2.findHomography(pts2,pts1)
    imgout=cv2.warpPerspective(imgaug,matrix,(img.shape[1],img.shape[0])) #used to paste on image to another & used in transformation
    cv2.fillConvexPoly(img,pts1.astype(int),(0,0,0))# to remove the black background 
    imgout=img+imgout
    return imgout

#reading the aruco markers to get it's id

def find_aruco(img):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    key=getattr(aruco,'DICT_5X5_250')# returns the value of the specified attribute from the specified object i.e aruco
    adict=aruco.Dictionary_get(key)
    aparam=aruco.DetectorParameters_create()
    (corners,ids,rejectedaruco)=cv2.aruco.detectMarkers(gray,adict,parameters=aparam)#detecting and reading the markers
    x1,y1=(corners[0][0][0][0],corners[0][0][0][1])
    x2,y2=(corners[0][0][1][0],corners[0][0][1][1])
    ynet=y2-y1
    xnet=x2-x1
    thetha=float(ynet/xnet)
    slope=math.atan(thetha)*(180/3.14)
    slenght=math.sqrt((ynet)**2+(xnet)**2)
    return corners,ids[0][0],(int(x1),int(y1)),slope,slenght


         

##!! Identification of the colour of the square !!##

img=cv2.imread("C:\\Users\\Ketan Kumar Verma\\OneDrive\\Desktop\\robo ism\\CVtask.jpg")
new_img=cv2.resize(img,(877,620))
hsv_img = cv2.cvtColor(new_img , cv2.COLOR_BGR2HSV)

          # finding pink peach colour
lower=np.array([4,4,216])
upper=np.array([29,35,251])
w=cv2.inRange(hsv_img,lower,upper)

          # finding green colour
lower=np.array([26,52,196])
upper=np.array([60,191,217])
g=cv2.inRange(hsv_img,lower,upper)


          # finding orange colour
lower=np.array([10,40,40])
upper=np.array([30,255,255])
o=cv2.inRange(hsv_img,lower,upper)


          # finding black colour
lower=np.array([0,0,0])
upper=np.array([10,210,210])
b=cv2.inRange(hsv_img,lower,upper)
b=cv2.bilateralFilter(b,10,25,25)
b=cv2.GaussianBlur(b,(3,3),0)
        



# reading the images of aruco markers
e="C:\\Users\\Ketan Kumar Verma\\OneDrive\\Desktop\\robo ism\\"
f=["Ha.jpg","HaHa.jpg","LMAO.jpg","XD.jpg"]
d=[]
def img_read(x):
    img1=cv2.imread(e+x)
    d.append(img1)

for i in f:
    img_read(i)

z=0

#calling all the functions and giving arguments to them
for i in d:
    corners,ids,point,m,L=find_aruco(i)
    rted=rotate_img(i,m,point)
    crpped=rted[point[1]:point[1]+int(L),point[0]:point[0]+int(L)]
    if ids==1:
        box=countorfind(g)
        new_img=augmenting(box,ids,new_img,crpped)
    elif ids==2:
        box=countorfind(o)
        new_img=augmenting(box,ids,new_img,crpped)
    elif ids==3:
        box=countorfind(b)
        new_img=augmenting(box,ids,new_img,crpped)
    else :
        box=countorfind(w)
        new_img=augmenting(box,ids,new_img,crpped)
    string_ofid=str(ids)    
    os.rename(e+f[z],e+string_ofid+".jpg")
    z+=1
        
cv2.imwrite("Final.jpg",new_img)    
cv2.imshow("my_project",new_img)
cv2.waitKey(0)
cv2.destroyAllWindows()


