"""
FACTORY PATTERN - Menu Item Creator
Menyediakan interface untuk membuat berbagai jenis menu tanpa specify concrete class
"""

from abc import ABC, abstractmethod
from typing import Optional
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.restaurant import MenuItem, FoodItem, BeverageItem, PackageItem
from creational.singleton import DatabaseConnection


class MenuItemFactory(ABC):
    """
    Abstract Factory Pattern untuk membuat menu items

    Teori:
    - Factory Pattern adalah creational pattern yang menyediakan interface
      untuk membuat objects tanpa specify exact class
    - Mengurangi coupling antara code dan concrete classes
    - Memudahkan penambahan type baru tanpa modify existing code

    Use Case Restaurant:
    - Restoran punya berbagai jenis menu: Makanan, Minuman, Paket
    - Setiap jenis punya behavior berbeda (size untuk beverage, ingredients untuk food)
    - Factory membuat proses pembuatan menu consistent dan maintainable
    """

    @abstractmethod
    def create_menu_item(
        self,
        customer_id: int,
        item_name: str,
        base_price: float,
        description: str = "",
        item_id: Optional[int] = None,
    ) -> MenuItem:
        """Abstract method untuk create menu item"""
        pass


class FoodItemFactory(MenuItemFactory):
    """Factory untuk membuat Menu Makanan"""

    def create_menu_item(
        self,
        customer_id: int,
        item_name: str,
        base_price: float,
        description: str = "",
        item_id: Optional[int] = None,
        category: str = "main_course",
    ) -> FoodItem:
        print(f"[FACTORY] Creating Food Item: {item_name} - Rp{base_price:,.0f}")
        return FoodItem(
            item_id, customer_id, item_name, base_price, description, category
        )


class BeverageItemFactory(MenuItemFactory):
    """Factory untuk membuat Menu Minuman"""

    def create_menu_item(
        self,
        customer_id: int,
        item_name: str,
        base_price: float,
        description: str = "",
        item_id: Optional[int] = None,
        size: str = "regular",
    ) -> BeverageItem:
        print(
            f"[FACTORY] Creating Beverage Item: {item_name} ({size}) - Rp{base_price:,.0f}"
        )
        return BeverageItem(
            item_id, customer_id, item_name, base_price, description, size
        )


class PackageItemFactory(MenuItemFactory):
    """Factory untuk membuat Menu Paket"""

    def create_menu_item(
        self,
        customer_id: int,
        item_name: str,
        base_price: float,
        description: str = "",
        item_id: Optional[int] = None,
        items_included: list = None,
    ) -> PackageItem:
        print(f"[FACTORY] Creating Package Item: {item_name} - Rp{base_price:,.0f}")
        return PackageItem(
            item_id, customer_id, item_name, base_price, description, items_included
        )


class MenuItemFactoryProvider:
    """
    Provider untuk mendapatkan factory yang sesuai berdasarkan menu type
    Implementasi Simple Factory Pattern
    """

    _factories = {
        "food": FoodItemFactory(),
        "beverage": BeverageItemFactory(),
        "package": PackageItemFactory(),
    }

    @classmethod
    def get_factory(cls, item_type: str) -> MenuItemFactory:
        """Get factory berdasarkan item type"""
        factory = cls._factories.get(item_type.lower())
        if not factory:
            raise ValueError(
                f"Unknown menu type: {item_type}. Available: food, beverage, package"
            )
        return factory

    @classmethod
    def get_available_types(cls):
        """Get list of available menu types"""
        return list(cls._factories.keys())


class MenuService:
    """
    Service layer untuk manage menu operations
    Menggunakan Factory Pattern untuk create menu items
    Menggunakan Singleton Pattern untuk database access
    """

    def __init__(self):
        self.db = DatabaseConnection()

    def create_menu_item(
        self,
        customer_id: int,
        item_type: str,
        item_name: str,
        base_price: float,
        description: str = "",
        **kwargs,
    ) -> MenuItem:
        """
        Create new menu item dan save ke database

        Args:
            customer_id: ID customer yang membuat menu (chef/owner)
            item_type: Type menu (food, beverage, package)
            item_name: Nama menu item
            base_price: Harga dasar
            description: Deskripsi menu
            **kwargs: Additional parameters (category, size, items_included)

        Returns:
            Created MenuItem object
        """
        # Get appropriate factory
        factory = MenuItemFactoryProvider.get_factory(item_type)

        # Create menu object (belum ada ID)
        menu_item = factory.create_menu_item(
            customer_id, item_name, base_price, description, **kwargs
        )

        # Save to database
        query = """
            INSERT INTO menu_items (customer_id, item_name, item_type, base_price, description)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING item_id
        """
        result = self.db.execute_query(
            query,
            (customer_id, item_name, item_type, base_price, description),
            fetch=True,
        )

        # Set item_id dari database
        menu_item.item_id = result[0][0]
        print(f"[SERVICE] Menu item saved to database with ID: {menu_item.item_id}")

        return menu_item

    def get_menu_item(self, item_id: int) -> Optional[MenuItem]:
        """Get menu item by ID dari database"""
        query = "SELECT * FROM menu_items WHERE item_id = %s"
        results = self.db.execute_query_dict(query, (item_id,))

        if not results:
            return None

        row = results[0]
        factory = MenuItemFactoryProvider.get_factory(row["item_type"])

        return factory.create_menu_item(
            customer_id=row["customer_id"],
            item_name=row["item_name"],
            base_price=float(row["base_price"]),
            description=row["description"] or "",
            item_id=row["item_id"],
        )

    def get_menu_by_type(self, item_type: str):
        """Get all menu items by type"""
        query = """
            SELECT * FROM menu_items 
            WHERE item_type = %s 
            ORDER BY item_name
        """
        results = self.db.execute_query_dict(query, (item_type,))

        menu_items = []
        for row in results:
            factory = MenuItemFactoryProvider.get_factory(row["item_type"])
            item = factory.create_menu_item(
                customer_id=row["customer_id"],
                item_name=row["item_name"],
                base_price=float(row["base_price"]),
                description=row["description"] or "",
                item_id=row["item_id"],
            )
            menu_items.append(item)

        return menu_items

    def get_all_menu(self):
        """Get all menu items"""
        query = "SELECT * FROM menu_items ORDER BY item_type, item_name"
        return self.db.execute_query_dict(query)

    def update_menu_item(
        self,
        item_id: int,
        item_name: str = None,
        base_price: float = None,
        description: str = None,
    ) -> bool:
        """Update menu item"""
        updates = []
        params = []

        if item_name:
            updates.append("item_name = %s")
            params.append(item_name)

        if base_price is not None:
            updates.append("base_price = %s")
            params.append(base_price)

        if description is not None:
            updates.append("description = %s")
            params.append(description)

        if not updates:
            return False

        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(item_id)

        query = f"UPDATE menu_items SET {', '.join(updates)} WHERE item_id = %s"
        self.db.execute_query(query, tuple(params), fetch=False)

        print(f"[SERVICE] Menu item {item_id} updated successfully")
        return True

    def delete_menu_item(self, item_id: int) -> bool:
        """Delete menu item"""
        query = "DELETE FROM menu_items WHERE item_id = %s"
        self.db.execute_query(query, (item_id,), fetch=False)
        print(f"[SERVICE] Menu item {item_id} deleted successfully")
        return True


# Test Factory Pattern
if __name__ == "__main__":
    print("=" * 70)
    print("TESTING FACTORY PATTERN - Restaurant Menu System")
    print("=" * 70)

    service = MenuService()

    print("\nAvailable menu types:", MenuItemFactoryProvider.get_available_types())

    # Test create menu items
    print("\n" + "=" * 70)
    print("Creating menu items with different factories...")
    print("=" * 70)

    try:
        # Food Item
        food = service.create_menu_item(
            customer_id=1,
            item_type="food",
            item_name="Rendang Sapi Spesial",
            base_price=45000,
            description="Rendang daging sapi dengan bumbu rempah pilihan",
            category="main_course",
        )
        print(f"✓ Created: {food}")

        # Beverage Item
        beverage = service.create_menu_item(
            customer_id=1,
            item_type="beverage",
            item_name="Kopi Susu Gula Aren",
            base_price=20000,
            description="Kopi susu dengan gula aren original",
            size="regular",
        )
        print(f"✓ Created: {beverage}")

        # Package Item
        package = service.create_menu_item(
            customer_id=1,
            item_type="package",
            item_name="Paket Nasi Goreng Komplit",
            base_price=50000,
            description="Nasi Goreng + Ayam Goreng + Es Teh + Kerupuk",
            items_included=["Nasi Goreng", "Ayam Goreng", "Es Teh", "Kerupuk"],
        )
        print(f"✓ Created: {package}")

        # Get menu by type
        print("\n" + "=" * 70)
        print("Menu Makanan (Food):")
        print("=" * 70)
        foods = service.get_menu_by_type("food")
        for item in foods[:5]:
            print(f"  • {item.item_name} - Rp{item.base_price:,.0f}")

        print("\n" + "=" * 70)
        print("Menu Minuman (Beverage):")
        print("=" * 70)
        beverages = service.get_menu_by_type("beverage")
        for item in beverages[:5]:
            print(f"  • {item.item_name} - Rp{item.base_price:,.0f}")

    except Exception as e:
        print(f"Error: {e}")
        print("Make sure database is setup correctly (database/schema.sql)")
