import numpy as np
import cv2

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FPS, 30)

num_frame = 0

_, frame = cam.read()
avg_frames = np.float32(frame)

img1 = cv2.imread("samolot01.jpg", 0)  # queryImage
img2 = cv2.imread("20-2012.jpg")  # trainImage

brisk = cv2.BRISK_create(thresh=100, octaves=0, patternScale=1)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
kp2, des2 = brisk.detectAndCompute(img2, None)

#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#avi = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

while True:
    _, frame = cam.read()
    #cv2.accumulateWeighted(frame, avg_frames, 1/15)
    #cvt_avg_frames = cv2.convertScaleAbs(avg_frames)

    # find the keypoints and descriptors with BRISK
    kp1, des1 = brisk.detectAndCompute(frame, None)

    # Match descriptors.
    matches = bf.match(des1, des2)

    # Sort them in the order of their distance.
    matches = sorted(matches, key=lambda x: x.distance)

    # Draw matches.
    img3 = cv2.drawMatches(frame, kp1, img2, kp2, matches[:100], None, flags=2)

    cv2.imshow('frame', img3)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #cv2.imwrite('images\camera' + str(num_frame) + '.png', frame)
    #cv2.imwrite('images\cameraAcc' + str(num_frame) + '.png', cvt_avg_frames)

    num_frame += 1

cam.release()
#avi.release()
cv2.destroyAllWindows()
