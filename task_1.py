from abc import ABC, abstractmethod

class FileSystemComponent(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_size(self) -> int:
        pass

    @abstractmethod
    def display(self, indent: str = "") -> None:
        pass

class File(FileSystemComponent):
    def __init__(self, name: str, size: int):
        self._name = name
        self._size = size

    def get_name(self) -> str:
        return self._name

    def get_size(self) -> int:
        return self._size

    def display(self, indent: str = "") -> None:
        print(f"{indent}- {self._name} ({self._size} bayt)")

class Directory(FileSystemComponent):
    def __init__(self, name: str):
        self._name = name
        self._children = []

    def add(self, component: FileSystemComponent) -> None:
        self._children.append(component)

    def remove(self, component: FileSystemComponent) -> None:
        self._children.remove(component)

    def get_name(self) -> str:
        return self._name

    def get_size(self) -> int:
        total_size = 0
        for child in self._children:
            total_size += child.get_size()
        return total_size

    def display(self, indent: str = "") -> None:
        print(f"{indent}[Papka] {self._name} (Jami: {self.get_size()} bayt)")
        for child in self._children:
            child.display(indent + "   ")

if __name__ == "__main__":
    file1 = File("Rezyume.pdf", 250000)
    file2 = File("Hisobot.docx", 120000)
    file3 = File("Dastur.py", 4500)

    docs_dir = Directory("Hujjatlar")
    docs_dir.add(file1)
    docs_dir.add(file2)

    root_dir = Directory("Mening Kompyuterim")
    root_dir.add(docs_dir)
    root_dir.add(file3)

    root_dir.display()
