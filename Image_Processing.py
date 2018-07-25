from datetime import datetime
import cv2



class Image_Processing:

    @staticmethod
    def SaveImage(img, fileLocation):
        print('Saving image')
        outfile = '{0}_{1}.jpg'.format(fileLocation, datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
        cv2.imwrite(outfile, img)
        print('Image saved')
