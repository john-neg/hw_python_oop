class Info:
    def __init__(self, a):
        self.a = a

    def message(self):
        print(self.a)


class Test:
    def __init__(self):
        self.a = 15

    def ret(self):
        return Info(self.a)



t = Test
print(t.ret())