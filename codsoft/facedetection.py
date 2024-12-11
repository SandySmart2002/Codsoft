import cv2
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow warnings
from deepface import DeepFace

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Directory containing images
image_folder = r"C:\Users\sande\Downloads\face"  # Replace with your image folder path

# Process each image in the folder
for img_file in os.listdir(image_folder):
    img_path = os.path.join(image_folder, img_file)

    # Load image
    img = cv2.imread(img_path)
    if img is None:
        print(f"Could not load image {img_file}")
        continue  # Skip to next image if current one can't be loaded

    # Resize image (keeping the aspect ratio) for faster processing
    height, width = img.shape[:2]
    max_dimension = 800  # Set the maximum dimension (width or height)
    if max(height, width) > max_dimension:
        scale_factor = max_dimension / float(max(height, width))
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        img = cv2.resize(img, (new_width, new_height))

    # Convert image to grayscale for face detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        print(f"No faces detected in {img_file}")

    # Process each face detected
    for (x, y, w, h) in faces:
        # Draw rectangle around the face
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Crop the face from the image for recognition
        face = img[y:y+h, x:x+w]

        try:
            # Recognize the face using DeepFace
            result = DeepFace.analyze(face, actions=['emotion'], enforce_detection=False)

            # If result is a list, take the first item (since only one face is cropped per iteration)
            if isinstance(result, list):
                result = result[0]

            # Extract the dominant emotion
            dominant_emotion = result['dominant_emotion']

            # Display emotion label near the face
            cv2.putText(img, dominant_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        except Exception as e:
            print(f"Error processing face in {img_file}: {e}")

    # Show the image with detected faces and recognized emotions
    cv2.imshow(f"Processed {img_file}", img)

    # Wait for user input to close image window
    cv2.waitKey(0)

cv2.destroyAllWindows()
