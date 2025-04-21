import cv2
import numpy as np
import matplotlib.pyplot as plt
import json


def run_return_mask_grey(image_path, lower_custom=None, upper_custom=None):
    print('Grey Started')
    # Load the image
    # image_path = "accentuated_outputtestCropImage7.jpeg"  # Update with your image path
    #image = cv2.imread(image_path)
    image = image_path
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Step 1: Background Removal using GrabCut
    gc_mask = np.zeros(image.shape[:2], np.uint8)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    rect = (55, 55, image.shape[1] - 20, image.shape[0] - 20)
    cv2.grabCut(image, gc_mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
    gc_mask = np.where((gc_mask == 2) | (gc_mask == 0), 0, 1).astype("uint8")
    bg_removed = image * gc_mask[:, :, np.newaxis]

    # Step 2: Convert to HSV and Apply Custom Filter
    hsv = cv2.cvtColor(bg_removed, cv2.COLOR_BGR2HSV)
    #lower_custom = np.array([104, 0, 0])
    #upper_custom = np.array([127, 76, 177])
    lower_custom = np.array(lower_custom if lower_custom is not None else [104, 0, 0])
    upper_custom = np.array(upper_custom if upper_custom is not None else [127, 76, 177])

    white_remover_lower_custom = np.array([37,26,0])
    white_remover_upper_custom = np.array([112,255,196])
    mask = cv2.inRange(hsv, lower_custom, upper_custom)
    white_mask = cv2.inRange(hsv, white_remover_lower_custom, white_remover_upper_custom)

    ##############

    # Find contours of white regions in the mask
    contours, _ = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Define the minimum white area threshold (adjust as needed)
    min_white_area = 50 

    # Filter out small white regions
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_white_area:
            cv2.drawContours(white_mask, [cnt], -1, 0, thickness=cv2.FILLED)  # Remove small regions


    ###################

    # combined_mask = cv2.bitwise_or(mask, white_mask)
    # Step 3: Morphological Operations (Dilation + Erosion)
    kernel = np.ones((5, 5), np.uint8)
    # here we can use white mask then mask 
    dilated_mask = cv2.dilate(mask, kernel, iterations=2)
    eroded_mask = cv2.erode(dilated_mask, kernel, iterations=1)

    # Step 4: Apply Final Mask
    final_result = cv2.bitwise_and(image, image, mask=eroded_mask)
    
    bg_removed_rgb = cv2.cvtColor(bg_removed, cv2.COLOR_BGR2RGB)
    final_result_rgb = cv2.cvtColor(final_result, cv2.COLOR_BGR2RGB)
    # Plot the results
    '''fig, axes = plt.subplots(1, 6, figsize=(20, 5))
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

    axes[4].imshow(hsv)
    axes[4].set_title("hsv Image")
    axes[4].axis("off")

    axes[5].imshow(white_mask)
    axes[5].set_title("white mask")
    axes[5].axis("off")

    plt.show()
    
    cv2.imshow('goku',final_result_rgb)
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''
    
    #cv2.imwrite('testing_outputs/grey_img.jpg',final_result_rgb)
    print('Grey Completed')
    
    return final_result

def run(image_path, lower_custom=None, upper_custom=None):
    print('Grey Started')
    # Load the image
    # image_path = "accentuated_outputtestCropImage7.jpeg"  # Update with your image path
    #image = cv2.imread(image_path)
    image = image_path
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Step 1: Background Removal using GrabCut
    gc_mask = np.zeros(image.shape[:2], np.uint8)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    rect = (35, 35, image.shape[1] - 20, image.shape[0] - 20)
    cv2.grabCut(image, gc_mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
    gc_mask = np.where((gc_mask == 2) | (gc_mask == 0), 0, 1).astype("uint8")
    bg_removed = image * gc_mask[:, :, np.newaxis]

    # Step 2: Convert to HSV and Apply Custom Filter
    hsv = cv2.cvtColor(bg_removed, cv2.COLOR_BGR2HSV)
    #lower_custom = np.array([104, 0, 0])
    #upper_custom = np.array([127, 76, 177])
    
    with open("config.json", "r") as f:
                config = json.load(f)
                lower_custom = config.get("white_hsv_values", [])
    upper_custom = lower_custom[3:]
    lower_custom = lower_custom[:3]
    print('lower_custom=')
    print(lower_custom)
    print('upper_custom=')
    print(upper_custom)
    lower_custom = np.array(lower_custom if lower_custom is not None else [104, 0, 0])
    upper_custom = np.array(upper_custom if upper_custom is not None else [127, 76, 177])

    white_remover_lower_custom = np.array([37,26,0])
    white_remover_upper_custom = np.array([112,255,196])
    mask = cv2.inRange(hsv, lower_custom, upper_custom)
    white_mask = cv2.inRange(hsv, white_remover_lower_custom, white_remover_upper_custom)

    ##############

    # Find contours of white regions in the mask
    contours, _ = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Define the minimum white area threshold (adjust as needed)
    min_white_area = 50 

    # Filter out small white regions
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_white_area:
            cv2.drawContours(white_mask, [cnt], -1, 0, thickness=cv2.FILLED)  # Remove small regions


    ###################

    # combined_mask = cv2.bitwise_or(mask, white_mask)
    # Step 3: Morphological Operations (Dilation + Erosion)
    kernel = np.ones((5, 5), np.uint8)
    # here we can use white mask then mask 
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
    '''
    fig, axes = plt.subplots(1, 6, figsize=(20, 5))
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

    axes[4].imshow(hsv)
    axes[4].set_title("hsv Image")
    axes[4].axis("off")

    axes[5].imshow(white_mask)
    axes[5].set_title("white mask")
    axes[5].axis("off")

    plt.show()
    
    cv2.imshow('goku',final_result_rgb)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    #cv2.imwrite('testing_outputs/grey_img.jpg',final_result_rgb)
    '''
    print('Grey Completed')
    
    return pixel_area
    
    
    
#run('test_Video_withModel/test2_detected_cropped3.jpeg')
