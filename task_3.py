from abc import ABC, abstractmethod

class TextComponent(ABC):
    @abstractmethod
    def get_content(self) -> str:
        pass

class PlainText(TextComponent):
    def __init__(self, text: str):
        self._text = text

    def get_content(self) -> str:
        return self._text

class TextDecorator(TextComponent):
    def __init__(self, component: TextComponent):
        self._component = component

    def get_content(self) -> str:
        return self._component.get_content()

class BoldDecorator(TextDecorator):
    def get_content(self) -> str:
        return f"<b>{super().get_content()}</b>"

class ItalicDecorator(TextDecorator):
    def get_content(self) -> str:
        return f"<i>{super().get_content()}</i>"

class ColorDecorator(TextDecorator):
    def __init__(self, component: TextComponent, color: str):
        super().__init__(component)
        self._color = color

    def get_content(self) -> str:
        return f"<font color='{self._color}'>{super().get_content()}</font>"

class UpperCaseDecorator(TextDecorator):
    def get_content(self) -> str:
        return super().get_content().upper()

if __name__ == "__main__":
    text = PlainText("Dasturga xush kelibsiz")
    text = BoldDecorator(text)
    text = ItalicDecorator(text)
    text = ColorDecorator(text, "red")

    print(text.get_content())

    headline = UpperCaseDecorator(PlainText("muhim bildirishnoma"))
    print(headline.get_content())
