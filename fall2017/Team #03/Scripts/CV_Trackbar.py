import numpy as np
import cv2

cap = cv2.VideoCapture(0)
# cap.set(3,1280)
# cap.set(4,720)

# create trackbars for color change
# create trackbars for num erosion and dilations
def nothing(x): pass
# cv2.namedWindow('Settings', flags=cv2.WINDOW_NORMAL)
# cv2.createTrackbar('H_low','Settings',0,255,nothing)
# cv2.createTrackbar('H_high','Settings',0,255,nothing)
# cv2.createTrackbar('S_low','Settings',0,255,nothing)
# cv2.createTrackbar('S_high','Settings',0,255,nothing)
# cv2.createTrackbar('V_low','Settings',0,255,nothing)
# cv2.createTrackbar('V_high','Settings',0,255,nothing)
# cv2.createTrackbar('#erode','Settings',1,10,nothing)
# cv2.createTrackbar('#dilate','Settings',1,10,nothing)
# cv2.createTrackbar('min_contour_area','Settings',300,2000,nothing)
# # cv2.createTrackbar('ksizex','Settings',7,100,nothing)
# # cv2.createTrackbar('ksizey','Settings',7,100,nothing)
# cv2.createTrackbar('ksize','Settings',3,100,nothing)

cv2.namedWindow('Settings', flags=cv2.WINDOW_NORMAL)
cv2.createTrackbar('ksize','Settings',1,100,nothing)
cv2.createTrackbar('H_low','Settings',0,255,nothing)
cv2.createTrackbar('H_high','Settings',255,255,nothing)
cv2.createTrackbar('S_low','Settings',0,255,nothing)
cv2.createTrackbar('S_high','Settings',255,255,nothing)
cv2.createTrackbar('V_low','Settings',0,255,nothing)
cv2.createTrackbar('V_high','Settings',255,255,nothing)
cv2.createTrackbar('#erode','Settings',0,10,nothing)
cv2.createTrackbar('#dilate','Settings',0,10,nothing)
cv2.createTrackbar('min_contour_area','Settings',1000,10000,nothing)
# cv2.createTrackbar('ksizex','Settings',7,100,nothing)
# cv2.createTrackbar('ksizey','Settings',7,100,nothing)


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    original_frame = frame.copy()
    # Our operations on the frame come here
    if not ret:
        print('ERROR READING FROM WEBCAM')
        break
        
    min_contour_area = cv2.getTrackbarPos('min_contour_area', 'Settings')#Minimum radius of a contour
    hl = cv2.getTrackbarPos('H_low','Settings')#HSV Settings
    hh = cv2.getTrackbarPos('H_high','Settings')
    sl = cv2.getTrackbarPos('S_low','Settings')
    sh = cv2.getTrackbarPos('S_high','Settings')
    vl = cv2.getTrackbarPos('V_low','Settings')
    vh = cv2.getTrackbarPos('V_high','Settings')
    er = cv2.getTrackbarPos('#erode', 'Settings')#Morphological transformation settings
    di = cv2.getTrackbarPos('#dilate', 'Settings')
    # ksize = (cv2.getTrackbarPos('ksizex', 'Settings')*2-1,cv2.getTrackbarPos('ksizey', 'Settings')*2-1)#Gaussian blur settings
    ksize = (cv2.getTrackbarPos('ksize', 'Settings')*2+1)#Median blur settings
    
    lower_hsv = np.array([hl,sl,vl])
    upper_hsv = np.array([hh,sh,vh])
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blur_frame = cv2.cv2.medianBlur(hsv_frame,ksize)  # blur to reduce noise
    color_filter_mask = cv2.inRange(blur_frame, lower_hsv, upper_hsv)
    erode_mask = cv2.erode(color_filter_mask, None, iterations=er)
    dilate_mask = cv2.dilate(erode_mask, None, iterations=di)
    frame = cv2.medianBlur(frame,ksize)
    contours = cv2.bitwise_and(frame,frame,mask=dilate_mask)
    cnts = cv2.findContours(dilate_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    for cnt in cnts:
        if cv2.contourArea(cnt) > min_contour_area:
            cv2.drawContours(contours, [cnt], 0, (0,255,0), 3)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(dilate_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroic = max(cnts, key=cv2.contourArea)
        c = max(cnts, key=cv2.contourArea)
        # print cv2.contourArea(c)
        if cv2.contourArea(c) >= min_contour_area:
            M = cv2.moments(c)
            # print cv2.contourArea(c)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    # Display the resulting frame
    # cv2.imshow('original_frame', original_frame)
    # cv2.imshow('hsv_frame', hsv_frame)
    # cv2.imshow('blur_frame', blur_frame)
    # cv2.imshow('color_filter_mask', color_filter_mask)
    # cv2.imshow('erode_mask', erode_mask)
    # cv2.imshow('dilate_mask', dilate_mask)
    cv2.imshow('contours',contours)
    cv2.imshow('final_result',frame)


    #cv2.imshow('mask',mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('s'):
        print lower_hsv,upper_hsv,er,di,ksize,min_rad

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

