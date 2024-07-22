

class InfoBlob
    def __init__(self, data_type, verbose=True):
        self.the_data = None
        self.data_type = data_type
        self.verbose = verbose
        self.valid = False
        print(f'Instantiated InfoBlob with type = {self.data_type}')

    def get_the_data(self):
        if self.verbose:
            print(f'(InfoBlob) the_data == {self.the_data}')
        return self.the_data

    def get_the_type(self):
        if self.verbose:
            print(f'(InfoBlob) data_type == {self.data_type}')
        return self.data_type

    def set_the_data(self, new_data):
        self.the_data = new_data
        print(f'(InfoBlob) new value for   data_type == {self.data_type}')


