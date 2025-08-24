import cv2
import mediapipe as mp
import numpy as np
import gradio as gr
from PIL import Image
import time

# Initialize Mediapipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False)

def calculate_angle(a, b, c):
    a = np.array(a)  # First point
    b = np.array(b)  # Midpoint
    c = np.array(c)  # End point

    # Vector calculations
    ba = a - b
    bc = c - b

    # Calculate cosine angle
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)  # In radians

    return np.degrees(angle)

def validate_pose(landmarks):
    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, 
                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, 
                  landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, 
                  landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    
    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, 
                      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, 
                   landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
    right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, 
                   landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

    left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
    right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

    # Define acceptable pose criteria (adjust thresholds as needed)
    correct_left_elbow = 70 <= left_elbow_angle <= 110
    correct_right_elbow = 70 <= right_elbow_angle <= 110

    feedback = []
    if correct_left_elbow:
        feedback.append("Left elbow pose is correct.")
    else:
        feedback.append(f"Left elbow angle {left_elbow_angle:.2f} is incorrect. Expected: 70-110 degrees.")

    if correct_right_elbow:
        feedback.append("Right elbow pose is correct.")
    else:
        feedback.append(f"Right elbow angle {right_elbow_angle:.2f} is incorrect. Expected: 70-110 degrees.")

    return "\n".join(feedback)

def overlay_landmarks(image, landmarks):
    image = np.array(image)
    for lm in landmarks.pose_landmarks.landmark:
        h, w, _ = image.shape
        x, y = int(lm.x * w), int(lm.y * h)
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

def calculate_execution_time(func):
    def wrapper(image):
        start_time = time.time()
        feedback, image_with_landmarks = func(image)
        end_time = time.time()
        exec_time = f"Execution Time: {end_time - start_time:.2f} seconds"
        return feedback + "\n" + exec_time, image_with_landmarks
    return wrapper

@calculate_execution_time
def pose_detection(image):
    image = np.array(image)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if not results.pose_landmarks:
        return "No Pose Detected", image

    feedback = validate_pose(results.pose_landmarks.landmark)
    image_with_landmarks = overlay_landmarks(image, results)
    return feedback, image_with_landmarks

# Create Gradio Interface with UI improvements
interface = gr.Interface(
    fn=pose_detection, 
    inputs=gr.Image(type="pil", label="Upload an Image for Pose Detection"), 
    outputs=[
        gr.Textbox(label="Pose Feedback", lines=4), 
        gr.Image(label="Processed Image", type="pil", image_mode="RGB")
    ],
    title="Pose Detection",
    description="""
    This application uses Mediapipe's Pose Detection to estimate the angles of your elbows in a given image.
    The system calculates the left and right elbow angles and validates if they meet the expected criteria for a correct pose.
    Upload a photo to see the results and the processed image with landmarks.
    """,
    live=True
)

interface.launch()
