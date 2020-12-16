import GameSession as gs


def main():  # Запуск игры
    session = gs.GameSession()
    gameType = input('Выберите тип игры: самостоятельный(1) или бот(2) ')
    try:
        gameType = int(gameType)
    except:
        pass
    while gameType != 1 and gameType != 2:
        print("Выберите 1 или 2 ")
        gameType = (str(input()))
        try:
            gameType = int(gameType)
        except:
            print("Выберите 1 или 2 ")
    session.choose_game(gameType)


main()
