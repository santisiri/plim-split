from moviepy.video.io.VideoFileClip import VideoFileClip
import numpy as np
import os

def detect_scenes(video_path, threshold=30):
    clip = VideoFileClip(video_path)
    prev_frame = None
    scenes = [0]
    
    for i, frame in enumerate(clip.iter_frames()):
        if prev_frame is not None:
            diff = np.abs(frame - prev_frame).mean()
            if diff > threshold:
                scenes.append(i)
        prev_frame = frame
    
    scenes.append(int(clip.fps * clip.duration))
    clip.close()
    return scenes

def split_video(video_path, scenes, output_dir):
    clip = VideoFileClip(video_path)
    total_frames = int(clip.fps * clip.duration)
    
    for i in range(len(scenes) - 1):
        start_frame = scenes[i]
        end_frame = min(scenes[i+1], total_frames)  # Ensure we don't exceed total frames
        
        # Convert frame numbers to times
        start_time = start_frame / clip.fps
        end_time = end_frame / clip.fps
        
        output_path = os.path.join(output_dir, f"scene_{i+1}.mp4")
        
        # Extract frames for this time segment
        frames = []
        for t in np.arange(start_time, end_time, 1/clip.fps):
            if t <= clip.duration:  # Only process frames within video duration
                frames.append(clip.get_frame(t))
        
        if frames:  # Only save if we have frames
            import imageio
            imageio.mimsave(output_path, frames, fps=clip.fps)
    
    clip.close()

def main(video_path, output_dir):
    print("Detecting scenes...")
    scenes = detect_scenes(video_path)
    
    print(f"Found {len(scenes)-1} scenes. Splitting video...")
    split_video(video_path, scenes, output_dir)
    
    print("Video splitting complete!")

if __name__ == "__main__":
    video_path = "input_video.mp4"
    output_dir = "output_scenes"
    os.makedirs(output_dir, exist_ok=True)
    main(video_path, output_dir)