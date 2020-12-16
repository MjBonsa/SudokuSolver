import Sudoku
import pickle


class GameSession(Sudoku.Sudoku):

    def choose_game(self, gameType):
        if gameType == 1:
            self.normal_play()
        else:
            self.bot_game()

    def bot_game(self):  # Решение введного судоку компом
        self.field = self.gen_clear_field()
        print("ВЫВОД ПРОМЕЖУТОЧНЫХ РЕЗУЛЬТАТОВ ЗАМЕДЛЯЕТ РАБОТУ ПРОГРАММЫ")
        print("если желаете отключить их отображение введите off или нажмите enter для продолжения")
        showing = "on"
        if str(input()) == "off":
            showing = "off"
        print("Заполните поле подсказами")
        print("Вводите команды типа строка, колонка, число для заполнения")
        print("или start для запсука решения")
        tmp = str(input("Строка, колонка, число или start "))
        while tmp != "start":
            row, column, number = list(map(int, tmp.split()))
            self.field[row - 1][column - 1] = number
            self.print_out(self.field)
            print("Строка, колонка, число или start ")
            tmp = str(input())
        if self.is_correct():
            field = self.gen_clear_field()
            field = self.copy_field(field, self.field)
            if self.solver(field,showing):
                print("Судоку решено")
                exit()
        print("Судоку не имеет решений")
        exit()

    def save_game(self, checkField):  # Сохранение игры
        data = {
            "field": self.field,
            "startedField": checkField
        }
        with open('gameSave.pkl', 'wb') as f:
            pickle.dump(data, f)
        print("Игра была успешно сохранена")

    def load_game(self):  # Загрузка игры
        with open('gameSave.pkl', 'rb') as f:
            data = pickle.load(f)
        return data['field'], data['startedField']

    def normal_play(self):  # Самостоятельная игра
        print("Загрузить раннее сохраненную игру? \n(load для загрзуки or любую строку для новой игры)")
        if str(input()) == "load":
            self.field, checkField = self.load_game()
            self.normal_play_body(checkField)
        difficulty = input("Введите количество известных клеток (не больше 80) ")
        try:
            difficulty = int(difficulty)
        except:
            pass
        while not isinstance(difficulty, int):
            try:
                difficulty = int(difficulty)
            except:
                print("Введите число от 0 до 80")
                difficulty = input()
        while difficulty > 80 or difficulty < 0:
            print("Введите число от 0 до 80")
            difficulty = int(input())
        self.generate(difficulty)
        checkField = self.gen_clear_field()
        checkField = self.copy_field(checkField, self.field)
        self.normal_play_body(checkField)

    def normal_play_body(self, checkField):  # Тело нормальной игры
        self.print_out(self.field)
        while self.zeros_in_field(self.field):
            print("Выберите строку, колонку, число (или save для сохранения игры)")
            tmp = str(input())
            if tmp == "save":
                self.save_game(checkField)
                exit()
            else:
                row, column, number = list(map(int, tmp.split()))
            row -= 1;
            column -= 1;
            tmp = self.field[row][column]
            self.field[row][column] = number
            if not self.is_correct():
                self.field[row][column] = tmp
                self.print_out(self.field)
                print("Нельзя поставить", number, "в", row + 1, column + 1)
                continue
            self.field[row][column] = tmp
            if checkField[row][column] != 0:
                self.print_out(self.field)
                print("Нельзя выбрать ячейку, которая принадлежит начальной подсказке ")
            else:
                self.field[row][column] = number
                self.print_out(self.field)

        if self.is_correct():
            print("Судоку решено верно")
        else:
            print("Судоку решено не верно")
