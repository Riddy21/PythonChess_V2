import GUI as gui

#TODO: Combine Board GUI and Menu objects into one object

def main():
    # Creating new GUI
    game_Window = gui.create_window()

    gui.loop(game_Window)


if __name__ == '__main__':
    main()
