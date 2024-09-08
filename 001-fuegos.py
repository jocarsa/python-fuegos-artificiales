import cv2
import numpy as np
import time
import os
from datetime import datetime

# Set parameters
width, height = 1920, 1080
fps = 60
duration = 60  # seconds
total_frames = fps * duration

# Generate unique file name using epoch time
epoch_time = int(time.time())
output_folder = "render"
os.makedirs(output_folder, exist_ok=True)
output_file = os.path.join(output_folder, f"{epoch_time}.mp4")

# Define video writer with H264 codec
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

# Firework parameters
num_particles = 100
gravity = 0.1
explosion_decay = 0.9

# Function to generate initial firework particles
def generate_firework():
    angles = np.linspace(0, 2 * np.pi, num_particles)
    speeds = np.random.uniform(4, 8, num_particles)
    dx = np.cos(angles) * speeds
    dy = np.sin(angles) * speeds
    colors = np.random.randint(0, 255, (num_particles, 3), dtype=np.uint8)
    return dx, dy, colors

# Initialize firework with float32 type to match dx and dy
x, y = np.full(num_particles, width // 2, dtype=np.float32), np.full(num_particles, height // 2, dtype=np.float32)
dx, dy, colors = generate_firework()

# Timing variables
start_time = time.time()

for frame_num in range(total_frames):
    # Create a black background
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Update particles
    dy += gravity  # Apply gravity
    x += dx
    y += dy
    dx *= explosion_decay
    dy *= explosion_decay

    # Draw particles
    for i in range(num_particles):
        if 0 <= x[i] < width and 0 <= y[i] < height:
            cv2.circle(frame, (int(x[i]), int(y[i])), 3, tuple(map(int, colors[i])), -1)

    # Write frame to video
    video_writer.write(frame)

    # Print statistics every 60 frames
    if frame_num % 60 == 0:
        elapsed_time = time.time() - start_time
        completed_frames = frame_num + 1
        remaining_frames = total_frames - completed_frames
        time_per_frame = elapsed_time / completed_frames
        estimated_total_time = time_per_frame * total_frames
        remaining_time = estimated_total_time - elapsed_time
        completion_percentage = (completed_frames / total_frames) * 100

        # Print statistics
        print(f"Frame: {completed_frames}/{total_frames} | "
              f"Elapsed Time: {elapsed_time:.2f}s | "
              f"Time Remaining: {remaining_time:.2f}s | "
              f"Estimated Finish: {datetime.fromtimestamp(start_time + estimated_total_time).strftime('%H:%M:%S')} | "
              f"Completion: {completion_percentage:.2f}%")

# Release video writer
video_writer.release()

print(f"Video saved to {output_file}")
