import cv2
import numpy as np

# Load image and convert to grayscale
image = cv2.imread('111.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding to remove noise
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Find contours and sort by area
contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
contours = sorted(contours, key=cv2.contourArea, reverse=True)

# Find largest contour and its bounding rectangle
largest_contour = contours[0]
x, y, w, h = cv2.boundingRect(largest_contour)

# Crop image to bounding rectangle
crop = image[y:y+h, x:x+w]

# Resize image
resized = cv2.resize(crop, (500, 500))

# Save output image
cv2.imwrite('output.jpg', resized)