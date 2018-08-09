from enum import Enum

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 4

class Mode(Enum):
    NORMAL = 0
    STRING = 1 

class BefungeInterpreter:

    def move(self):
        if self.direction == Direction.NORTH:
            self.y -= 1
        elif self.direction == Direction.EAST:
            self.x += 1
        elif self.direction == Direction.SOUTH:
            self.y += 1
        elif self.direction == Direction.WEST:
            self.x -= 1

    def push(self):
        self.stack.append(int(self.matrix[self.y][self.x]))

    def add(self):
        self.stack.append(self.stack.pop() + self.stack.pop())

    def sub(self):
        self.stack.append(self.stack.pop() - self.stack.pop())

    def mul(self):
        self.stack.append(self.stack.pop() * self.stack.pop())

    def div(self):
        a = self.stack.pop()
        self.stack.append(0 if a == 0 else int(self.stack.pop() / a))

    def mod(self):
        a = self.stack.pop()
        self.stack.append(0 if a == 0 else int(self.stack.pop() % a))

    def log_not(self):
        self.stack.append(1 if self.stack.pop() == 0 else 0)

    def gt(self):
        a = self.stack.pop()
        self.stack.append(1 if self.stack.pop() > a else 0)

    def right(self):
        self.direction = Direction.EAST

    def left(self):
        self.direction = Direction.WEST

    def up(self):
        self.direction = Direction.NORTH

    def down(self):
        self.direction = Direction.SOUTH

    def ran(self):
        self.direction = random.choice(list(Direction))

    def hor(self):
        self.direction = Direction.EAST if self.stack.pop() == 0 else Direction.WEST

    def ver(self):
        self.direction = Direction.SOUTH if self.stack.pop() == 0 else Direction.NORTH

    def toggle_str_mode(self):
        if self.mode == Mode.NORMAL:
            self.mode = Mode.STRING
        else:
            self.mode = Mode.NORMAL

    def dup(self):
        self.stack.append(0 if len(self.stack) == 0 else self.stack[-1])

    def swp(self):
        if len(self.stack) == 1:
            self.stack.append(0)
        else:
            self.stack[-1],self.stack[-2] = self.stack[-2], self.stack[-1]

    def dis(self):
        self.stack.pop()
            
    def pop_int(self):
        return self.stack.pop()

    def pop_ascii(self):
        return chr(self.stack.pop()) 

    def skip(self):
        self.move()

    def put(self):
        y = self.stack.pop()
        x = self.stack.pop()
        self.matrix[y][x] = chr(self.stack.pop()) 

    def get(self):
        y = self.stack.pop()
        x = self.stack.pop()
        return self.matrix[y][x] 

    def end(self):
        self.finished = True
        
    def noop(self):
        pass

    def __init__(self):
        self.stack = []
        self.matrix = []
        self.x = 0
        self.y = 0    
        self.direction = Direction.EAST
        self.finished = False 
        self.mode = Mode.NORMAL
        self.funcs = {
            '0':self.push,
            '1':self.push,
            '2':self.push,
            '3':self.push,
            '4':self.push,
            '5':self.push,
            '6':self.push,
            '7':self.push,
            '8':self.push,
            '9':self.push,
            '+':self.add,
            '-':self.sub,
            '*':self.mul,
            '/':self.div,
            '%':self.mod,
            '!':self.log_not,
            '`':self.gt,
            '>':self.right,
            '<':self.left,
            '^':self.up,
            'v':self.down,
            '?':self.ran,
            '_':self.hor,
            '|':self.ver,
            '"':self.toggle_str_mode,
            ':':self.dup,
            '\\':self.swp,
            '$':self.dis,
            '.':self.pop_int,
            ',':self.pop_ascii,
            '#':self.skip,
            'p':self.put,
            'g':self.get,
            '@':self.end,
            ' ':self.noop
        }
    def interpret(self, input):
        result = ''
        self.matrix.extend(input.split('\n'))
        while(not(self.finished)):
            op  = self.matrix[self.y][self.x] 
            if self.mode == Mode.NORMAL or op == '"':
                func = self.funcs[op]
                ret = func()
                if ret is not None: result += str(ret)  
            else:
                self.stack.append(ord(op))
            self.move()
        return result
if __name__ == "__main__":
    print(BefungeInterpreter().interpret(">987v>.v\nv456<  :\n>321 ^ _@"))
