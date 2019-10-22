import cv2
import face_recognition
import numpy as np
from datetime import datetime
from datetime import timedelta
import sys

def main(argv):

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    if len(argv) >= 1:
        print("Using stream source at %s" % (argv[0]))
        video_capture = cv2.VideoCapture(argv[0])
    else:
        print("Trying to open live stream")
        video_capture = cv2.VideoCapture(0)

    show_frame = False
    if len(argv) > 1 and argv[1] == '-f':
        show_frame = True

    fps = int(video_capture.get(5))
    width = int(video_capture.get(3))
    height = int(video_capture.get(4))
    print("Stream format: %dx%d %d fps" % (width, height, fps))

    index = 0;
    fc = 0;
    n_faces_prev = 0;
    start = datetime.now()
    cap_trg = False
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)

        n_faces = len(face_locations)
        if n_faces_prev != n_faces:
            print("Detected %d faces" % (n_faces))
            # Store detected faces and start video stream
            for (top, right, bottom, left) in face_locations:
                shift_x = int ((right-left)*0.15)
                shift_y = int ((bottom-top)*0.6)
                left = left*2 - shift_x
                top = top*2 - shift_y
                right = right*2 + shift_x
                bottom = bottom*2 + shift_y
                if n_faces_prev != n_faces:
                    face_img = frame[top:bottom, left:right]
                    start = datetime.now()
                    date_time = start.strftime("%m-%d-%Y-%H:%M:%S")
                    name = '/media/capture/face_'+date_time+str(index)+'.jpg'
                    name = 'pict/face_'+date_time+str(index)+'.jpg'
                    cv2.imwrite(name, face_img)
                    index = index + 1
                if not cap_trg:
                    cap_trg = True
                    stream = '/media/video/vid_' + date_time +'.avi'
                    print("Starting new live stream to %s" % (stream))
                    out = cv2.VideoWriter(stream, cv2.VideoWriter_fourcc('M','J','P','G'), fps, (width,height))
        # Draw rectangle around the faces
        for (top, right, bottom, left) in face_locations:
            shift_x = int ((right-left)*0.15)
            shift_y = int ((bottom-top)*0.6)
            cv2.rectangle(frame, (int(left*2 - shift_x), int(top*2 - shift_y)), (int(right*2 + shift_x), int(bottom*2 + shift_y)), (0, 0, 255), 2)
        if show_frame:
            # Display the output
            cv2.imshow('img', frame)
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        n_faces_prev = n_faces
        if cap_trg:
            out.write(frame)
            if (datetime.now() - start).total_seconds() > 30:
                out.release()
                cap_trg = False
                print("Stream closed")
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
       main(sys.argv[1:])
