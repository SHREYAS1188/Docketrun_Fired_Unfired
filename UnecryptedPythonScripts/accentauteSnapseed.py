import cv2
import numpy as np
import time
import math

def apply_accentuate(image,fimg_name):
    print('Accentaute Started')
    # Convert to LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to enhance contrast
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(3, 3))
    l = clahe.apply(l)
    
    # Merge channels back
    lab_enhanced = cv2.merge([l, a, b])
    contrast_enhanced = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)
    
    #cv2.imshow('goku',contrast_enhanced)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    
    # Apply unsharp mask for sharpness
    gaussian = cv2.GaussianBlur(contrast_enhanced, (0, 0), 3)
    sharp_image = cv2.addWeighted(contrast_enhanced, 1.5, gaussian, -0.5, 0)
    
    # Convert to HSV and boost saturation
    hsv = cv2.cvtColor(sharp_image, cv2.COLOR_BGR2HSV).astype(np.float32)
    h, s, v = cv2.split(hsv)
    s = np.clip(s * 1.5, 0, 255)  # Increase saturation
    hsv_enhanced = cv2.merge([h, s, v])
    final_image = cv2.cvtColor(hsv_enhanced.astype(np.uint8), cv2.COLOR_HSV2BGR)
    #fimg_name = str(math.trunc(time.time()))
    cv2.imwrite('output/'+fimg_name+'.jpg',final_image)
    print('Accentaute Completed')
    return final_image

'''
# Load image
inputfilaname = "testCropImage7.jpeg"
image = cv2.imread(inputfilaname)

# Apply Accentuate effect twice
enhanced_image = apply_accentuate(image)
enhanced_image = apply_accentuate(enhanced_image)

# Show results
cv2.imshow("Original", image)

cv2.imshow("Accentuated", enhanced_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save result
cv2.imwrite("accentuated_output_2_"+inputfilaname, enhanced_image)
'''
    