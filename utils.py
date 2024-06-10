import time
import random
import os
import cv2
import pickle
import numpy as np
from collections import Counter

start = time.time()

def object_scanner(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to create a binary image
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the contour with the maximum area (assuming it's the cloth)
    max_contour = max(contours, key=cv2.contourArea)

    # Create a mask for the cloth contour
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, [max_contour], -1, (255), thickness=cv2.FILLED)

    # Apply the mask to the original image
    result = cv2.bitwise_and(image, image, mask=mask)
    return {"result": result, "mask": mask}

def dominant_color(image):

    # Open the pickle file in binary read mode
    with open('./color_recognition_model_svm.pickle', 'rb') as f:
        _model = pickle.load(f)

    # Convert image to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Flatten image array
    pixels = image.reshape((-1, 3))

    # Exclude black pixels
    non_black_pixels = [pixel for pixel in pixels if pixel[0] != 0 or pixel[1] != 0 or pixel[2] != 0]

    # Count occurrences of each color
    color_counts = Counter(map(tuple, non_black_pixels))

    # Get the most common color
    dominant_color = max(color_counts, key=color_counts.get)

    # Assuming your model's predict method expects a 2D array
    result = _model.predict([dominant_color])

    return {"dominant_color": result}


def process_images_in_folder(folder_path):
    dominant_colors_map = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            # Read the image
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path)

            # Scan the image to extract cloth region
            result, mask = object_scanner(image)["result"], object_scanner(image)["mask"]

            # Get the dominant color of the cloth region
            dominant_cloth_color = dominant_color(result)["dominant_color"]

            # Store dominant color in the hashmap
            dominant_colors_map[tuple(dominant_cloth_color)] = filename

    return dominant_colors_map

# Process images in the folder and get dominant colors
dominant_colors_upper = process_images_in_folder(r".\Upper Body")
dominant_colors_lower = process_images_in_folder(r".\Lower Body")

print(dominant_colors_upper)
print(dominant_colors_lower)

dataset = {
    ('Black',) : (('Grey',), ('White',), ('Yellow',)),
    ('Blue',) : (('Yellow',), ('Grey',)),
    ('Brown',) : (('White',), ('Grey',)),
    ('Green',) : (('Yellow',), ('Black',), ('Grey',), ('Blue',)),
    ('Grey',) : (('Black',), ),
    ('Orange',) : (('Black',), ('White',)),
    ('Pink',) : (('Black',), ('Blue',), ('Yellow',)),
    ('Purple',) : (('Black',), ('White',), ('Grey',)),
    ('Red',) : (('Yellow',), ('Black',)),
    ('White',) : (('Black',), ('Grey',), ('Blue',), ('Green',), ('Yellow',), ('Brown',)),
    ('Yellow',) : (('Blue',), ('Black',))
    }

# dataset = {
#     (45, 45, 107) : ((229, 200, 142), (137, 138, 143)), # (Blue - Brown, Grey)
#     (197, 224, 207) : ((229, 200, 142), (22, 22, 20)), # (Green - Brown, Black)
#     (247, 193, 206) : ((22, 22, 20), (38, 59, 90)), # (Pink - Black, Blue)
#     (197, 198, 202) : ((22, 22, 20), ) # (White - Black) 
#     }

def combinations_of_matching_colors(dominant_colors_upper, dominant_colors_lower, dataset):
    combinations = []
    for upper_body in dominant_colors_upper:
        for lower_body in dominant_colors_lower:
            if upper_body in dataset and lower_body in dataset[upper_body]:
                value = (dominant_colors_upper[upper_body], dominant_colors_lower[lower_body])
                combinations.append(value)
    return combinations

possible_outfits = combinations_of_matching_colors(dominant_colors_upper, dominant_colors_lower, dataset)
print(possible_outfits)
todays_outfit = possible_outfits[random.randint(0, len(possible_outfits) - 1)]

todays_outfit_upper = cv2.imread(rf".\Upper Body\{todays_outfit[0]}")
cv2.imshow('For the upper body', todays_outfit_upper)

todays_outfit_lower = cv2.imread(rf".\Lower Body\{todays_outfit[1]}")
cv2.imshow('For the lower body', todays_outfit_lower)

end = time.time()
print("The time of execution of above program is :",
      (end-start) * 10**3, "ms")

cv2.waitKey(0)  
cv2.destroyAllWindows()