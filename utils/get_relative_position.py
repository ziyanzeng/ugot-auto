import math
from utils.parse_results import parse_detection_results
import config
import numpy as np
from shared_data import SharedData
from logger import logger

# 函数 get_single_relative_pos 计算给定检测结果中某一类目标的相对位置
def get_single_relative_pos(detections, class_name):
    # 解析检测结果，返回边界框、置信度分数和类别信息
    boxes, scores, classes = parse_detection_results(detections)
    
    # 如果没有检测到任何目标，返回默认值
    if len(scores) == 0:
        return 0, 0, None, 0, 0
    
    # 获取指定类别的所有索引
    class_indices = [i for i, c in enumerate(classes) if config.CLASS_LABELS[int(c)] == class_name]
    
    # 如果没有找到指定类别的目标，返回默认值
    if not class_indices:
        return 0, 0, None, 0, 0
    
    # 找到具有最高分数的目标的索引
    max_index = max(class_indices, key=lambda i: scores[i])
    
    # 获取该目标的边界框坐标
    box = boxes[max_index]
    x1, y1, x2, y2 = map(int, box)
    
    # 根据目标类别选择实际宽度
    actual_width = config.BALL_DIAMETER if class_name in ["ping-pong", "ping-pong-partial"] else config.GOAL_WIDTH
    
    # 计算目标的距离和角度
    distance, angle = calculate_relative_position_params(
        actual_width, 
        config.CAM_FOCAL, 
        config.SENSOR_WIDTH, 
        config.SENSOR_HEIGHT, 
        SharedData.shared_data["frame_width"] / 2, 
        SharedData.shared_data["frame_height"] / 2, 
        x1, y1, x2, y2
    )
    
    # 返回距离、角度、边界框、置信度分数和类别
    return distance, angle, box, scores[max_index], classes[max_index]

# 函数 calculate_relative_position_params 计算目标的相对位置参数（距离和角度）
def calculate_relative_position_params(actual_width, focal_length, sensor_width, sensor_height, image_center_x, image_center_y, x1, y1, x2, y2):
    # 计算目标的像素宽度和高度
    pixel_width = abs(x1 - x2)
    pixel_height = abs(y1 - y2)
    
    # 计算目标的像素中心点
    pixel_x = abs(x1 + x2) / 2
    pixel_y = abs(y1 + y2) / 2
    
    # 如果目标的宽高比接近 1，则取宽高的平均值作为宽度
    if abs(pixel_width - pixel_height) / max(pixel_width, pixel_height) < 0.2:
        pixel_width = (pixel_width + pixel_height) / 2
    else:
        # 否则，取较大的值作为宽度，并重新计算中心点
        pixel_width = max(pixel_width, pixel_height)
        pixel_x = x2 - pixel_width / 2 if x1 == 0 else x1 + pixel_width / 2
    
    # 将像素坐标转换为传感器坐标
    sensor_x = (pixel_x - image_center_x) * sensor_width / (2 * image_center_x)
    
    # 计算水平角度
    theta_x = math.atan(sensor_x / focal_length)
    
    # 计算水平距离
    horizontal_distance = (actual_width * focal_length) / ((pixel_width * sensor_width / (image_center_x * 2)) * math.cos(theta_x))
    
    # 检查目标是否在图像的角落
    if (x1 < 5 or x2 > image_center_x * 2 - 5) and (y1 > image_center_y * 2 - 5 or y2 > image_center_y * 2 - 5):
        # 如果在角落，返回0距离和调整后的角度
        return 0, math.degrees(theta_x * 4.56)
    
    # 返回计算的相对距离和角度
    return abs((horizontal_distance / 1000 - 0.09) / 0.033), math.degrees(theta_x * 4.56)