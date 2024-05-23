import math

def calculate_relative_position_params(actual_width, focal_length, sensor_width, sensor_height, image_center_x, image_center_y, x1, y1, x2, y2):
    pixel_width = abs(x1 - x2)
    pixel_height = abs(y1 - y2)
    pixel_x = abs(x1 + x2) / 2
    pixel_y = abs(y1 + y2) / 2
    
    if abs(pixel_width - pixel_height) / max(pixel_width, pixel_height) < 0.2:
        pixel_width = (pixel_width + pixel_height) / 2
    else:
        pixel_width = max(pixel_width, pixel_height)
        pixel_x = x2 - pixel_width / 2 if x1 == 0 else x1 + pixel_width / 2
    
    sensor_x = (pixel_x - image_center_x) * sensor_width / (2 * image_center_x)
    theta_x = math.atan(sensor_x / focal_length)
    horizontal_distance = (actual_width * focal_length) / ((pixel_width * sensor_width / (image_center_x * 2)) * math.cos(theta_x))
    
    return abs((horizontal_distance / 1000 - 0.09) / 0.033), math.degrees(theta_x * 4.56)
