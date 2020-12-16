from random import randint, sample


class Field():  # игровое поле
    def __init__(self):
        self.field = [[((i * 3 + i // 3 + j) % 9 + 1) for j in range(9)] for i in range(9)]  # генерация поля

    def swap_rows(self):  # пермещение строк
        block = randint(0, 2)
        tmpRand1, tmpRand2 = sample(range(3), 2)
        self.field[block * 3 + tmpRand1], self.field[block * 3 + tmpRand2] = self.field[block * 3 + tmpRand2], \
                                                                             self.field[block * 3 + tmpRand1]

    def swap_columns(self):  # перемещеник колнок
        self.transposition()
        self.swap_rows()
        self.transposition()

    def transposition(self):  # переворот
        self.field = [list(i) for i in zip(*self.field)]

    def swap_3_rows(self):  # пермещение двух блоков по строкам
        block1, block2 = sample(range(3), 2)
        block1 *= 3
        block2 *= 3
        j = 0
        for i in range(3):
            self.field[block1 + i], self.field[block2 + i] = self.field[block2 + i], self.field[block1 + i]
            j += 1

    def swap_3_columns(self):  # пермещение 3 колонок из одного блока
        block1, block2 = sample(range(3), 2)
        self.transposition()
        self.swap_3_rows()
        self.transposition()

    def random_mix(self):  # рандомное использование пермещения
        for _ in range(1000):
            random = randint(0, 4)
            if random == 1:
                self.swap_rows()
            elif random == 4:
                self.swap_columns()

    def print_out(self, field):  # вывод поля
        print("  1 2 3   4 5 6   7 8 9")
        for k in range(9):
            print(k + 1, end=" ")
            for j in range(9):
                print(field[k][j], end=" ")
                if (j + 1) % 3 == 0 and j != 8:
                    print("|", end=" ")
                if j == 8 and (k + 1) % 3 != 0:
                    print('')
                if (k + 1) % 3 == 0 and j == 8 and k != 8:
                    print('\n   ---------------------')
        print("")
