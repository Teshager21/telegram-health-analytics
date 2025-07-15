# import os
# import pytest
import sys


import yolo_image_detection as yolo
from unittest.mock import patch, MagicMock

sys.path.append("src/etl")
# Import the functions to test from your module, e.g.
# from src.etl.yolo_image_detection import is_image, batch, detect_objects

# For example purposes, assuming your script is
# named yolo_image_detection.py and is in src/etl/


def test_is_image_with_valid_image(tmp_path):
    # Create a small valid image file
    img_path = tmp_path / "test.jpg"
    from PIL import Image

    img = Image.new("RGB", (10, 10), color="red")
    img.save(img_path)

    assert yolo.is_image(str(img_path)) is True


def test_is_image_with_invalid_image(tmp_path):
    # Create a dummy text file with .jpg extension (invalid image)
    fake_img_path = tmp_path / "fake.jpg"
    fake_img_path.write_text("not really an image")

    assert yolo.is_image(str(fake_img_path)) is False


def test_batch_function():
    data = list(range(10))
    batches = list(yolo.batch(data, n=3))

    # Should split into 4 batches: 3, 3, 3, 1 elements
    assert batches == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]


@patch("yolo_image_detection.model")
def test_detect_objects(mock_model):
    # Mock the YOLO model return
    mock_result = MagicMock()
    mock_result.boxes.data.tolist.return_value = [
        [0, 0, 0, 0, 0.9, 1],  # x1,y1,x2,y2,conf,class_id
        [0, 0, 0, 0, 0.75, 2],
    ]
    mock_model.return_value = [mock_result]
    mock_model.names = {1: "bottle", 2: "cup"}

    detections = yolo.detect_objects("dummy_path.jpg")
    expected = [("bottle", 0.9), ("cup", 0.75)]

    assert detections == expected


@patch("yolo_image_detection.execute_values")
@patch("yolo_image_detection.psycopg2.connect")
@patch("yolo_image_detection.detect_objects")
@patch("yolo_image_detection.is_image")
def test_main_flow(
    mock_is_image, mock_detect_objects, mock_connect, mock_execute_values, tmp_path
):
    # Setup mocks
    mock_is_image.return_value = True
    mock_detect_objects.return_value = [("bottle", 0.85)]
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Create a fake directory with one image file
    images_dir = tmp_path / "telegram_images" / "2025-07-13"
    images_dir.mkdir(parents=True)
    img_path = images_dir / "12345.jpg"
    img_path.write_text("fake image content")

    # Patch os.walk and images_dir
    with patch("yolo_image_detection.os.walk") as mock_walk, patch(
        "yolo_image_detection.images_dir", str(images_dir)
    ):
        mock_walk.return_value = [(str(images_dir), [], ["12345.jpg"])]

        from yolo_image_detection import main

        main()

    # Assert DB calls
    mock_connect.assert_called_once()
    mock_cursor.execute.assert_not_called()  # execute_values used instead
    mock_execute_values.assert_called()
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()
