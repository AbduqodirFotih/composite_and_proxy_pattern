from abc import ABC, abstractmethod

class PriceComponent(ABC):
    @abstractmethod
    def calculate_price(self) -> float:
        pass

    @abstractmethod
    def get_breakdown(self) -> str:
        pass

class BaseProductPrice(PriceComponent):
    def __init__(self, price: float):
        self._price = price

    def calculate_price(self) -> float:
        return self._price

    def get_breakdown(self) -> str:
        return f"${self._price:.2f}"

class PriceDecorator(PriceComponent):
    def __init__(self, price_component: PriceComponent):
        self._price_component = price_component

    def calculate_price(self) -> float:
        return self._price_component.calculate_price()

    def get_breakdown(self) -> str:
        return self._price_component.get_breakdown()

class SeasonalDiscountDecorator(PriceDecorator):
    def __init__(self, price_component: PriceComponent, percent: float):
        super().__init__(price_component)
        self._percent = percent

    def calculate_price(self) -> float:
        return super().calculate_price() * (1 - self._percent / 100.0)

    def get_breakdown(self) -> str:
        return f"{super().get_breakdown()} - Chegirma({self._percent:.0f}%)"

class LoyaltyDiscountDecorator(PriceDecorator):
    def __init__(self, price_component: PriceComponent, fixed_amount: float):
        super().__init__(price_component)
        self._fixed_amount = fixed_amount

    def calculate_price(self) -> float:
        return max(0.0, super().calculate_price() - self._fixed_amount)

    def get_breakdown(self) -> str:
        return f"{super().get_breakdown()} - Bonus(${self._fixed_amount:.0f})"

class TaxDecorator(PriceDecorator):
    def __init__(self, price_component: PriceComponent, tax_rate: float):
        super().__init__(price_component)
        self._tax_rate = tax_rate

    def calculate_price(self) -> float:
        return super().calculate_price() * (1 + self._tax_rate / 100.0)

    def get_breakdown(self) -> str:
        return f"{super().get_breakdown()} + Soliq({self._tax_rate:.0f}%)"

class ProductDetails(ABC):
    @abstractmethod
    def show_details(self) -> None:
        pass

class RealProductDetails(ProductDetails):
    def __init__(self, product_id: str):
        self._product_id = product_id
        self._load_heavy_data()

    def _load_heavy_data(self) -> None:
        self._high_res_image = f"rasm_{self._product_id}.jpg"
        self._full_description = "Mahsulotning to'liq parametrlari va kafolat shartlari yuklandi."

    def show_details(self) -> None:
        print(f"  Rasm: {self._high_res_image}")
        print(f"  Tavsif: {self._full_description}")

class ProductDetailsProxy(ProductDetails):
    def __init__(self, product_id: str):
        self._product_id = product_id
        self._real_details = None

    def show_details(self) -> None:
        if self._real_details is None:
            self._real_details = RealProductDetails(self._product_id)
        self._real_details.show_details()

class CatalogComponent(ABC):
    @abstractmethod
    def display(self, indent: str = "") -> None:
        pass

class ProductItem(CatalogComponent):
    def __init__(self, product_id: str, name: str, base_price: float):
        self._product_id = product_id
        self._name = name
        self._price_component = BaseProductPrice(base_price)
        self._details_proxy = ProductDetailsProxy(product_id)

    def get_price_component(self) -> PriceComponent:
        return self._price_component

    def set_price_component(self, price_component: PriceComponent) -> None:
        self._price_component = price_component

    def inspect(self) -> None:
        print(f"Mahsulot sahifasi: {self._name}")
        print(f"Narx shakllanishi: {self._price_component.get_breakdown()}")
        self._details_proxy.show_details()

    def display(self, indent: str = "") -> None:
        final_price = self._price_component.calculate_price()
        print(f"{indent}- {self._name} | Narxi: ${final_price:.2f}")

class Category(CatalogComponent):
    def __init__(self, name: str):
        self._name = name
        self._children = []

    def add(self, component: CatalogComponent) -> None:
        self._children.append(component)

    def remove(self, component: CatalogComponent) -> None:
        self._children.remove(component)

    def display(self, indent: str = "") -> None:
        print(f"{indent}[{self._name}]")
        for child in self._children:
            child.display(indent + "  ")

if __name__ == "__main__":
    root_catalog = Category("Asosiy Katalog")
    electronics = Category("Elektronika")
    phones = Category("Telefonlar")

    phone = ProductItem("P101", "iPhone 15 Pro", 1200.0)
    phone.set_price_component(SeasonalDiscountDecorator(phone.get_price_component(), 10.0))
    phone.set_price_component(LoyaltyDiscountDecorator(phone.get_price_component(), 50.0))
    phone.set_price_component(TaxDecorator(phone.get_price_component(), 12.0))

    laptop = ProductItem("P102", "MacBook Pro", 2000.0)
    laptop.set_price_component(TaxDecorator(laptop.get_price_component(), 12.0))

    phones.add(phone)
    electronics.add(phones)
    electronics.add(laptop)
    root_catalog.add(electronics)

    root_catalog.display()

    print()
    phone.inspect()
