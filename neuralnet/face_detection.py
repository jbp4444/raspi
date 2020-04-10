from aiy.vision.inference import CameraInference
from aiy.vision.models import face_detection
from picamera import PiCamera

def main():
	with PiCamera() as camera:
	camera.resolution = (1640, 922)
	camera.start_preview()
	with CameraInference(face_detection.model()) as inference:
		for result in inference.run():
			if len(face_detection.get_faces(result)) >= 1:
				camera.capture('faces.jpg')
				break

	camera.stop_preview()

if __name__ == '__main__':
	main()
