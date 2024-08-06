class FileHandler:

    def read_file(self, inpfilepath):
        try:
            fileContents = open(inpfilepath, 'r').read()
            return fileContents
        except FileNotFoundError:
            print('Error reading input file, check if filepath exists!')

    def check_maze_dimensions(self, inpfilepath):
        contents = self.read_file(inpfilepath).split('\n')
        if contents is None:
            return False
        
        num_rows = len(contents)
        if num_rows > 24:
            print(f'Maze height exceeds 24 rows: {num_rows} rows.')
            return False
        
        num_cols = len(contents[0].strip())
        if num_cols > 36:
            print(f'Maze width exceeds 36 columns: {num_cols} columns.')
            return False
        
        valid_chars = {'.', 's', 'X', 'e'}
        start_count = 0
        end_count = 0
        
        for line in contents:
            line = line.strip()
            if len(line) != num_cols:
                print(f'Inconsistent number of columns in row: {len(line)}.')
                return False
            
            if not all(char in valid_chars for char in line):
                print(f'Map should contain only ., s, X, e. Unknown character in row: {line}')
                return False
            
            # Count occurrences of 's' and 'e'
            start_count += line.count('s')
            end_count += line.count('e')
        
        if start_count != 1:
            print(f'Maze should contain exactly one start point (s), found {start_count}.')
            return False
        
        if end_count != 1:
            print(f'Maze should contain exactly one end point (e), found {end_count}.')
            return False
        return contents