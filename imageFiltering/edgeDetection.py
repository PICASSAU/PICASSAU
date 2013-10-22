from PIL import Image, ImageFilter

image = Image.open('teamTestPic.png')
image = image.filter(ImageFilter.FIND_EDGES)
image.save('testTeamPicEdges.png')

