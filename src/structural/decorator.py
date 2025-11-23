"""
DECORATOR PATTERN - Menu Item Decorators
Menambahkan fitur ekstra ke menu items secara dinamis
"""

from abc import ABC, abstractmethod
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.restaurant import MenuItem


class MenuItemDecorator(ABC):
    """
    Abstract Decorator untuk Menu Items

    Teori:
    - Decorator Pattern adalah structural pattern yang memungkinkan penambahan
      behavior/responsibility baru ke objects secara dinamis
    - Decorator membungkus object asli dan menambahkan functionality
    - Alternative yang lebih flexible dari subclassing untuk extend functionality

    Use Case Restaurant:
    - Customer bisa menambah extras ke menu: Extra Cheese, Extra Topping, Large Size, etc
    - Setiap extra menambah harga ke base menu price
    - Decorator memungkinkan stacking multiple extras tanpa modify MenuItem class
    - Contoh: Burger + Extra Cheese + Extra Patty + Large Size
    """

    def __init__(self, menu_item: MenuItem):
        self._menu_item = menu_item

    @abstractmethod
    def get_description(self) -> str:
        """Get deskripsi menu dengan extras"""
        pass

    @abstractmethod
    def get_price(self) -> float:
        """Get total price dengan extras"""
        pass

    def get_base_item(self) -> MenuItem:
        """Get original menu item"""
        return self._menu_item

    def __str__(self):
        return f"{self.get_description()} - Rp {self.get_price():,.0f}"


class ExtraCheeseDecorator(MenuItemDecorator):
    """Decorator untuk menambah Extra Cheese"""

    EXTRA_PRICE = 5000

    def get_description(self) -> str:
        base_desc = (
            self._menu_item.item_name
            if isinstance(self._menu_item, MenuItem)
            else self._menu_item.get_description()
        )
        return f"{base_desc} + Extra Cheese"

    def get_price(self) -> float:
        base_price = (
            self._menu_item.base_price
            if isinstance(self._menu_item, MenuItem)
            else self._menu_item.get_price()
        )
        return base_price + self.EXTRA_PRICE


class ExtraToppingDecorator(MenuItemDecorator):
    """Decorator untuk menambah Extra Topping"""

    def __init__(
        self, menu_item: MenuItem, topping_name: str, topping_price: float = 7000
    ):
        super().__init__(menu_item)
        self.topping_name = topping_name
        self.topping_price = topping_price

    def get_description(self) -> str:
        base_desc = (
            self._menu_item.item_name
            if isinstance(self._menu_item, MenuItem)
            else self._menu_item.get_description()
        )
        return f"{base_desc} + Extra {self.topping_name}"

    def get_price(self) -> float:
        base_price = (
            self._menu_item.base_price
            if isinstance(self._menu_item, MenuItem)
            else self._menu_item.get_price()
        )
        return base_price + self.topping_price


class LargeSizeDecorator(MenuItemDecorator):
    """Decorator untuk upgrade ke Large Size"""

    EXTRA_PRICE = 10000

    def get_description(self) -> str:
        base_desc = (
            self._menu_item.item_name
            if isinstance(self._menu_item, MenuItem)
            else self._menu_item.get_description()
        )
        return f"{base_desc} (Large Size)"

    def get_price(self) -> float:
        base_price = (
            self._menu_item.base_price
            if isinstance(self._menu_item, MenuItem)
            else self._menu_item.get_price()
        )
        return base_price + self.EXTRA_PRICE


class ExtraSpicyDecorator(MenuItemDecorator):
    """Decorator untuk menambah Extra Spicy Level"""

    EXTRA_PRICE = 3000

    def __init__(self, menu_item: MenuItem, spicy_level: int = 1):
        super().__init__(menu_item)
        self.spicy_level = spicy_level

    def get_description(self) -> str:
        base_desc = (
            self._menu_item.item_name
            if isinstance(self._menu_item, MenuItem)
            else self._menu_item.get_description()
        )
        return f"{base_desc} (Extra Spicy Level {self.spicy_level})"

    def get_price(self) -> float:
        base_price = (
            self._menu_item.base_price
            if isinstance(self._menu_item, MenuItem)
            else self._menu_item.get_price()
        )
        return base_price + (self.EXTRA_PRICE * self.spicy_level)


class GiftWrapDecorator(MenuItemDecorator):
    """Decorator untuk Gift Wrapping"""

    EXTRA_PRICE = 5000

    def get_description(self) -> str:
        base_desc = (
            self._menu_item.item_name
            if isinstance(self._menu_item, MenuItem)
            else self._menu_item.get_description()
        )
        return f"{base_desc} + Gift Wrap"

    def get_price(self) -> float:
        base_price = (
            self._menu_item.base_price
            if isinstance(self._menu_item, MenuItem)
            else self._menu_item.get_price()
        )
        return base_price + self.EXTRA_PRICE


class IceLevelDecorator(MenuItemDecorator):
    """Decorator untuk customize Ice Level (untuk minuman)"""

    def __init__(self, menu_item: MenuItem, ice_level: str = "normal"):
        """
        Args:
            ice_level: "less", "normal", "more", "no ice"
        """
        super().__init__(menu_item)
        self.ice_level = ice_level
        # No extra charge, hanya customization
        self.extra_price = 0

    def get_description(self) -> str:
        base_desc = (
            self._menu_item.item_name
            if isinstance(self._menu_item, MenuItem)
            else self._menu_item.get_description()
        )
        return f"{base_desc} ({self.ice_level.title()} Ice)"

    def get_price(self) -> float:
        base_price = (
            self._menu_item.base_price
            if isinstance(self._menu_item, MenuItem)
            else self._menu_item.get_price()
        )
        return base_price + self.extra_price


class SugarLevelDecorator(MenuItemDecorator):
    """Decorator untuk customize Sugar Level (untuk minuman)"""

    def __init__(self, menu_item: MenuItem, sugar_level: str = "normal"):
        """
        Args:
            sugar_level: "less", "normal", "more", "no sugar"
        """
        super().__init__(menu_item)
        self.sugar_level = sugar_level
        # No extra charge, hanya customization
        self.extra_price = 0

    def get_description(self) -> str:
        base_desc = (
            self._menu_item.item_name
            if isinstance(self._menu_item, MenuItem)
            else self._menu_item.get_description()
        )
        return f"{base_desc} ({self.sugar_level.title()} Sugar)"

    def get_price(self) -> float:
        base_price = (
            self._menu_item.base_price
            if isinstance(self._menu_item, MenuItem)
            else self._menu_item.get_price()
        )
        return base_price + self.extra_price


class MenuDecoratorService:
    """
    Service untuk manage menu decorations
    Demonstrasi bagaimana stack multiple decorators
    """

    @staticmethod
    def apply_decorators(
        base_item: MenuItem, decorators_config: list
    ) -> MenuItemDecorator:
        """
        Apply multiple decorators to menu item

        Args:
            base_item: Base MenuItem object
            decorators_config: List of dict dengan decorator config
                               [{'type': 'cheese'}, {'type': 'topping', 'name': 'Mushroom'}]

        Returns:
            Decorated menu item
        """
        decorated_item = base_item

        for config in decorators_config:
            decorator_type = config.get("type", "").lower()

            if decorator_type == "cheese":
                decorated_item = ExtraCheeseDecorator(decorated_item)

            elif decorator_type == "topping":
                topping_name = config.get("name", "Topping")
                topping_price = config.get("price", 7000)
                decorated_item = ExtraToppingDecorator(
                    decorated_item, topping_name, topping_price
                )

            elif decorator_type == "large":
                decorated_item = LargeSizeDecorator(decorated_item)

            elif decorator_type == "spicy":
                spicy_level = config.get("level", 1)
                decorated_item = ExtraSpicyDecorator(decorated_item, spicy_level)

            elif decorator_type == "gift":
                decorated_item = GiftWrapDecorator(decorated_item)

            elif decorator_type == "ice":
                ice_level = config.get("level", "normal")
                decorated_item = IceLevelDecorator(decorated_item, ice_level)

            elif decorator_type == "sugar":
                sugar_level = config.get("level", "normal")
                decorated_item = SugarLevelDecorator(decorated_item, sugar_level)

            else:
                print(f"[WARNING] Unknown decorator type: {decorator_type}")

        return decorated_item

    @staticmethod
    def get_price_breakdown(decorated_item: MenuItemDecorator) -> dict:
        """
        Get price breakdown dari decorated item
        Useful untuk show customer detail biaya
        """
        # Trace back to base item
        current = decorated_item
        breakdown = []

        while isinstance(current, MenuItemDecorator):
            decorator_name = current.__class__.__name__.replace("Decorator", "")
            decorator_price = current.get_price() - (
                current._menu_item.get_price()
                if isinstance(current._menu_item, MenuItemDecorator)
                else current._menu_item.base_price
            )

            if decorator_price > 0:
                breakdown.insert(0, {"name": decorator_name, "price": decorator_price})

            current = current._menu_item

        # Base item
        base_item = current
        breakdown.insert(
            0, {"name": base_item.item_name, "price": base_item.base_price}
        )

        return {"items": breakdown, "total": decorated_item.get_price()}


# Test Decorator Pattern
if __name__ == "__main__":
    print("=" * 70)
    print("TESTING DECORATOR PATTERN - Menu Customization System")
    print("=" * 70)

    from models.restaurant import FoodItem, BeverageItem

    # Test 1: Single Decorator
    print("\n" + "=" * 70)
    print("Test 1: Single Decorator")
    print("=" * 70)

    burger = FoodItem(
        item_id=1,
        customer_id=1,
        item_name="Beef Burger",
        base_price=35000,
        description="Juicy beef burger",
        category="main_course",
    )

    print(f"Base Item: {burger.item_name} - Rp {burger.base_price:,.0f}")

    burger_with_cheese = ExtraCheeseDecorator(burger)
    print(f"With Decorator: {burger_with_cheese}")

    # Test 2: Stacking Multiple Decorators
    print("\n" + "=" * 70)
    print("Test 2: Stacking Multiple Decorators")
    print("=" * 70)

    pizza = FoodItem(
        item_id=2,
        customer_id=1,
        item_name="Pepperoni Pizza",
        base_price=50000,
        description="Classic pepperoni pizza",
        category="main_course",
    )

    print(f"Base Item: {pizza.item_name} - Rp {pizza.base_price:,.0f}")

    # Stack decorators
    pizza_custom = ExtraCheeseDecorator(pizza)
    print(f"Step 1: {pizza_custom}")

    pizza_custom = ExtraToppingDecorator(pizza_custom, "Mushroom", 7000)
    print(f"Step 2: {pizza_custom}")

    pizza_custom = ExtraToppingDecorator(pizza_custom, "Beef", 10000)
    print(f"Step 3: {pizza_custom}")

    pizza_custom = LargeSizeDecorator(pizza_custom)
    print(f"Step 4 (Final): {pizza_custom}")

    # Test 3: Using Service with Config
    print("\n" + "=" * 70)
    print("Test 3: Using MenuDecoratorService")
    print("=" * 70)

    coffee = BeverageItem(
        item_id=3,
        customer_id=1,
        item_name="Kopi Susu",
        base_price=15000,
        description="Indonesian milk coffee",
        size="regular",
    )

    print(f"Base Item: {coffee.item_name} - Rp {coffee.base_price:,.0f}")

    decorators_config = [
        {"type": "large"},
        {"type": "ice", "level": "less"},
        {"type": "sugar", "level": "more"},
    ]

    coffee_custom = MenuDecoratorService.apply_decorators(coffee, decorators_config)
    print(f"\nCustomized Order: {coffee_custom}")

    # Test 4: Price Breakdown
    print("\n" + "=" * 70)
    print("Test 4: Price Breakdown")
    print("=" * 70)

    nasi_goreng = FoodItem(
        item_id=4,
        customer_id=1,
        item_name="Nasi Goreng Spesial",
        base_price=25000,
        description="Special fried rice",
        category="main_course",
    )

    custom_config = [
        {"type": "topping", "name": "Telur", "price": 5000},
        {"type": "topping", "name": "Ayam", "price": 8000},
        {"type": "spicy", "level": 2},
        {"type": "large"},
    ]

    nasi_goreng_custom = MenuDecoratorService.apply_decorators(
        nasi_goreng, custom_config
    )

    print(f"Final Order: {nasi_goreng_custom}")
    print(f"\nPrice Breakdown:")

    breakdown = MenuDecoratorService.get_price_breakdown(nasi_goreng_custom)
    for item in breakdown["items"]:
        print(f"  • {item['name']}: Rp {item['price']:,.0f}")
    print(f"  " + "-" * 40)
    print(f"  TOTAL: Rp {breakdown['total']:,.0f}")
