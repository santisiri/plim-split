from moviepy.video.io.VideoFileClip import VideoFileClip
import numpy as np
import os

def detect_scenes(video_path, threshold=30):
    clip = VideoFileClip(video_path)
    scenes = [0]  # Start with first frame
    prev_frame = None
    frame_count = 0
    
    for current_frame in clip.iter_frames():
        if prev_frame is not None:
            # Calculate difference between frames
            diff = np.mean(np.abs(current_frame - prev_frame))
            if diff > threshold:
                scenes.append(frame_count)
        
        prev_frame = current_frame
        frame_count += 1
    
    scenes.append(frame_count)  # Add last frame
    clip.close()
    return scenes

def split_video(video_path, scenes, output_dir, progress_callback=None):
    clip = VideoFileClip(video_path)
    total_frames = int(clip.fps * clip.duration)
    total_scenes = len(scenes) - 1
    
    for i in range(total_scenes):
        if progress_callback:
            progress = (i / total_scenes) * 100
            progress_callback(progress, f"Processing scene {i+1} of {total_scenes}")
            
        start_frame = scenes[i]
        end_frame = min(scenes[i+1], total_frames)
        
        start_time = start_frame / clip.fps
        end_time = end_frame / clip.fps
        
        output_path = os.path.join(output_dir, f"scene_{i+1}.mp4")
        
        frames = []
        for t in np.arange(start_time, end_time, 1/clip.fps):
            if t <= clip.duration:
                frames.append(clip.get_frame(t))
        
        if frames:
            import imageio
            imageio.mimsave(output_path, frames, fps=clip.fps)
    
    if progress_callback:
        progress_callback(100, "Processing complete!")
    
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