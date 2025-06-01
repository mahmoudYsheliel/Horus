from abc import ABC, abstractmethod
from collections import deque
import numpy as np
import cv2

class FilterBase(ABC):
    @abstractmethod
    def apply_filter(self):
        pass
    
    @abstractmethod
    def calc_out_conf(self):
        pass


class bilateral_filter(FilterBase):
    def __init__(self, kernal_size=3, sigma_color=5, sigma_space=2):
        self.kernal_size = kernal_size
        self.sigma_color = sigma_color
        self.sigma_space = sigma_space

    def apply_filter(self, frame):
        return cv2.bilateralFilter(frame, self.kernal_size, self.sigma_color, self.sigma_space)
    
    def calc_out_conf(self,initial_width,intial_height,initial_conf):
        return initial_width, intial_height, initial_conf


class gaussian_blur(FilterBase):
    def __init__(self, kernal_width=5, kernal_height=5, sigmaX=0.25, sigmaY=0.25):
        self.kernal_width = kernal_width
        self.kernal_height = kernal_height
        self.sigmaX = sigmaX
        self.sigmaY = sigmaY

    def apply_filter(self, frame):
        return cv2.GaussianBlur(frame, (self.kernal_width, self.kernal_height), sigmaX=self.sigmaX, sigmaY=self.sigmaY)

    def calc_out_conf(self,initial_width,intial_height,initial_conf):
        return initial_width, intial_height, initial_conf

class median_blur(FilterBase):
    def __init__(self, kernal_size=5):
        self.kernal_size = kernal_size

    def apply_filter(self, frame):
        return cv2.medianBlur(frame, self.kernal_size)
    
    def calc_out_conf(self,initial_width,intial_height,initial_conf):
        return initial_width, intial_height, initial_conf


class crop_filter(FilterBase):
    def __init__(self, x=0, y=0, w=640, h=480):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def apply_filter(self, frame):
        try:
            shape = getattr(frame, 'shape', None)
            if shape is None:
                raise TypeError("Frame has no shape attribute")
            if len(shape) == 2:
                height, width = shape
            elif len(shape) == 3:
                height, width = shape[:2]
            else:
                raise ValueError("Unsupported frame shape")
        except Exception as e:
            print(f"Error getting frame size: {e}")

        if self.x < 0 or self.y < 0 or self.w < 0 or self.h < 0:
            print('One or more Target Parameters are less than 0')
            return frame
        if self.x + self.w > width or self.y + self.h > height:
            print('One or more Target Parameters excceeded the limit')
            return frame
        return frame[self.y:self.y + self.h, self.x:self.x + self.w]
    
    def calc_out_conf(self,initial_width,intial_height,initial_conf):
        return self.w, self.h, initial_conf


class resize_filter(FilterBase):
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

    def apply_filter(self, frame):
        if self.w < 0 or self.h < 0:
            print('One or more Target Parameters are less than 0')
            return frame
        return cv2.resize(frame, (int(self.w), int(self.h)))
    
    def calc_out_conf(self,initial_width,intial_height,initial_conf):
        return self.w, self.h, initial_conf


class motion_filter(FilterBase):
    def __init__(self, frame_count=30,image_format = 'bgr24',drop_rate= 5,threshold=20, frame_width=640,frame_height=480):
        self.frame_diff_buffer = deque(maxlen=frame_count)
        self.frame_number = 0
        self.drop_rate = drop_rate
        self.threshold = threshold
        self.image_format = image_format
        self.summed_frame_diff =np.zeros((frame_height, frame_width,3), dtype=np.uint8)
        self.prev_gray = np.zeros((frame_height, frame_width), dtype=np.uint8)

    def apply_filter(self, frame):
        self.frame_number = self.frame_number + 1
        if self.frame_number % int(self.drop_rate) > 0:
            return self.summed_frame_diff

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        mask = gray > self.threshold
        gray = gray * mask.astype(np.uint8)
        frame_diff = cv2.absdiff(self.prev_gray, gray)

        if self.image_format == 'bgr24':
            frame_diff = cv2.applyColorMap(frame_diff, cv2.COLORMAP_JET)


        self.frame_diff_buffer.append(frame_diff)
        self.summed_frame_diff = np.zeros_like(frame_diff)
        for diff in self.frame_diff_buffer:
            self.summed_frame_diff += diff
        self.prev_gray = gray
        return self.summed_frame_diff
    
    def calc_out_conf(self,initial_width,intial_height,initial_conf):
        return self.w, self.h, self.image_format







default_filter_inputs_map = {
    'bilateral_filter': {'kernal_size': 3, 'sigma_color': 5, 'sigma_space': 2},
    'crop_filter': {'x': 0, 'y': 0, 'w': 640, 'h': 480},
    'gaussian_blur': {'kernal_width': 5, 'kernal_height': 5, 'sigmaX': 0.25, 'sigmaY': 0.25},
    'median_blur': {'kernal_size': 5},
    'resize_filter': {'w': 640, 'h': 480},
    'motion_filter': {'frame_count':30,'image_format':'bgr24','drop_rate': 5,'threshold':20, 'frame_width':640,'frame_height':480}
}

class_map = {
    'bilateral_filter': bilateral_filter,
    'crop_filter': crop_filter,
    'gaussian_blur': gaussian_blur,
    'median_blur': median_blur,
    'resize_filter': resize_filter,
    'motion_filter': motion_filter
}
