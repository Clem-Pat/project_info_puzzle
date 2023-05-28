from game_object.matrix import Matrix
from logic.command import Command
from graphic_interface.window import Window

def main(with_app=False):
    matrix = Matrix(size=(4, 4))
    cmd = Command(matrix)
    if with_app:
        app = Window(cmd)
        while True:
            app.update()
    else:
        cmd.begin_listener()

if __name__ == '__main__':
    main(with_app=True)
