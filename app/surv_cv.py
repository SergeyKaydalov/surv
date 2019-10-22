import cv2
from datetime import datetime
from datetime import timedelta
import sys

def main(argv):

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    if len(argv) > 0:
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
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # Grab a single frame of video
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        n_faces = len(faces)
        if n_faces_prev != n_faces:
            print("Detected %d faces" % (n_faces))
            # Store detected faces and start video stream
            for (x, y, w, h) in faces:
                if n_faces_prev != n_faces:
                    face_img = frame[y:y+h, x:x+w]
                    start = datetime.now()
                    date_time = start.strftime("%m-%d-%Y-%H:%M:%S")
                    name = '/media/capture/face_'+date_time+str(index)+'.jpg'
                    print("Capturing to %s" % (name))
                    cv2.imwrite(name, face_img)
                    index = index + 1
                if not cap_trg:
                    cap_trg = True
                    stream = '/media/video/vid_' + date_time +'.avi'
                    print("Starting new live stream to %s" % (stream))
                    out = cv2.VideoWriter(stream, cv2.VideoWriter_fourcc('M','J','P','G'), fps, (width,height))
        # Draw rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        if show_frame:
            # Display the output
            cv2.imshow('img', frame)
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
