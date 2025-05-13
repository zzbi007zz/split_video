import cv2
import os
import argparse

def extract_frames(video_path, frame_interval=1):
    """
    Extract frames from a video and save them in the same folder as the video.
    
    Args:
        video_path (str): Path to the video file
        frame_interval (int): Extract every nth frame
    """
    # Get the directory and filename without extension
    video_dir = os.path.dirname(video_path)
    video_filename = os.path.basename(video_path)
    video_name = os.path.splitext(video_filename)[0]
    
    # Create output folder as a subfolder in the same directory as the video
    output_folder = os.path.join(video_dir, f"{video_name}_frames")
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output directory: {output_folder}")
    
    # Open the video file
    video = cv2.VideoCapture(video_path)
    
    # Check if video opened successfully
    if not video.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return
    
    # Get video properties
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)
    
    print(f"Video loaded: {video_path}")
    print(f"Total frames: {total_frames}")
    print(f"FPS: {fps}")
    print(f"Extracting every {frame_interval} frame(s)")
    print(f"Saving frames to: {output_folder}")
    
    # Initialize frame counter
    count = 0
    saved_count = 0
    
    # Read until video is completed
    while True:
        # Read frame
        ret, frame = video.read()
        
        # Break the loop if we've reached the end of the video
        if not ret:
            break
        
        # Save frame if it matches our interval
        if count % frame_interval == 0:
            # Create filename with leading zeros for proper sorting
            frame_filename = os.path.join(output_folder, f"frame_{saved_count:06d}.jpg")
            
            # Save frame as JPEG file
            cv2.imwrite(frame_filename, frame)
            saved_count += 1
            
            # Print progress periodically
            if saved_count % 100 == 0:
                print(f"Saved {saved_count} frames so far...")
        
        count += 1
    
    # Release video capture object
    video.release()
    
    print(f"Extraction complete! Saved {saved_count} frames to {output_folder}")

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="Extract frames from a video file.")
    parser.add_argument("video_path", type=str, help="Path to the video file")
    parser.add_argument("--interval", type=int, default=1, 
                        help="Extract every nth frame (default: 1)")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Extract frames from video
    extract_frames(args.video_path, args.interval)