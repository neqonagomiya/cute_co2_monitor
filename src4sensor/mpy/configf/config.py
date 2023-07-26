import ure

class Config:
    def __init__(self):
        self.config_path = "./configf/config.txt"
        self.__make_attribute_list(self.config_path)

    def __make_attribute_list(self, config_path):
        f = open(config_path)
        s = f.read()
        f.close()
        regex = ure.compile("[=\n]")
        self.s_splited_list = regex.split(s)
        
    def get(self, attribute_name:str) -> str:
        for i in range(0, len(self.s_splited_list)-1, 2):
            if self.s_splited_list[i] == attribute_name:
                self.attribute_val = self.s_splited_list[i+1]
        return self.attribute_val