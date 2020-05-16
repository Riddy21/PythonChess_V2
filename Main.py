import GUI as gui

#TODO: Combine Board GUI and Menu objects into one object

def main():
    # Creating new GUI
    game_GUI = gui.create_game()

    print(game_GUI)
    gui.loop(game_GUI)


if __name__ == '__main__':
    main()
