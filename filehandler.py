class FileHandler:
    def read_file(self, inpfilepath):
        try:
            fileContents = open(inpfilepath, 'r').read()
            return fileContents
        except FileNotFoundError:
            print('Error reading input file, check if filepath exists!')
    def readlines_file(self, inpfilepath):
        try:
            fileContents = open(inpfilepath, 'r').readlines()
            return fileContents
        except FileNotFoundError:
            print('Error reading input file, check if filepath exists!')
    def write_file(self, inpfilepath, contents):
        try:
            open(inpfilepath, 'w').write(contents)
            return 1
        except FileNotFoundError:
            print('Error writing output file, check if filepath exists!')
    def append_file(self, filename,contents):
        try:
            with open(filename, 'a') as f:
                f.write(contents)
            return 1
        except FileNotFoundError:
            print('Error writing output file, check if filepath exists!')
    def check_file(self, output):
        return output == None