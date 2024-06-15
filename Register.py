class Register():
    def __init__(self, name, addr, len, type):
        self.name = name
        self.addr = addr
        self.len = len
        self.type = type

    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return f"{self.name}@{self.addr} ({self.type} : {self.len})"
