from PIL import Image
import glob, os

for infile in glob.glob("*.jpg"):
    file, ext = os.path.splitext(infile)
    im = Image.open(infile)
    imWidth, imHeight = im.size

    width = 115

    height = 65
    #row 5 only: 60
    #other rows: 85

    topMargin = 416 #change this to determine what row to crop
    #row 1: 0
    #row 2: 105
    #row 3: 208
    #row 4: 311
    #row 5: 416

    i = 0
    while (i < imWidth):
        button = im.crop((i, topMargin, width+i, topMargin + height))
        button.save(f'row5button{i}.jpeg', 'JPEG')
        i += width + 26 #26 is the margin between the buttons in the image