class Read_from_text:

    @staticmethod
    def connect_data():
        import os.path
        scriptpath = os.path.dirname(__file__)
        filename = os.path.join(scriptpath, 'user.txt')
        with open(filename) as f:
            data = f.read()
            data = data.strip("\n")
            return data