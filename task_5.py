from abc import ABC, abstractmethod

class UIComponent(ABC):
    @abstractmethod
    def render(self) -> None:
        pass

    @abstractmethod
    def add(self, component: "UIComponent") -> None:
        pass

class Button(UIComponent):
    def __init__(self, label: str):
        self._label = label

    def render(self) -> None:
        print(f"[Tugma: {self._label}]")

    def add(self, component: UIComponent) -> None:
        raise TypeError("Tugma ichiga yangi element qo'shib bo'lmaydi.")

class TextBox(UIComponent):
    def __init__(self, text: str):
        self._text = text

    def render(self) -> None:
        print(f"[Matn maydoni: {self._text}]")

    def add(self, component: UIComponent) -> None:
        raise TypeError("Matn maydoni ichiga yangi element qo'shib bo'lmaydi.")

class Panel(UIComponent):
    def __init__(self):
        self._children = []

    def add(self, component: UIComponent) -> None:
        self._children.append(component)

    def render(self) -> None:
        print("{Oyna ochildi}")
        for child in self._children:
            child.render()
        print("{Oyna yopildi}")

class UIDecorator(UIComponent):
    def __init__(self, component: UIComponent):
        self._component = component

    def render(self) -> None:
        self._component.render()

    def add(self, component: UIComponent) -> None:
        self._component.add(component)

class BorderDecorator(UIDecorator):
    def render(self) -> None:
        print("+--- Ramka ---+")
        super().render()
        print("+-------------+")

class ScrollDecorator(UIDecorator):
    def render(self) -> None:
        print("[Aylantirish paneli / Scroll qo'shildi]")
        super().render()

class TooltipDecorator(UIDecorator):
    def __init__(self, component: UIComponent, tooltip: str):
        super().__init__(component)
        self._tooltip = tooltip

    def render(self) -> None:
        super().render()
        print(f"Ko'rsatma: {self._tooltip}")

if __name__ == "__main__":
    submit_button = Button("Saqlash")
    decorated_button = BorderDecorator(submit_button)

    main_panel = Panel()
    main_panel.add(decorated_button)
    main_panel.add(TextBox("Elektron pochta manzili"))

    scrollable_panel = ScrollDecorator(main_panel)
    scrollable_panel.render()
