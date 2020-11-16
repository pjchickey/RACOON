import os
import constants
import numpy as np
from scipy import misc, ndimage

def resize(image, dim1, dim2):
	return misc.imresize(image, (dim1, dim2))

def fileWalk(directory, destPath):
	try: 
		os.makedirs(destPath)
	except OSError:
		if not os.path.isdir(destPath):
			raise

	for subdir, dirs, files in os.walk(directory):
		for file in files:
			if len(file) <= 4 or file[-4:] != '.png':
				continue

			pic = misc.imread(os.path.join(subdir, file))
			dim1 = len(pic)
			dim2 = len(pic[0])
			if dim1 > dim2:
				pic = np.rot90(pic)

			picResized = resize(pic,constants.DIM1, constants.DIM2)
			misc.imsave(os.path.join(destPath, file), picResized)
		

def main():
	prepath = os.path.join(os.getcwd(), 'Images')
	aluminumDir = os.path.join(prepath, 'Aluminum')
	cardboardboxDir = os.path.join(prepath, 'Cardboard-Boxes')
	cardboardotherDir = os.path.join(prepath, 'Cardboard-Other')
	glassDir = os.path.join(prepath, 'Glass')
	paperjunkDir = os.path.join(prepath, 'Paper-Junk_Mail')
	plasticbottlesDir = os.path.join(prepath, 'Plastic-Bottles')
	steelandtinDir = os.path.join(prepath, 'Steel_and_Tin')

	destPath = os.path.join(os.getcwd(), 'Images-resized')
	try: 
		os.makedirs(destPath)
	except OSError:
		if not os.path.isdir(destPath):
			raise

	#ALUMINUM
	fileWalk(aluminumDir, os.path.join(destPath, 'Aluminum'))

	#CARDBOARD-BOXES
	fileWalk(cardboardboxDir, os.path.join(destPath, 'Cardboard-Boxes'))

	#CARDBOARD-OTHER
	fileWalk(cardboardotherDir, os.path.join(destPath, 'Cardboard-Other'))

	#GLASS
	fileWalk(glassDir, os.path.join(destPath, 'Glass'))

	#PAPER-JUNK-MAIL
	fileWalk(paperjunkDir, os.path.join(destPath, 'Paper-Junk_Mail'))

	#PLASTIC-BOTTLES
	fileWalk(plasticbottlesDir, os.path.join(destPath, 'Plastic-Bottles'))

	#STEEL_AND_TIN
	fileWalk(steelandtinDir, os.path.join(destPath, 'Steel_and_Tin'))

if __name__ == '__main__':
    main()