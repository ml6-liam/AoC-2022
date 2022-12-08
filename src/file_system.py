import re

class FsObject():
    name: str
    parent: object
    obj_type: str # 1 = dir, 0 = file
    size: int

class File(FsObject):
    
    def __init__(self, name: str, size: int, parent: object):
        self.name = name
        self.size = size
        self.parent = parent
        self.obj_type = "file"

    def list_file(self):
        return f"- {self.name} (file, {self.size})"

class Directory(FsObject):
    contents: dict
    def __init__(self, name: str, parent: object):
        self.name = name
        self.parent = parent
        self.contents = dict()
        self.size = 0
        self.obj_type = "dir"

    def add_file(self, name: str, size: int):
        self.contents[name] = File(name, size, self)
        self.update_size()
    
    def add_sub_dir(self, name):
        new_sub_dir = Directory(name, self)
        self.contents[name] = new_sub_dir
        return new_sub_dir
    
    def sum_contents(self):
        sum = 0
        for (name, obj) in self.contents.items():
            if obj.obj_type == "dir":
                sum += obj.sum_contents()
            else:
                sum += obj.size
    
    def list_files(self):
        output_lines = [f"- {self.name} (dir, {self.size})"]
        for (name, obj) in self.contents.items():
            if obj.obj_type == "dir":
                sub_dir_lines = obj.list_files()
                for line in sub_dir_lines:
                    output_lines.append('    '+line)
            elif obj.obj_type == "file":
                output_lines.append('    '+obj.list_file())
        return output_lines
    
    def update_size(self):
        self.size = 0
        for name, child in self.contents.items():
            self.size += child.size
        if self.parent is not None:
            self.parent.update_size()


class FileTreeParser():
    cwd: object
    root_dir: object
    commands: list
    commands_buffer: list

    def __init__(self):
        self.root_dir = Directory("/", None)
        self.cwd = self.root_dir

    def load_commands(self, commands: list):
        self.commands = commands.copy()
        self.commands_buffer = commands.copy()
    
    def run_commands(self):
        while len(self.commands_buffer) > 0:
            command = self.commands_buffer.pop(0)
            print(command)
            if 'ls' in command:
                self.ls()
            elif 'cd' in command:
                cs = re.split(' ', command)
                name = cs[2]
                self.cwd = self.cd(name)

    def ls(self):
            while (len(self.commands_buffer)>0) and (self.commands_buffer[0][0] != '$'):
                command = self.commands_buffer.pop(0)
                desc, name = re.split(' ', command)
                in_cwd = (name in self.cwd.contents)
                if desc == "dir":
                    if not in_cwd:
                        self.cwd.add_sub_dir(name)
                else:
                    if not in_cwd:
                        self.cwd.add_file(name, int(desc))

    def cd(self, name):
        if name == "..":
            if self.cwd.name != "/":
                return self.cwd.parent
            else:
                return self.cwd
        elif name == '/':
            return self.root_dir
        elif name in self.cwd.contents:
            if self.cwd.contents[name].obj_type == "dir":
                return self.cwd.contents[name]
            else:
                raise Exception 
        else:
            return self.cwd.add_sub_dir(name)

    def print_tree(self):
        print_lines = self.root_dir.list_files()
        for line in print_lines:
            print(line)
    
    def sum_dirs_under_threshold(self, threshold, dir):
        total=0
        if dir is None:
            dir=self.root_dir
        for name, obj in dir.contents.items():
            if obj.obj_type == "dir":
                if obj.size < threshold:
                    total+=obj.size
                total+=self.sum_dirs_under_threshold(threshold, obj)
        return total
    
    def list_dirs_over_threshold(self, threshold, dir=None):
        big_dirs=[]
        if dir is None:
            dir=self.root_dir
        for name, obj in dir.contents.items():
            if obj.obj_type == "dir":
                if obj.size > threshold:
                    big_dirs+=[obj]
                big_dirs+=self.list_dirs_over_threshold(threshold, obj)
        return big_dirs

    def smallest_to_delete(self, update_size):
        free_space = 70000000 - self.root_dir.size
        req_space = update_size - free_space
        if req_space <= 0:
            print(f"enough space for update - no del required")
            return
        
        candidates = self.list_dirs_over_threshold(req_space, None)
        print(f"found {len(candidates)} possible directories")
        smallest = candidates.pop(0)
        if len(candidates) != 0:
            print("finding smallest")
            for i, candidate in enumerate(candidates):
                if i == 0:
                    smallest = candidate
                    continue
                elif candidate.size < smallest.size:
                    smallest = candidate
        print(f'The smallest directory to delete to free up {req_space} is {smallest.name} with a total size of {smallest.size}')
            
    def clear_tree(self):
        print(f'Timbeeerrrrr')
        self.root_dir = Directory("/", None)
        print(f'CREEEEAAASH')
