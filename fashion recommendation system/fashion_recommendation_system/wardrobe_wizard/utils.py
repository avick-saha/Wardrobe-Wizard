import os
import cv2
import numpy as np
from collections import Counter
import pickle
import json
from django.conf import settings
from pathlib import Path

def object_scanner(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contours, key=cv2.contourArea)
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, [max_contour], -1, (255), thickness=cv2.FILLED)

    result = cv2.bitwise_and(image, image, mask=mask)
    return {"result": result, "mask": mask}

def dominant_color(image):
    model_path = Path(settings.BASE_DIR) / 'color_recognition_model_svm.pickle'
    
    print(f"Checking if model file exists at: {model_path}")  # Debugging statement
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found at {model_path}")
    
    with open(model_path, 'rb') as f:
        _model = pickle.load(f)
        
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixels = image.reshape((-1, 3))
    non_black_pixels = [pixel for pixel in pixels if pixel[0] != 0 or pixel[1] != 0 or pixel[2] != 0]
    color_counts = Counter(map(tuple, non_black_pixels))
    dominant_color = max(color_counts, key=color_counts.get)

    result = _model.predict([dominant_color])

    return {"dominant_color": result}


def process_images_in_folder(queryset, image_field_name):
    dominant_colors_map = {}

    for obj in queryset:
        image_file = getattr(obj, image_field_name)
        image_path = image_file.path
        image = cv2.imread(image_path)

        scan_result = object_scanner(image)
        result = scan_result["result"]
        dominant_cloth_color = dominant_color(result)["dominant_color"]
        dominant_colors_map[tuple(dominant_cloth_color)] = obj

    return dominant_colors_map

def combinations_of_matching_colors(dominant_colors_upper, dominant_colors_lower):
    dataset = {
        ('Black',): (('Grey',), ('White',), ('Yellow',)),
        ('Blue',): (('Yellow',), ('Grey',)),
        ('Brown',): (('White',), ('Grey',)),
        ('Green',): (('Yellow',), ('Black',), ('Grey',), ('Blue',)),
        ('Grey',): (('Black',),),
        ('Orange',): (('Black',), ('White',)),
        ('Pink',): (('Black',), ('Blue',), ('Yellow',)),
        ('Purple',): (('Black',), ('White',), ('Grey',)),
        ('Red',): (('Yellow',), ('Black',)),
        ('White',): (('Black',), ('Grey',), ('Blue',), ('Green',), ('Yellow',), ('Brown',)),
        ('Yellow',): (('Blue',), ('Black',))
    }

    combinations = []
    for upper_color, upper_obj in dominant_colors_upper.items():
        for lower_color, lower_obj in dominant_colors_lower.items():
            if upper_color in dataset and lower_color in dataset[upper_color]:
                combinations.append((upper_obj, lower_obj))

    return combinations