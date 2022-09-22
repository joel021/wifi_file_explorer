import json
import os

"""
This class manage all user information persistence, in json files
"""
class UserData():

    def __init__(self, path='/thyroid_user_files'):
        self.path = json.load(open("instalation_path.json","r"))['path']+path
        self._create_path(self.path)

    """
    complete URI. Ex.: C:/sub1/sub2...
    """
    def _create_path(self, path):
        sub_ps = path.split("/")
        uri = sub_ps[0]
        for i in range(1, len(sub_ps)):
            uri = uri+"/"+sub_ps[i]

            if not os.path.isdir(uri):
                os.mkdir(uri)

    def save_user_path(self, path_str):

        uri_str = (self.path+'/user_paths.json').replace("\\","/")

        if os.path.isfile(uri_str):
            f = open(uri_str, 'r', encoding='utf-8')
            try:
                list_urls = json.load(f)
            except:
                list_urls = []
            f.close()
        else:
            list_urls = []
        
        if not path_str in list_urls:
            list_urls.append(path_str)
            f = open(uri_str, 'w', encoding='utf-8')
            f.write(json.dumps(list_urls))
            f.close()

        return json.dumps(list_urls)
    
    #return a list
    def load_user_paths(self):
        try:
            f = open(self.path+"/user_paths.json", 'r', encoding='utf8')
            list_urls = json.load(f)
            f.close()
        except:
            return []
        return list_urls

    def remove_path(self, path_str):

        try:
            f = open(self.path+"/user_paths.json", 'r', encoding='utf8')
            list_urls = json.load(f)
            f.close()
        except:
            list_urls = []

        if path_str in list_urls:
            list_urls.remove(path_str)
            f = open(self.path+"/user_paths.json", 'w', encoding='utf8')
            f.write(json.dumps(list_urls))
            f.close()
        
        return json.dumps(list_urls)

    def clear(self):
        try:
            f = open(self.path+"/user_paths.json", 'w', encoding='utf8')
            f.write("")
            f.close()
        except:
            pass
