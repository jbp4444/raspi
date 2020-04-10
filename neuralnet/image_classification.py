import argparse
from PIL import Image
from aiy.vision.inference import ImageInference
from aiy.vision.models import image_classification

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--input', '-i', dest='input', required=True)
	args = parser.parse_args()
	with ImageInference(image_classification.model()) as inference:
		image = Image.open(args.input)
		classes = image_classification.get_classes(inference.run(image))
		for i, (label, score) in enumerate(classes):
			print('Result %d: %s (prob=%f)' % (i, label, score))

if __name__ == '__main__':
	main()
