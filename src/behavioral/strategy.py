"""
STRATEGY PATTERN - Pricing Strategies
Algoritma perhitungan harga yang berbeda untuk berbagai kondisi
"""

from abc import ABC, abstractmethod
from datetime import datetime, time
from typing import Optional
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.restaurant import Order


class PricingStrategy(ABC):
    """
    Abstract Strategy untuk perhitungan harga

    Teori:
    - Strategy Pattern adalah behavioral pattern yang mendefinisikan family of algorithms,
      encapsulate masing-masing, dan membuat mereka interchangeable
    - Strategy memungkinkan algorithm vary independent dari clients yang menggunakannya
    - Menghindari conditional statements yang complex untuk pemilihan algorithm

    Use Case Restaurant:
    - Restaurant punya berbagai strategi diskon: Member discount, Promo discount,
      Voucher discount, Happy hour discount
    - Setiap strategy punya logic perhitungan berbeda
    - Strategy dapat di-switch saat runtime berdasarkan customer type atau waktu
    - Context (Order) dapat menggunakan strategy apapun tanpa tahu implementasi detailnya
    """

    @abstractmethod
    def calculate_discount(self, original_amount: float, **kwargs) -> float:
        """
        Calculate discount amount

        Args:
            original_amount: Total harga sebelum diskon
            **kwargs: Additional parameters untuk strategy

        Returns:
            Discount amount (positive number)
        """
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        """Get nama strategy untuk display"""
        pass

    def calculate_final_price(self, original_amount: float, **kwargs) -> float:
        """Calculate final price after discount"""
        discount = self.calculate_discount(original_amount, **kwargs)
        return max(0, original_amount - discount)


class NoDiscountStrategy(PricingStrategy):
    """Strategy tanpa diskon (regular price)"""

    def calculate_discount(self, original_amount: float, **kwargs) -> float:
        return 0

    def get_strategy_name(self) -> str:
        return "Regular Price (No Discount)"


class MemberDiscountStrategy(PricingStrategy):
    """
    Strategy untuk member discount
    Diskon berdasarkan member tier: Silver, Gold, Platinum
    """

    DISCOUNT_RATES = {
        "silver": 0.05,  # 5%
        "gold": 0.10,  # 10%
        "platinum": 0.15,  # 15%
    }

    def calculate_discount(self, original_amount: float, **kwargs) -> float:
        member_tier = kwargs.get("member_tier", "silver").lower()
        discount_rate = self.DISCOUNT_RATES.get(member_tier, 0)

        discount = original_amount * discount_rate
        print(
            f"[MEMBER DISCOUNT] Tier: {member_tier.upper()} | Rate: {discount_rate*100}% | Discount: Rp {discount:,.0f}"
        )

        return discount

    def get_strategy_name(self) -> str:
        return "Member Discount"


class PromoDiscountStrategy(PricingStrategy):
    """
    Strategy untuk promo discount
    Diskon flat amount jika minimum purchase terpenuhi
    Contoh: Diskon 20rb untuk belanja min 100rb
    """

    def __init__(
        self, discount_amount: float = 20000, minimum_purchase: float = 100000
    ):
        self.discount_amount = discount_amount
        self.minimum_purchase = minimum_purchase

    def calculate_discount(self, original_amount: float, **kwargs) -> float:
        if original_amount >= self.minimum_purchase:
            print(
                f"[PROMO DISCOUNT] Min Purchase: Rp {self.minimum_purchase:,.0f} | Discount: Rp {self.discount_amount:,.0f}"
            )
            return self.discount_amount
        else:
            print(
                f"[PROMO DISCOUNT] Min Purchase: Rp {self.minimum_purchase:,.0f} | Need: Rp {self.minimum_purchase - original_amount:,.0f} more"
            )
            return 0

    def get_strategy_name(self) -> str:
        return f"Promo Discount (Rp {self.discount_amount:,.0f} off for min Rp {self.minimum_purchase:,.0f})"


class VoucherDiscountStrategy(PricingStrategy):
    """
    Strategy untuk voucher discount
    Diskon percentage dengan maximum discount amount
    Contoh: Diskon 20% maksimal 50rb
    """

    def __init__(self, discount_percentage: float = 0.20, max_discount: float = 50000):
        self.discount_percentage = discount_percentage
        self.max_discount = max_discount

    def calculate_discount(self, original_amount: float, **kwargs) -> float:
        calculated_discount = original_amount * self.discount_percentage
        actual_discount = min(calculated_discount, self.max_discount)

        print(
            f"[VOUCHER DISCOUNT] Rate: {self.discount_percentage*100}% | Calculated: Rp {calculated_discount:,.0f} | Actual: Rp {actual_discount:,.0f}"
        )

        return actual_discount

    def get_strategy_name(self) -> str:
        return f"Voucher Discount ({self.discount_percentage*100}% off, max Rp {self.max_discount:,.0f})"


class HappyHourStrategy(PricingStrategy):
    """
    Strategy untuk happy hour discount
    Diskon percentage pada jam-jam tertentu
    Contoh: Diskon 25% antara jam 14:00 - 16:00
    """

    def __init__(
        self,
        discount_percentage: float = 0.25,
        start_hour: int = 14,
        end_hour: int = 16,
    ):
        self.discount_percentage = discount_percentage
        self.start_time = time(start_hour, 0)
        self.end_time = time(end_hour, 0)

    def calculate_discount(self, original_amount: float, **kwargs) -> float:
        current_time = kwargs.get("order_time", datetime.now().time())

        if self.start_time <= current_time <= self.end_time:
            discount = original_amount * self.discount_percentage
            print(
                f"[HAPPY HOUR] Time: {current_time.strftime('%H:%M')} | Rate: {self.discount_percentage*100}% | Discount: Rp {discount:,.0f}"
            )
            return discount
        else:
            print(
                f"[HAPPY HOUR] Time: {current_time.strftime('%H:%M')} | Happy Hour: {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
            )
            return 0

    def get_strategy_name(self) -> str:
        return f"Happy Hour ({self.discount_percentage*100}% off, {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"


class BirthdayDiscountStrategy(PricingStrategy):
    """
    Strategy untuk birthday discount
    Diskon special untuk customer yang ulang tahun
    """

    def __init__(self, discount_percentage: float = 0.30):
        self.discount_percentage = discount_percentage

    def calculate_discount(self, original_amount: float, **kwargs) -> float:
        is_birthday = kwargs.get("is_birthday", False)

        if is_birthday:
            discount = original_amount * self.discount_percentage
            print(
                f"[BIRTHDAY DISCOUNT] Happy Birthday! | Rate: {self.discount_percentage*100}% | Discount: Rp {discount:,.0f}"
            )
            return discount
        else:
            print(f"[BIRTHDAY DISCOUNT] Not customer's birthday")
            return 0

    def get_strategy_name(self) -> str:
        return f"Birthday Special ({self.discount_percentage*100}% off)"


class PricingContext:
    """
    Context class untuk menggunakan pricing strategy
    Memungkinkan switch strategy at runtime
    """

    def __init__(self, strategy: Optional[PricingStrategy] = None):
        self._strategy = strategy or NoDiscountStrategy()

    def set_strategy(self, strategy: PricingStrategy):
        """Change pricing strategy"""
        self._strategy = strategy
        print(f"[CONTEXT] Strategy changed to: {strategy.get_strategy_name()}")

    def get_strategy(self) -> PricingStrategy:
        """Get current strategy"""
        return self._strategy

    def calculate_price(self, original_amount: float, **kwargs) -> dict:
        """
        Calculate final price using current strategy

        Returns:
            Dict with original_amount, discount, final_amount, strategy_name
        """
        discount = self._strategy.calculate_discount(original_amount, **kwargs)
        final_amount = max(0, original_amount - discount)

        return {
            "original_amount": original_amount,
            "discount": discount,
            "final_amount": final_amount,
            "strategy_name": self._strategy.get_strategy_name(),
        }


class OrderPricingService:
    """
    Service untuk apply pricing strategy ke Order
    Integration dengan database dan Order model
    """

    def __init__(self):
        from creational.singleton import DatabaseConnection

        self.db = DatabaseConnection()

    def apply_strategy_to_order(
        self, order: Order, strategy: PricingStrategy, **kwargs
    ) -> dict:
        """
        Apply pricing strategy to an order

        Args:
            order: Order object
            strategy: PricingStrategy to apply
            **kwargs: Additional parameters for strategy

        Returns:
            Pricing result dict
        """
        context = PricingContext(strategy)
        result = context.calculate_price(order.total_amount, **kwargs)

        # Update order dengan discount info
        order.discount_amount = result["discount"]
        order.final_amount = result["final_amount"]

        return result

    def get_best_strategy(
        self, original_amount: float, customer_data: dict
    ) -> PricingStrategy:
        """
        Determine best strategy for customer
        Try multiple strategies and return yang kasih diskon terbesar

        Args:
            original_amount: Total amount before discount
            customer_data: Dict with customer info (member_tier, is_birthday, etc)

        Returns:
            Best PricingStrategy
        """
        strategies = [
            NoDiscountStrategy(),
            MemberDiscountStrategy(),
            PromoDiscountStrategy(),
            VoucherDiscountStrategy(),
            HappyHourStrategy(),
            BirthdayDiscountStrategy(),
        ]

        best_strategy = strategies[0]
        best_discount = 0

        print("\n[BEST STRATEGY] Evaluating all strategies...")
        print("=" * 60)

        for strategy in strategies:
            discount = strategy.calculate_discount(original_amount, **customer_data)
            print(f"  {strategy.get_strategy_name()}: Rp {discount:,.0f}")

            if discount > best_discount:
                best_discount = discount
                best_strategy = strategy

        print("=" * 60)
        print(f"[BEST STRATEGY] Selected: {best_strategy.get_strategy_name()}")
        print(f"[BEST STRATEGY] Discount: Rp {best_discount:,.0f}")

        return best_strategy


# Test Strategy Pattern
if __name__ == "__main__":
    print("=" * 70)
    print("TESTING STRATEGY PATTERN - Pricing System")
    print("=" * 70)

    original_amount = 150000

    # Test 1: No Discount
    print("\n" + "=" * 70)
    print("Test 1: No Discount Strategy")
    print("=" * 70)

    context = PricingContext(NoDiscountStrategy())
    result = context.calculate_price(original_amount)
    print(f"Original: Rp {result['original_amount']:,.0f}")
    print(f"Discount: Rp {result['discount']:,.0f}")
    print(f"Final: Rp {result['final_amount']:,.0f}")

    # Test 2: Member Discount
    print("\n" + "=" * 70)
    print("Test 2: Member Discount Strategy")
    print("=" * 70)

    context.set_strategy(MemberDiscountStrategy())
    result = context.calculate_price(original_amount, member_tier="gold")
    print(f"Original: Rp {result['original_amount']:,.0f}")
    print(f"Discount: Rp {result['discount']:,.0f}")
    print(f"Final: Rp {result['final_amount']:,.0f}")

    # Test 3: Promo Discount
    print("\n" + "=" * 70)
    print("Test 3: Promo Discount Strategy")
    print("=" * 70)

    context.set_strategy(
        PromoDiscountStrategy(discount_amount=25000, minimum_purchase=100000)
    )
    result = context.calculate_price(original_amount)
    print(f"Original: Rp {result['original_amount']:,.0f}")
    print(f"Discount: Rp {result['discount']:,.0f}")
    print(f"Final: Rp {result['final_amount']:,.0f}")

    # Test 4: Voucher Discount
    print("\n" + "=" * 70)
    print("Test 4: Voucher Discount Strategy")
    print("=" * 70)

    context.set_strategy(
        VoucherDiscountStrategy(discount_percentage=0.20, max_discount=50000)
    )
    result = context.calculate_price(original_amount)
    print(f"Original: Rp {result['original_amount']:,.0f}")
    print(f"Discount: Rp {result['discount']:,.0f}")
    print(f"Final: Rp {result['final_amount']:,.0f}")

    # Test 5: Happy Hour
    print("\n" + "=" * 70)
    print("Test 5: Happy Hour Strategy")
    print("=" * 70)

    context.set_strategy(
        HappyHourStrategy(discount_percentage=0.25, start_hour=14, end_hour=16)
    )

    # Test during happy hour
    result = context.calculate_price(original_amount, order_time=time(15, 30))
    print(f"Original: Rp {result['original_amount']:,.0f}")
    print(f"Discount: Rp {result['discount']:,.0f}")
    print(f"Final: Rp {result['final_amount']:,.0f}")

    # Test outside happy hour
    print("\nOutside Happy Hour:")
    result = context.calculate_price(original_amount, order_time=time(18, 0))
    print(f"Original: Rp {result['original_amount']:,.0f}")
    print(f"Discount: Rp {result['discount']:,.0f}")
    print(f"Final: Rp {result['final_amount']:,.0f}")

    # Test 6: Birthday Discount
    print("\n" + "=" * 70)
    print("Test 6: Birthday Discount Strategy")
    print("=" * 70)

    context.set_strategy(BirthdayDiscountStrategy(discount_percentage=0.30))
    result = context.calculate_price(original_amount, is_birthday=True)
    print(f"Original: Rp {result['original_amount']:,.0f}")
    print(f"Discount: Rp {result['discount']:,.0f}")
    print(f"Final: Rp {result['final_amount']:,.0f}")

    # Test 7: Best Strategy Selection
    print("\n" + "=" * 70)
    print("Test 7: Automatic Best Strategy Selection")
    print("=" * 70)

    service = OrderPricingService()
    customer_data = {
        "member_tier": "platinum",
        "is_birthday": True,
        "order_time": time(15, 0),
    }

    best_strategy = service.get_best_strategy(original_amount, customer_data)
    result = context.calculate_price(original_amount, **customer_data)

    print(f"\nFinal Result:")
    print(f"Original: Rp {result['original_amount']:,.0f}")
    print(f"Discount: Rp {result['discount']:,.0f}")
    print(f"Final: Rp {result['final_amount']:,.0f}")
    print(f"Savings: {(result['discount']/result['original_amount']*100):.1f}%")
