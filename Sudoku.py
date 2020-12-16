from random import randint, sample
import sys
import GameField

sys.setrecursionlimit = 1000


class Sudoku(GameField.Field):
    def solver(self, field, showing):  # рекурсивная решалка судоку
        length = 0
        while length < 2:  # Ищем поля где значение определенно однозначно и заполняем их
            for row in range(9):
                for column in range(9):
                    if field[row][column] == 0:  # Если нашли пустое пошли
                        suitable = self.find_suitable(field, row, column)  # Смотрим подходящие значения для поля
                        length = len(suitable)  # Храним количество подходящих значений для поля
                        topSuitable = suitable  # Запоминаем количество вариантов для поля
                        pos = (row, column)  # и положение поля на случай если не найдем однозначное
                        if length == 0:  # Если нет значений, которыми можно заполнить поле - судоку не имеет решения
                            return False  # или путь для решения выбран неверно
                        if length == 1:  # Если нашли единственное значение для - используем его
                            field[row][column] = suitable.pop()
                            if showing == "on":
                                print("\n", row + 1, column + 1, field[row][column])
                                self.print_out(field)
                            continue
            if not self.zeros_in_field(field):  # Если не осталось нулей на поле - судоку решено
                if showing != "check":
                    self.print_out(field)
                return True
        while suitable:  # Пытаемся засунуть какое-либо возможное значение для поля которое мы запоминали
            fieldCopy = self.gen_clear_field()
            fieldCopy = self.copy_field(fieldCopy, field)  # Копируем матрицу на случай неправильного выбора
            fieldCopy[pos[0]][pos[1]] = suitable.pop()  # Снимаем крайнее значенение
            if showing == "on":
                print("\n", pos[0] + 1, pos[1] + 1, fieldCopy[pos[0]][pos[1]])
                self.print_out(field)
            if self.solver(fieldCopy, showing):  # Запускаем рекурсию для данного значения
                field = self.copy_field(field, fieldCopy)
                return True
        return False

    def gen_clear_field(self):  # Создание чистого поля
        return [[0 for i in range(9)] for j in range(9)]

    def copy_field(self, field1, field2):  # Копирование полей
        for i in range(9):
            for j in range(9):
                field1[i][j] = field2[i][j]
        return field1

    def generate(self, difficulty):  # Удаление ячеек в полном судоку
        self.random_mix()
        # Удаление для появления однозначных ячеек
        # (Получаем судоку со сложностью примерно 40 с одзнозначным решением )
        for _ in range(1000):
            if self.difficulty_count() == difficulty:
                break
            row, column = randint(0, 8), randint(0, 8)
            while self.field[row][column] == 0:
                row, column = randint(0, 8), randint(0, 8)
            tmp = self.field[row][column]
            self.field[row][column] = 0
            if len(self.find_suitable(self.field, row, column)) > 1:
                self.field[row][column] = tmp
        # Добиваем до заданной сложности с большой вероятностью теряя
        # одназначность решения
        while self.difficulty_count() != difficulty:
            row, column = randint(0, 8), randint(0, 8)
            if self.field[row][column] != 0:
                tmp = self.field[row][column]
                self.field[row][column] = 0
                field = self.gen_clear_field()
                field = self.copy_field(field, self.field)
                if self.solver(field, "check"):
                    continue
                self.field[row][column] = tmp

    def difficulty_count(self):  # Подсчет сложности
        ans = 0
        for i in range(9):
            ans += self.field[i].count(0)
        return (81 - ans)

    def find_suitable(self, field, yPos, xPos, ):  # поиск возможных подходящих
        suitable = {v for v in range(1, 10)}
        suitable -= set(field[yPos])
        suitable -= set(field[i][xPos] for i in range(9))
        block = ((3 * (yPos // 3)), (3 * (xPos // 3)))
        for i in range(3):
            for j in range(3):
                tmp = set([field[block[0] + i][block[1] + j]])
                suitable -= tmp
        return suitable

    def is_correct(self):  # Правильно ли составлено судоку
        for row in range(9):
            for column in range(9):
                tmp = set()
                for i in range(9):
                    if not self.field[row][i] in tmp:
                        if self.field[row][i] != 0:
                            tmp.add(self.field[row][i])
                    else:
                        return False
                tmp = set()
                for i in range(9):
                    if not self.field[i][column] in tmp:
                        if self.field[i][column] != 0:
                            tmp.add(self.field[i][column])
                    else:
                        return False
                tmp = set()
                block = ((3 * (row // 3)), (3 * (column // 3)))
                for i in range(3):
                    for j in range(3):
                        if not self.field[block[0] + i][block[1] + j] in tmp:
                            if self.field[block[0] + i][block[1] + j] != 0:
                                tmp.add(self.field[block[0] + i][block[1] + j])
                        else:
                            return False
        return True

    def zeros_in_field(self, field):  # Есть ли нули на поле
        for i in range(9):
            if 0 in field[i]:
                return True
        return False
