import cv2

stream_url = 'rtsp://localhost:8554/mystream'  # RTSP stream URL

cap = cv2.VideoCapture(stream_url)

# Check if stream opened successfully
if not cap.isOpened():
    print("Error: Cannot open video stream.")
    exit()

# Read and display frames in a loop
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    cv2.imshow("Video Stream", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
