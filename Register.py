class Register():
    def __init__(self, name: str, addr: int, len: int, type: str):
        self.name: str = name
        self.addr: int = addr
        self.len: int = len
        self.type: str = type

    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return f"{self.name}@{self.addr} ({self.type} : {self.len})"
