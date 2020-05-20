import GUI as gui
import GUI_button_handler as hdlr

#TODO: Combine Board GUI and Menu objects into one object

def main():
    # Create new Game
    game_Window = gui.create_window()

    gui.loop(game_Window)


if __name__ == '__main__':
    main()
