import GUI_Manager


def main():
    # Creating new GUI
    game_window = GUI_Manager.createGame()

    GUI_Manager.loop(game_window)


if __name__ == '__main__':
    main()
