import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time
import random

# Set page config for a dark theme
st.set_page_config(page_title="Mystic Mirror", page_icon="🔮", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(to bottom, #0f0c29, #302b63, #24243e);
        color: #f1f1f1;
    }
    .stButton>button {
        background-color: #7e57c2;
        color: white;
    }
    .stSuccess {
        background-color: rgba(0, 255, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def generate_fortune():
    fortunes = [
        "The stars align in your favor. Great opportunities await you.",
        "A journey of self-discovery lies ahead. Embrace the unknown.",
        "Your creativity will lead you to unexpected treasures.",
        "A challenge you've been facing will soon resolve itself.",
        "Love and harmony will enter your life in a surprising way.",
        "Your persistence will pay off. Keep pushing forward.",
        "An old friend will bring exciting news.",
        "Your intuition is strong. Trust your inner voice.",
        "A dream you've long held will soon become reality.",
        "Unexpected kindness will brighten your path."
    ]
    return random.choice(fortunes)

def annotate_face_in_pieces(image):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    base_options = python.BaseOptions(model_asset_path='face_landmarker_v2_with_blendshapes.task')
    options = vision.FaceLandmarkerOptions(
        base_options=base_options,
        output_face_blendshapes=True,
        output_facial_transformation_matrixes=True,
        num_faces=1
    )
    detector = vision.FaceLandmarker.create_from_options(options)
    
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
    detection_result = detector.detect(mp_image)
    
    annotated_image = np.copy(rgb_image)
    
    if detection_result.face_landmarks:
        face_landmarks = detection_result.face_landmarks[0]
        face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        face_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z)
            for landmark in face_landmarks
        ])
        
        skin_color = (255, 224, 189)
        eye_color = (150, 255, 150)
        
        # Yield partial annotations
        yield annotated_image  # Initial image without annotations
        
        # Draw face mesh
        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks_proto,
            connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles.DrawingSpec(color=skin_color, thickness=1)
        )
        yield annotated_image
        
        # Draw contours
        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks_proto,
            connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles.DrawingSpec(color=skin_color, thickness=2)
        )
        yield annotated_image
        
        # Draw irises
        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks_proto,
            connections=mp.solutions.face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles.DrawingSpec(color=eye_color, thickness=2)
        )
        yield annotated_image  # Final fully annotated image

def main():
    st.title("🔮 The Mystic Mirror of Destiny 🔮")
    st.markdown("""
    <p style='font-style: italic; color: #b39ddb;'>
    Gaze into the magical mirror and uncover the secrets that lie within your visage.
    The ancient spirits await to reveal your destiny...
    </p>
    """, unsafe_allow_html=True)

    # Create a placeholder for the camera input
    camera_placeholder = st.empty()

    # Display the camera input in the placeholder
    img_file_buffer = camera_placeholder.camera_input("📸 Capture Your Essence")

    if img_file_buffer is not None:
        bytes_data = img_file_buffer.getvalue()
        img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        with st.spinner("The spirits are studying your visage..."):
            face_detected = False
            for annotated_img in annotate_face_in_pieces(img):
                face_detected = True
                # Replace the camera input with the annotated image
                camera_placeholder.image(annotated_img, channels="RGB", use_column_width=True)
                time.sleep(0.5)  # Add a delay between each step

        if face_detected:
            # Magical sound effect (you can replace this with an actual sound if desired)
            st.markdown("🔔")

            st.success("The mystical energies have aligned!")
            
            # Generate and display the fortune
            fortune = generate_fortune()
            st.markdown(f"""
            <div style='background-color: rgba(62, 39, 135, 0.2); padding: 20px; border-radius: 10px; text-align: center;'>
                <h3 style='color: #e1bee7;'>Your Fortune Reveals:</h3>
                <p style='font-size: 18px; font-style: italic; color: #fff59d;'>{fortune}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("No face detected. Please ensure your face is in the frame and try again.")

        # Option to try again
        if st.button("🔮 Consult the Mystic Mirror Again"):
            st.experimental_rerun()

if __name__ == "__main__":
    main()