import cv2

original_img = cv2.imread('photo2.jpg')
mask = cv2.imread('mask.png')

gray_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
ret, thresh_mask = cv2.threshold(gray_mask, 180, 255, cv2.THRESH_BINARY)

dst = cv2.inpaint(original_img, thresh_mask, 10, cv2.INPAINT_TELEA)

b, g, r = cv2.split(dst)

a = thresh_mask
result = thresh_mask

cv2.imshow("Original Image", original_img)
cv2.imshow("Result", result)
cv2.imwrite("result.png", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
#
# cap = cv2.VideoCapture(0)
# cap.set(3, 500)
# cap.set(4, 300)
#
# while True:
#     success, img = cap.read()
#     cv2.imshow('Result', img)
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break