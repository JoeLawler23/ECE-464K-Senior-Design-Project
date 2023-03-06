import freenect
import numpy as np
import readchar
import time
import matplotlib.pyplot as plt

# Initialize the plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# Update the subplots in real time
while True:
    # Capture a color frame and a depth frame from the Kinect sensor
    video, _ = freenect.sync_get_video()
    depth, _ = freenect.sync_get_depth()

    # Convert the video data to an RGB image
    rgb_image = video[:, :, ::-1]

    # Display the color image as a subplot
    ax1.clear()
    ax1.imshow(rgb_image)
    ax1.set_title('Color Image')

    # Display the depth map as a subplot
    ax2.clear()
    ax2.imshow(depth, cmap='gray')
    ax2.set_title('Depth Map')

    # Update the subplots with the latest data
    plt.draw()
    plt.pause(0.001)