import re
from utils import parse_file_lines

class Tree():
    height: int
    visible: bool
    coordinates: tuple
    parent: object
    scenic_score: int
    def __init__(self, height, coordinates, parent, visible=False):
        self.height = height
        self.visible = visible
        self.coordinates = coordinates
        self.parent = parent
        self.scenic_score = 0

class Forrest():
    trees: list
    visible_trees: int
    def __init__(self):
        self.trees = []
        self.visible_trees = 0
    
    def parse_tree_map(self, map_lines: list):
        total_lines = len(map_lines)
        for row_number, row in enumerate(map_lines):
            new_row = []
            splits = re.split("", row)
            trimmed_row = splits[1:len(splits)-1]
            row_width = len(trimmed_row)-1
            for col_number, tree_height in enumerate(trimmed_row):
                first_last_col = ((col_number == 0) or (col_number == row_width))
                first_last_row = ((row_number == 0) or (row_number == total_lines-1))
                print(f"({col_number} {first_last_col}), ({row_number}, {first_last_row})")
                edge = (first_last_col or first_last_row)
                new_row.append(Tree(int(tree_height), 
                                    (col_number, row_number), 
                                    self,
                                    edge))
            self.trees.append(new_row)
    
    def assess_visibility(self):
        for row in self.trees:
            for tree in row:
                top, top_d = self.visible_from_top(tree)
                bot, bot_d = self.visible_from_bottom(tree)
                left, left_d = self.visible_from_left(tree)
                right, right_d = self.visible_from_right(tree)
                print(f'tree {tree.coordinates} - top:{top}, bot:{bot}, left:{left}, right:{right}')
                if top or bot or left or right:
                    tree.visible = True
                tree.scenic_score = (top_d * bot_d * left_d * right_d)
                print(f'tree {tree.coordinates} - {tree.visible}')
    

    def show_visibility(self):
        for row in self.trees:
            for tree in row:
                print(f'tree at pos {tree.coordinates} - visible: {tree.visible}')  

    def most_scenic(self):
        most_scenic_score = 0
        most_scenic_tree: object
        for row in self.trees:
            for tree in row:
                if tree.scenic_score > most_scenic_score:
                    most_scenic_score = tree.scenic_score
                    most_scenic_tree = tree
        print(f'tree at pos {most_scenic_tree.coordinates} has highest scenic score of {most_scenic_score}')

     
    def count_visible(self):
        for row in self.trees:
            for tree in row:
                print(tree.visible)
                if tree.visible:
                    self.visible_trees += 1
            print('\n')
        return self.visible_trees

    def visible_from_top(self, tree):
        (target_col, target_row) = tree.coordinates
        distance = 0
        candidates = self.trees[0:target_row]
        candidates.reverse()
        for row in candidates:
            test_tree = row[target_col]
            distance = tree.coordinates[1] - test_tree.coordinates[1]
            if test_tree.height >= tree.height:
                print(f'tree at pos {tree.coordinates} not visible from top') 
                return False, distance
        print(f'tree at pos {tree.coordinates} visible from top') 
        return True, distance
    
    def visible_from_bottom(self, tree):
        (target_col, target_row) = tree.coordinates
        distance = 0
        for row in self.trees[target_row+1:]:
            test_tree = row[target_col]
            distance = test_tree.coordinates[1] - tree.coordinates[1]
            if test_tree.height >= tree.height: 
                print(f'tree at pos {tree.coordinates} not visible from bottom') 
                return False, distance
        print(f'tree at pos {tree.coordinates} visible from bottom') 
        return True, distance
    
    def visible_from_left(self, tree):
        (target_col, target_row) = tree.coordinates
        row = self.trees[target_row]
        distance = 0
        candidates = row[0:target_col]
        candidates.reverse()
        for test_tree in candidates:
            distance = tree.coordinates[0] - test_tree.coordinates[0]
            if test_tree.height >= tree.height:
                print(f'tree at pos {tree.coordinates} not visible from left') 
                return False, distance
        print(f'tree at pos {tree.coordinates} visible from left') 
        return True, distance
    
    def visible_from_right(self, tree):
        (target_col, target_row) = tree.coordinates
        row = self.trees[target_row]
        distance = 0
        for test_tree in row[target_col+1:]:
            distance = test_tree.coordinates[0] - tree.coordinates[0]
            if test_tree.height >= tree.height:
                print(f'tree at pos {tree.coordinates} not visible from right') 
                return False, distance
        print(f'tree at pos {tree.coordinates} visible from right') 
        return True, distance

    def clear_forest(self):
        self.trees = []
    
input = ['30373',
         '25512', '65332',
         '33549', '35390']

if __name__ == '__main__':
    map_lines = parse_file_lines('./data/forest.txt')
    forest = Forrest()
    forest.parse_tree_map(map_lines)
    forest.assess_visibility()
    total_visible = forest.count_visible()
    print(total_visible)
    forest.most_scenic()