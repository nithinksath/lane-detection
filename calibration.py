import numpy as np
import cv2
import glob
import sys
#sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)
#print(objp)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob("*.jpg")
#print(images)

for fname in images:
    img = cv2.imread(fname)
    #img1=cv2.imread('frame487.jpg')
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7,7),None)
    print(ret)
	#print(corners)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        cv2.drawChessboardCorners(img, (7,7), corners2, ret)
        #cv2.imshow('img', img)
        #print(img)
        #cv2.waitKey(3)
		
cv2.destroyAllWindows()
#print(objpoints,imgpoints)
img1=cv2.imread('frame1.jpg')
gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
#print(rvecs)
#np.savetxt('rotationalmatrix.txt',rvecs)
#np.savetxt('translationmatrix.txt',tvecs)
np.savetxt('cameramatrix.txt',mtx)
np.savetxt('distortioncoefficient.txt',dist)
fovx, fovy, focalLength, principalPoint, aspectRatio=cv2.calibrationMatrixValues(mtx,gray1.shape[::-1],44.5,109)
print(focalLength)
img = cv2.imread('frame7.jpg')
h,w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
np.savetxt('optimalcameramatrix.txt',newcameramtx)
# undistort
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
#cv2.imwrite('calibresult.png', dst)

