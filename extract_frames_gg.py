import cv2
import os
import sys

def extract_frames(video_path, output_folder, frame_interval=1):
    """
    Extracts frames from a video file and saves them as images.

    Args:
        video_path (str): The path to the input video file.
        output_folder (str): The directory where extracted frames will be saved.
        frame_interval (int): Save every Nth frame. Use 1 to save every frame.
    """

    # --- Input Validation ---
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        sys.exit(1)

    # --- Create Output Folder ---
    # Create the output folder if it doesn't exist. exist_ok=True prevents errors
    # if the folder is already there.
    os.makedirs(output_folder, exist_ok=True)
    print(f"Output folder '{output_folder}' ensured.")

    # --- Open Video File ---
    cap = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        sys.exit(1)

    # --- Extract Frames ---
    frame_count = 0
    saved_frame_count = 0
    print("Starting frame extraction...")

    while True:
        # Read a frame
        ret, frame = cap.read() # ret is True if frame is read correctly, frame is the image data

        # If frame is not read correctly (end of video or error), break the loop
        if not ret:
            break

        # Check if we should save this frame based on the interval
        if frame_count % frame_interval == 0:
            # Construct filename
            # Using a zero-padded number ensures files sort correctly (e.g., 00001.png, 00010.png)
            # The format is 'frame_XXXXX.png' where XXXXX is the saved frame index
            frame_filename = os.path.join(output_folder, f"frame_{saved_frame_count:05d}.png")

            # Save the frame as an image file
            # cv2.imwrite() saves the image. Choose format based on extension (.png, .jpg, etc.)
            cv2.imwrite(frame_filename, frame)

            saved_frame_count += 1
            if saved_frame_count % 100 == 0: # Optional: print progress every 100 frames
                 print(f"Processed and saved {saved_frame_count} frames...", end='\r')


        frame_count += 1 # Always increment total frame count

    # --- Release Resources ---
    cap.release() # Release the video capture object

    # --- Conclusion ---
    print("\nFrame extraction finished.")
    print(f"Total frames processed: {frame_count}")
    print(f"Total frames saved: {saved_frame_count}")


# --- Script Usage Example ---
if __name__ == "__main__":
    # --- Configuration ---
    # IMPORTANT:
    # 1. Replace 'path/to/your/video.mp4' with the actual path to your video file.
    # 2. Replace 'output_images' with the desired name for the folder where images will be saved.
    #    This folder will be created in the same directory as the script if a full path isn't given.
    # 3. Adjust frame_interval: 1 means save every frame, 5 means save every 5th frame, etc.
    #    Saving every frame can result in a huge number of images for long videos.
    #    Consider increasing frame_interval if your video is long or you don't need every frame.

    video_input_path = 'video.mp4'
    output_frames_folder = 'output_images'
    save_every_n_frames = 1 # Set to 1 to save every frame, 2 to save every 2nd, etc.

    # --- Run the extraction ---
    extract_frames(video_input_path, output_frames_folder, save_every_n_frames)

    print(f"\nFrames saved to the folder: {output_frames_folder}")