import cv2
from PIL import Image

def resize_video(input_video_path, output_video_path, new_height, new_width):
    # Open the input video
    cap = cv2.VideoCapture(input_video_path)

    # Get the original video's width, height, fps and codec
    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for mp4

    # Open the output video writer
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (new_width, new_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Resize the frame
        resized_frame = cv2.resize(frame, (new_width, new_height))
        
        # Write the resized frame to the output video
        out.write(resized_frame)

    # Release resources
    cap.release()
    out.release()


# If you need to know the dimensions for a video, use these two functions below

def extract_frame(video_path, frame_number):
    # Open the video file
    video = cv2.VideoCapture(video_path)
    # Set the video position to the desired frame number
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    # Read the frame
    ret, frame = video.read()
    # Release the video capture object
    video.release()

    if ret:
        return frame
    else:
        raise ValueError("Could not read the frame from the video.")

# Function to get the size of the frame
def get_frame_size(frame):
    # Convert the frame to a PIL Image
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    # Get the size of the image
    return image.size # width, height

path = "results/1ehtmua.mp4"
frame = extract_frame(path, 1)
print(get_frame_size(frame))
# resize_video(path, "gameplay/gta5.mp4", 384, 540)