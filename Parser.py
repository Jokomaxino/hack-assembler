class Parser:
    def __init__(self, filename):
        self.filename = filename
        self.f = open(self.filename, 'r').readlines()
        self.lines = [i.strip() for i in self.f]
        self.currentCommand = ''
    
    def hasMoreCommands(self):
        return len(self.lines) > 0
    
    def advance(self):
        assert(self.hasMoreCommands())
        line = self.lines.pop(0).strip()
        while (line[:2] == '//' or line == '') and self.hasMoreCommands():
            line = self.lines.pop(0).strip()
        self.currentCommand = line.split('//')[0].strip()
    
    def reset(self):
        self.lines = self.f
        self.currentCommand = ''
    
    def commandType(self):
        if self.currentCommand[0] == '@':
            return 'A_COMMAND'
        elif '=' in self.currentCommand or ';' in self.currentCommand:
            return 'C_COMMAND'
        elif self.currentCommand[0] == '(' and self.currentCommand[-1] == ')':
            return 'L_COMMAND'
        raise Exception("invalid command")

    def symbol(self):
        command_type = self.commandType()
        assert( command_type == 'A_COMMAND' or command_type == 'L_COMMAND')
        if command_type  == 'A_COMMAND':
            return self.currentCommand[1:]
        elif command_type == 'L_COMMAND':
            return self.currentCommand[1:-1]

    def comp(self):
        assert(self.commandType() == 'C_COMMAND')
        command = self.currentCommand.split(';')[0]
        if '=' in command:
            command = command.split('=')[1]
        return command
    
    def dest(self):
        assert(self.commandType() == 'C_COMMAND')
        if '=' in self.currentCommand:
            return self.currentCommand.split('=')[0]  
        return ''

    def jump(self):
        assert(self.commandType() == 'C_COMMAND')
        if ';' in self.currentCommand:
            return self.currentCommand.split(';')[1]
        return ''
