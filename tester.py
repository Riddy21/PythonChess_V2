from typing import Any


# HELLLLLO

class tester(object):
    def __init__(self):
        self.game = ''
        self.hello = ''

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)


tester = tester()
setattr(tester, 'game', "helllllllo")
print(getattr(tester, 'game'))
