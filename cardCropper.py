from PIL import Image
import glob, os

for infile in glob.glob("Cards.png"):
    file, ext = os.path.splitext(infile)
    im = Image.open(infile)
    imWidth, imHeight = im.size

    width = 23

    height = 34


    topMargin = 0

    i = 0
    for i in range(0, imWidth, 23):
        for j in range(0, 34*4, 34):
            card = im.crop((i, j, width+i, j + height))
            if j == 0*34:
                rank = "H"
            elif j ==1*34:
                rank = "D"
            elif j ==2*34:
                rank = "C"
            elif j == 3*34:
                rank = "S"
            if 0*23 <= i <= 8*23:
                num = i//23+2
            elif i == 9*23:
                num = "J"
            elif i==10*23:
                num = "Q"
            elif i==11*23:
                num="K"
            elif i==12*23:
                num="A"
            card.save(f'{rank}{num}.png', 'PNG')

