import cv2
import numpy as np
import matplotlib.pyplot as plt
import json

def run_return_mask(image_path, lower_custom=None, upper_custom=None):
    print("blue started")
    # Load the image
    #image_path = "accentuated_outputtestCropImage5.jpeg"  # Update with your image path
    #image = cv2.imread(image_path)
    image = image_path
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Step 1: Background Removal using GrabCut
    gc_mask = np.zeros(image.shape[:2], np.uint8)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    rect = (10, 10, image.shape[1] - 20, image.shape[0] - 20)
    cv2.grabCut(image, gc_mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
    gc_mask = np.where((gc_mask == 2) | (gc_mask == 0), 0, 1).astype("uint8")
    bg_removed = image * gc_mask[:, :, np.newaxis]

    # Step 2: Convert to HSV and Apply Custom Filter
    hsv = cv2.cvtColor(bg_removed, cv2.COLOR_BGR2HSV)
    #lower_custom = np.array([90, 50, 50])
    #upper_custom = np.array([140, 255, 255])
    lower_custom = np.array(lower_custom if lower_custom is not None else [90, 50, 50])
    upper_custom = np.array(upper_custom if upper_custom is not None else [140, 255, 255])
    mask = cv2.inRange(hsv, lower_custom, upper_custom)

    # Step 3: Morphological Operations (Dilation + Erosion)
    kernel = np.ones((5, 5), np.uint8)
    dilated_mask = cv2.dilate(mask, kernel, iterations=2)
    eroded_mask = cv2.erode(dilated_mask, kernel, iterations=1)

    # Step 4: Apply Final Mask
    final_result = cv2.bitwise_and(image, image, mask=eroded_mask)
    
    return final_result

def run(image_path, lower_custom=None, upper_custom=None):
    print("blue started")
    # Load the image
    #image_path = "accentuated_outputtestCropImage5.jpeg"  # Update with your image path
    #image = cv2.imread(image_path)
    image = image_path
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Step 1: Background Removal using GrabCut
    gc_mask = np.zeros(image.shape[:2], np.uint8)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    rect = (10, 10, image.shape[1] - 20, image.shape[0] - 20)
    cv2.grabCut(image, gc_mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
    gc_mask = np.where((gc_mask == 2) | (gc_mask == 0), 0, 1).astype("uint8")
    bg_removed = image * gc_mask[:, :, np.newaxis]

    # Step 2: Convert to HSV and Apply Custom Filter
    hsv = cv2.cvtColor(bg_removed, cv2.COLOR_BGR2HSV)
    #lower_custom = np.array([90, 50, 50])
    #upper_custom = np.array([140, 255, 255])
    with open("config.json", "r") as f:
                config = json.load(f)
                lower_custom = config.get("blue_hsv_values", [])
    upper_custom = lower_custom[3:]
    lower_custom = lower_custom[:3]
    print('lower_custom=')
    print(lower_custom)
    print('upper_custom=')
    print(upper_custom)
    lower_custom = np.array(lower_custom if lower_custom is not None else [90, 50, 50])
    upper_custom = np.array(upper_custom if upper_custom is not None else [140, 255, 255])
    mask = cv2.inRange(hsv, lower_custom, upper_custom)

    # Step 3: Morphological Operations (Dilation + Erosion)
    kernel = np.ones((5, 5), np.uint8)
    dilated_mask = cv2.dilate(mask, kernel, iterations=2)
    eroded_mask = cv2.erode(dilated_mask, kernel, iterations=1)

    # Step 4: Apply Final Mask
    final_result = cv2.bitwise_and(image, image, mask=eroded_mask)
    # Convert images for display
    bg_removed_rgb = cv2.cvtColor(bg_removed, cv2.COLOR_BGR2RGB)
    final_result_rgb = cv2.cvtColor(final_result, cv2.COLOR_BGR2RGB)


    ############################ Extra on 10 march 25
    # Count pixsels
    # Count the number of white pixels (255 represents detected regions)
    pixel_area = np.count_nonzero(dilated_mask == 255)
    total_pixels = dilated_mask.shape[0] * mask.shape[1]
    print('Total pixels='+str(total_pixels))
    print('Pixel Area of masked region =' + str(pixel_area))
    ############################
    
    # Plot the results
    '''fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    axes[0].imshow(image_rgb)
    axes[0].set_title("Original Image")
    axes[0].axis("off")

    axes[1].imshow(bg_removed_rgb)
    axes[1].set_title("stage1")
    axes[1].axis("off")

    axes[2].imshow(dilated_mask, cmap="gray")
    axes[2].set_title("Dilated Mask")
    axes[2].axis("off")

    axes[3].imshow(final_result_rgb)
    axes[3].set_title("Final Filtered Image")
    axes[3].axis("off")

    plt.show()'''
    
    #cv2.imwrite('outputs/blue_img.jpg',final_result_rgb)
    print("blue completed")
    
    return pixel_area

#run('test_Video_withModel/test2_detected_cropped3.jpeg')
