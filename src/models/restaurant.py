"""
Data Models untuk Restaurant Management System
"""

from datetime import datetime
from typing import Optional, List


class Customer:
    """Model untuk Customer/Pelanggan"""

    def __init__(
        self,
        customer_id: int,
        name: str,
        phone: str,
        email: str = None,
        is_member: bool = False,
        created_at: Optional[datetime] = None,
    ):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
        self.email = email
        self.is_member = is_member
        self.created_at = created_at or datetime.now()

    def __repr__(self):
        member_status = "Member" if self.is_member else "Regular"
        return f"Customer(id={self.customer_id}, name='{self.name}', status={member_status})"


class MenuItem:
    """Base Model untuk Menu Item"""

    def __init__(
        self,
        item_id: Optional[int],
        customer_id: int,
        item_name: str,
        item_type: str,
        base_price: float,
        description: str = "",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.item_id = item_id
        self.customer_id = customer_id
        self.item_name = item_name
        self.item_type = item_type  # food, beverage, package
        self.base_price = base_price
        self.description = description
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "item_id": self.item_id,
            "customer_id": self.customer_id,
            "item_name": self.item_name,
            "item_type": self.item_type,
            "base_price": self.base_price,
            "description": self.description,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }

    def get_price(self):
        """Get final price (bisa di-override oleh subclass)"""
        return self.base_price

    def __repr__(self):
        return f"MenuItem(id={self.item_id}, name='{self.item_name}', type='{self.item_type}', price=Rp{self.base_price:,.0f})"


class FoodItem(MenuItem):
    """Menu Makanan"""

    def __init__(
        self,
        item_id: Optional[int],
        customer_id: int,
        item_name: str,
        base_price: float,
        description: str = "",
        category: str = "main_course",
        **kwargs,
    ):
        super().__init__(
            item_id, customer_id, item_name, "food", base_price, description, **kwargs
        )
        self.category = category  # appetizer, main_course, dessert

    def get_ingredients(self):
        """Get ingredients dari description"""
        if not self.description:
            return []
        return [ing.strip() for ing in self.description.split(",")]


class BeverageItem(MenuItem):
    """Menu Minuman"""

    def __init__(
        self,
        item_id: Optional[int],
        customer_id: int,
        item_name: str,
        base_price: float,
        description: str = "",
        size: str = "regular",
        **kwargs,
    ):
        super().__init__(
            item_id,
            customer_id,
            item_name,
            "beverage",
            base_price,
            description,
            **kwargs,
        )
        self.size = size  # small, regular, large

    def get_size_multiplier(self):
        """Get price multiplier based on size"""
        multipliers = {"small": 0.8, "regular": 1.0, "large": 1.3}
        return multipliers.get(self.size, 1.0)

    def get_price(self):
        """Override untuk apply size multiplier"""
        return self.base_price * self.get_size_multiplier()


class PackageItem(MenuItem):
    """Menu Paket (combo)"""

    def __init__(
        self,
        item_id: Optional[int],
        customer_id: int,
        item_name: str,
        base_price: float,
        description: str = "",
        items_included: List[str] = None,
        **kwargs,
    ):
        super().__init__(
            item_id,
            customer_id,
            item_name,
            "package",
            base_price,
            description,
            **kwargs,
        )
        self.items_included = items_included or []

    def get_package_items(self):
        """Get items yang termasuk dalam paket"""
        if self.items_included:
            return self.items_included
        if self.description:
            return [item.strip() for item in self.description.split("+")]
        return []


class Order:
    """Model untuk Order/Pesanan"""

    def __init__(
        self,
        order_id: Optional[int] = None,
        customer_id: int = None,
        table_number: int = None,
        items: List[dict] = None,
        total_price: float = None,
        total_amount: float = None,
        status: str = "pending",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.order_id = order_id
        self.customer_id = customer_id
        self.table_number = table_number or 0
        self.items = items or []
        # Support both total_price and total_amount
        self.total_amount = total_amount or total_price or 0
        self.total_price = self.total_amount  # Alias
        self.status = status  # pending, cooking, served, paid, cancelled
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        # Additional fields for observer pattern
        self.discount_amount = 0
        self.final_amount = self.total_amount

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "table_number": self.table_number,
            "items": self.items,
            "total_price": self.total_price,
            "status": self.status,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }

    def __repr__(self):
        return f"Order(id={self.order_id}, table={self.table_number}, total=Rp{self.total_price:,.0f}, status='{self.status}')"


class OrderReport:
    """Model untuk Order Report/Laporan"""

    def __init__(
        self,
        order_id: int,
        customer_name: str,
        total_items: int,
        total_amount: float,
        report_id: Optional[int] = None,
        report_type: str = "",
        report_path: str = "",
        created_at: Optional[datetime] = None,
    ):
        self.report_id = report_id
        self.order_id = order_id
        self.customer_name = customer_name
        self.total_items = total_items
        self.total_amount = total_amount
        self.report_type = report_type  # pdf, excel, json
        self.report_path = report_path
        self.created_at = created_at or datetime.now()
        self.items_details = []  # Will be populated with order items

    def __repr__(self):
        return f"Report(id={self.report_id}, type='{self.report_type}', path='{self.report_path}')"
