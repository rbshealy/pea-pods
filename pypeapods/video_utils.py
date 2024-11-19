
import cv2
import os

def video_to_frames(video_path, output_dir):
    """Converts a video to frames and saves them in the output directory."""

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error opening video file")
        return

    # Create the output directory if it doesn't exist
    import os
    os.makedirs(output_dir, exist_ok=True)

    frame_count = 0
    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        if not ret:
            break

        # Save the frame as an image
        frame_path = os.path.join(output_dir, f"frame_{frame_count:04d}.png")
        cv2.imwrite(frame_path, frame)

        frame_count += 1

    cap.release()
    print(f"Successfully extracted {frame_count} frames from {video_path} to {output_dir}")


def frames_to_video(frames_input, video_output):

    images = [img for img in os.listdir(frames_input) if img.endswith(".png")]
    if len(images) == 0:
        print(f"Nothing in expected path: {frames_input}")
        return
    frame = cv2.imread(os.path.join(frames_input, images[0]))
    height, width, layers = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(video_output, fourcc, 30, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(frames_input, image)))

    cv2.destroyAllWindows()
    video.release()
    print(f"Successfully made {video_output} from {frames_input}")


def clear_dir(dir):
    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)
        if filename.endswith('.png') and os.path.isfile(file_path):
            os.remove(file_path)
            #print(f"Deleted: {file_path}")
