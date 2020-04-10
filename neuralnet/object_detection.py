import argparse
from PIL import Image
from PIL import ImageDraw
from aiy.vision.inference import ImageInference
from aiy.vision.models import object_detection

def _crop_center(image):
	width, height = image.size
	size = min(width, height)
	x, y = (width - size) / 2, (height - size) / 2
	return image.crop((x, y, x + size, y + size)), (x, y)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--input', '-i', dest='input', required=True)
	parser.add_argument('--output', '-o', dest='output')
	args = parser.parse_args()
	with ImageInference(object_detection.model()) as inference:
		image = Image.open(args.input)
		image_center, offset = _crop_center(image)
		draw = ImageDraw.Draw(image)
		result = inference.run(image_center)
		for i, obj in enumerate(object_detection.get_objects(result, 0.3, offset)):
			print('Object #%d: %s' % (i, str(obj)))
			x, y, width, height = obj.bounding_box
			draw.rectangle((x, y, x + width, y + height), outline='red')
		if args.output:
			image.save(args.output)

if __name__ == '__main__':
	main()
