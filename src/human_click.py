import pyautogui
import bezier
import numpy as np


def move_mouse(x, y):
    end = x, y
    # Disable pyautogui pauses (from DJV's answer)
    pyautogui.MINIMUM_DURATION = 0
    pyautogui.MINIMUM_SLEEP = 0
    pyautogui.PAUSE = 0

    print("Moving to searchbox.")

    # For this example we'll use four control points, including start and end coordinates
    start = pyautogui.position()
    # end = start[0]+600, start[1]+200
    # Two intermediate control points that may be adjusted to modify the curve.
    control1 = start[0]+30, start[1]+12
    control2 = start[0]+23, start[1]+33

    # Format points to use with bezier
    control_points = np.array([start, control1, control2, end])
    points = np.array([control_points[:,0], control_points[:,1]]) # Split x and y coordinates

    # You can set the degree of the curve here, should be less than # of control points
    degree = 3
    # Create the bezier curve
    curve = bezier.Curve(points, degree)
    # You can also create it with using Curve.from_nodes(), which sets degree to len(control_points)-1
    # curve = bezier.Curve.from_nodes(points)

    curve_steps = 50  # How many points the curve should be split into. Each is a separate pyautogui.moveTo() execution
    delay = .2/curve_steps  # Time between movements. 1/curve_steps = 1 second for entire curve

    # Move the mouse
    for i in range(1, curve_steps+1):
        # The evaluate method takes a float from [0.0, 1.0] and returns the coordinates at that point in the curve
        # Another way of thinking about it is that i/steps gets the coordinates at (100*i/steps) percent into the curve
        x, y = curve.evaluate(i/curve_steps)
        pyautogui.moveTo(x, y)  # Move to point in curve
        pyautogui.sleep(delay)  # Wait delay