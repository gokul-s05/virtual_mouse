# Virtual Mouse Control Using Hand Gestures

Control your computer's mouse using hand gestures captured through your webcam. This project uses MediaPipe for hand tracking and supports various mouse control gestures.

## Features

- 👆 Mouse Movement: Control cursor position with your index finger
- 🖱️ Left Click: Bend index finger while keeping middle finger straight
- 🔘 Right Click: Bend middle finger while keeping index finger straight
- ✌️ Double Click: Bend both index and middle fingers
- 📸 Screenshot: Bend both index and middle fingers while bringing thumb close
- 🎯 Smooth Movement: Implements cursor smoothing for precise control

## Requirements

- Python 3.7+
- Webcam
- Good lighting conditions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/gokul-s05/virtual_mouse.git
cd virtual_mouse
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

Required packages:
- opencv-python
- mediapipe
- pyautogui
- pynput
- numpy

## Usage

1. Run the program:
```bash
python main.py
```

2. Position your hand in front of the webcam
3. Use the following gestures:
   - Move cursor: Point with your index finger
   - Left click: Bend index finger (keep middle finger straight)
   - Right click: Bend middle finger (keep index finger straight)
   - Double click: Bend both index and middle fingers
   - Screenshot: Bend both fingers and bring thumb close
   
4. Press 'q' to quit the program

## Gesture Guide

### Mouse Movement
- Extend your index finger
- Move your hand in the direction you want the cursor to go
- The cursor movement is smoothed for better control

### Left Click
- Keep middle finger straight
- Bend index finger
- Keep thumb away from fingers

### Right Click
- Keep index finger straight
- Bend middle finger
- Keep thumb away from fingers

### Double Click
- Bend both index and middle fingers
- Keep thumb away from fingers

### Screenshot
- Bend both index and middle fingers
- Bring thumb close to fingers
- Screenshots are saved as 'my_screenshot_[number].png'

## Customization

You can adjust the following parameters in `main.py` to customize the mouse behavior:

```python
SMOOTHING_FACTOR = 0.5  # Adjusts how smooth the motion is (0-1)
SCALING_FACTOR = 1.2    # Adjusts the sensitivity of mouse movement
DEADZONE = 5           # Minimum pixel movement required
```

- Increase `SMOOTHING_FACTOR` for smoother but slower movement
- Decrease `SMOOTHING_FACTOR` for more responsive but potentially jittery movement
- Adjust `SCALING_FACTOR` to change movement sensitivity
- Adjust `DEADZONE` to change how much movement is required before the mouse moves

## Troubleshooting

1. **Camera not detected**
   - Ensure your webcam is properly connected
   - Try changing the camera index in `main.py` (default is 0)

2. **Poor gesture recognition**
   - Ensure good lighting conditions
   - Keep your hand within the camera frame
   - Maintain clear separation between fingers for better detection

3. **Jerky mouse movement**
   - Adjust the `SMOOTHING_FACTOR` and `SCALING_FACTOR` in `main.py`
   - Try to keep your hand steady
   - Ensure adequate lighting for better hand tracking

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.
