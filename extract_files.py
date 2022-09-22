from PIL import Image
from threading import Thread
from user_data import UserData

class ExtractFiles(Thread):

    def __init__(self, slide, image_name, level, x_list, y_list):
        self.path_to_save = "C:/thyroid_user_files/extracted/"+image_name+"/"
        self.slide = slide
        self.level = level
        self.x_list = x_list
        self.y_list = y_list
        user_data = UserData(self.path_to_save)
        super().__init__()

    def run(self):
        image = None
        for col in self.x_list:
            for row in self.y_list:
                image_i = Image.fromarray(self.slide.get_tile(self.level, (col, row)))

                """
                Concat the images to image and save
                """
        image.save(self.path_to_save+"/"+str(self.level)+"_"+str(self.x)+"_"+str(self.y)+".png")
