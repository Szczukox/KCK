import cv2

img20 = cv2.imread("zdjecie20zl2.jpg")
img50 = cv2.imread("zdjecie50zl2.jpg")
img100 = cv2.imread("zdjecie100zl2.jpg")
img_puste = cv2.imread("zdjecie_puste.jpg")

img = cv2.imread("test20_0.jpg")

brisk = cv2.BRISK_create(thresh=100, octaves=0, patternScale=1)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
kp20, des20 = brisk.detectAndCompute(img20, None)
kp50, des50 = brisk.detectAndCompute(img50, None)
kp100, des100 = brisk.detectAndCompute(img100, None)
kp_puste, des_puste = brisk.detectAndCompute(img_puste, None)

kp, des = brisk.detectAndCompute(img, None)

# Match descriptors.
matches20 = bf.match(des20, des)
matches50 = bf.match(des50, des)
matches100 = bf.match(des100, des)
matches_puste = bf.match(des_puste, des)

# Sort them in the order of their distance.
matches20 = sorted(matches20, key=lambda x: x.distance)
matches50 = sorted(matches50, key=lambda x: x.distance)
matches100 = sorted(matches100, key=lambda x: x.distance)
matches_puste = sorted(matches_puste, key=lambda x: x.distance)

# Draw matches.
if len(matches20) > len(matches50) and len(matches20) > len(matches100):
    img3 = cv2.drawMatches(img20, kp20, img, kp, matches20, None, flags=2)
    print("*** WYKRYTO 20ZŁ ***")
elif len(matches50) > len(matches20) and len(matches50) > len(matches100):
    img3 = cv2.drawMatches(img50, kp50, img, kp, matches50, None, flags=2)
    print("*** WYKRYTO 50ZŁ ***")
elif len(matches100) > len(matches20) and len(matches100) > len(matches50):
    img3 = cv2.drawMatches(img100, kp100, img, kp, matches100, None, flags=2)
    print("*** WYKRYTO 100ZŁ ***")
else:
    img3 = cv2.drawMatches(img_puste, kp_puste, img, kp, matches_puste, None, flags=2)
    print("*** NIE WYKRYTO NIC ***")

while True:
    cv2.imshow('frame', img3)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("\n")
        print("*** PUNKTY CHARAKTERYSTYCZNE: ***")
        print("BANKNOT\t\tLICZBA")
        print("20ZŁ: \t\t", len(matches20))
        print("50ZŁ: \t\t", len(matches50))
        print("100ZŁ: \t\t", len(matches100))
        break

cv2.destroyAllWindows()
