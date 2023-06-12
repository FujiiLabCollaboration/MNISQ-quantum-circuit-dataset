import cv2
import numpy as np


def decomposite_to_RGB(data_row: np.ndarray) -> np.ndarray:
    return np.array(
        [
            [
                [
                    data_row[x * 32 + y] / 255.0,
                    data_row[1024 + x * 32 + y] / 255.0,
                    data_row[2048 + x * 32 + y] / 255.0,
                ]
                for y in range(32)
            ]
            for x in range(32)
        ],
        np.float32,
    )


def to_grayscale(RGB_data: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(RGB_data, cv2.COLOR_RGB2GRAY)
