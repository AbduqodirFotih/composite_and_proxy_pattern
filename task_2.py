from abc import ABC, abstractmethod

class Image(ABC):
    @abstractmethod
    def display(self) -> None:
        pass

class RealImage(Image):
    def __init__(self, filename: str):
        self._filename = filename
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        print(f"{self._filename} diskdan xotiraga yuklanmoqda...")

    def display(self) -> None:
        print(f"{self._filename} ekranda ko'rsatildi.")

class ImageProxy(Image):
    def __init__(self, filename: str):
        self._filename = filename
        self._real_image = None

    def display(self) -> None:
        if self._real_image is None:
            self._real_image = RealImage(self._filename)
        self._real_image.display()

if __name__ == "__main__":
    image1 = ImageProxy("tabiat_manzarasi.jpg")
    image2 = ImageProxy("shahar_markazi.jpg")

    print("Rasmlar ro'yxati shakllantirildi.")

    image1.display()
    image1.display()
    image2.display()
