import cv2
import numpy as np
from scenedetect import detect, ContentDetector
from moviepy.editor import VideoFileClip
import os

def detect_scenes(video_path):
    # Detect scenes using PySceneDetect
    scenes = detect(video_path, ContentDetector())
    return scenes

def split_video(video_path, scenes, output_dir):
    # Load the video
    video = VideoFileClip(video_path)
    
    # Split the video into scenes
    for i, scene in enumerate(scenes):
        start_time = scene[0].get_seconds()
        end_time = scene[1].get_seconds()
        
        # Extract the scene
        scene_clip = video.subclip(start_time, end_time)
        
        # Write the scene to a file
        output_path = os.path.join(output_dir, f"scene_{i+1}.mp4")
        scene_clip.write_videofile(output_path, codec="libx264")
        
        print(f"Scene {i+1} saved as {output_path}")
    
    # Close the video to free up system resources
    video.close()

def main(video_path, output_dir):
    print("Detecting scenes...")
    scenes = detect_scenes(video_path)
    
    print(f"Found {len(scenes)} scenes. Splitting video...")
    split_video(video_path, scenes, output_dir)
    
    print("Video splitting complete!")

if __name__ == "__main__":
    video_path = "input_video.mp4"  # Replace with your video file path
    output_dir = "output_scenes"  # Specify the output directory for scenes
    os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist
    main(video_path, output_dir)

