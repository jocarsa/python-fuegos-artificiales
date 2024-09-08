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

# Firework generation function with random parameters
def generate_firework():
    num_particles = np.random.randint(50, 150)  # Random number of particles
    angles = np.linspace(0, 2 * np.pi, num_particles)
    speeds = np.random.uniform(5, 15, num_particles)  # Increased speed for wider bursts
    dx = np.cos(angles) * speeds
    dy = np.sin(angles) * speeds
    colors = np.random.randint(0, 255, (num_particles, 3), dtype=np.uint8)
    x = np.full(num_particles, np.random.randint(width // 4, 3 * width // 4), dtype=np.float32)
    y = np.full(num_particles, np.random.randint(height // 4, height // 2), dtype=np.float32)
    decay = np.random.uniform(0.85, 0.95)  # Random decay rate
    alpha = np.ones(num_particles, dtype=np.float32)  # Alpha for fading
    return x, y, dx, dy, colors, decay, alpha

# Initialize list of fireworks
fireworks = []

# Timing variables
start_time = time.time()

for frame_num in range(total_frames):
    # Create a black background
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Generate a new firework every 30 frames
    if frame_num % 30 == 0:
        fireworks.append(generate_firework())

    # Update and draw each firework
    for fw in fireworks:
        x, y, dx, dy, colors, decay, alpha = fw
        dy += 0.1  # Apply gravity
        prev_x, prev_y = x.copy(), y.copy()
        x += dx
        y += dy
        dx *= decay
        dy *= decay

        # Decrease alpha for fade out as they fall
        alpha *= 0.98

        # Draw particles as lines indicating speed and direction, with fading effect
        for i in range(len(x)):
            if 0 <= x[i] < width and 0 <= y[i] < height:
                start_point = (int(prev_x[i]), int(prev_y[i]))
                end_point = (int(x[i]), int(y[i]))
                faded_color = tuple(int(c * alpha[i]) for c in colors[i])
                cv2.line(frame, start_point, end_point, faded_color, 2)

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
