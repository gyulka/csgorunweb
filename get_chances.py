import sqlite3


class Interval:
    def __init__(self, minn, maxx, name='Undefined'):
        self.minn = minn
        self.maxx = maxx
        self.name = name

    def __contains__(self, item):
        return self.minn <= item <= self.maxx

    def get_name(self):
        return self.name


RED = Interval(1.0, 1.19, 'R')
BLUE = Interval(1.2, 1.99, 'B')
PURPLE = Interval(2.0, 3.99, 'P')
GREEN = Interval(4.0, 7.99, 'Gr')
GOLD = Interval(8, 19.99, 'Gl')
LIGHT_BLUE = Interval(20, 99999999.0, 'L')


class Tactic:
    LEN = 3

    def __init__(self, lis: list):
        lis = lis[-Tactic.LEN:]
        self.lis = []
        if True:
            self.flag = True
            for id1, crash in lis:
                for inter in [RED, BLUE, PURPLE, GREEN, GOLD, LIGHT_BLUE]:
                    if crash in inter:
                        self.lis.append(inter)
        else:
            self.flag = False

    def __call__(self, lis: list):
        for i in range(Tactic.LEN):
            if not (lis[i] in self.lis[i]):
                return False
        return self.flag

    def __repr__(self):
        return ' '.join(map(lambda x: x.get_name(), self.lis))


def db_init():
    return sqlite3.connect('db1.db')


def get_chances(tactic, k=1.2):
    lis = []
    ans = []
    con = db_init()
    for id1, crash in con.execute('select id,crash from crashes').fetchall()[-9000:]:
        lis.append(crash)
        if len(lis) == 11:
            if tactic(lis[:-1]):
                ans.append(lis[-1])
            lis.pop(0)
    if ans:
        x = 0
        for i in ans:
            if i >= k:
                x += 1
        return x / len(ans) - 1 / len(ans)
    return 0.0


def main():
    con = db_init()
    tactic = Tactic([(id1, cash) for id1, cash in con.execute('select id,crash from crashes').fetchall()[-10:]])
    print(tactic)
    x = get_chances(tactic, 1.2)
    print(f'шанс на коэфф 1.2: {x}')
    return x


if __name__ == '__main__':
    main()
