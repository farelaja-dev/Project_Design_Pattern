"""
OBSERVER PATTERN - Order Notification System
Notifikasi otomatis ke berbagai pihak ketika order berubah
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.restaurant import Order


class Observer(ABC):
    """
    Abstract Observer

    Teori:
    - Observer Pattern adalah behavioral pattern yang mendefinisikan one-to-many dependency
      antara objects, sehingga ketika satu object berubah state, semua dependents
      di-notify dan di-update otomatis
    - Implementasi publish-subscribe pattern
    - Loose coupling antara subject dan observers

    Use Case Restaurant:
    - Ketika order dibuat/diupdate, berbagai pihak perlu di-notify:
      * Kitchen - untuk mulai masak
      * Cashier - untuk prepare payment
      * Waiter - untuk deliver ke table
      * SMS Service - untuk notifikasi customer
      * Audit Log - untuk record keeping
    - Observer pattern memungkinkan add/remove observers tanpa modify subject
    """

    @abstractmethod
    def update(self, order: Order, event_type: str, message: str):
        """
        Called when order state changes

        Args:
            order: Order object yang berubah
            event_type: Type of event (created, updated, completed, cancelled)
            message: Additional message
        """
        pass

    @abstractmethod
    def get_observer_name(self) -> str:
        """Get nama observer untuk display"""
        pass


class KitchenDisplayObserver(Observer):
    """
    Observer untuk Kitchen Display System
    Notify kitchen staff tentang order baru
    """

    def update(self, order: Order, event_type: str, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")

        if event_type == "created":
            print(f"[KITCHEN - {timestamp}] NEW ORDER #{order.order_id}")
            print(f"   Customer: {order.customer_id}")
            print(f"   Items: {len(order.items) if hasattr(order, 'items') else 'N/A'}")
            print(f"   Priority: {'HIGH' if order.total_amount > 100000 else 'NORMAL'}")
            print(f"   Message: {message}")

        elif event_type == "cancelled":
            print(f"[KITCHEN - {timestamp}] ORDER CANCELLED #{order.order_id}")
            print(f"   Stop preparation!")

    def get_observer_name(self) -> str:
        return "Kitchen Display System"


class CashierNotificationObserver(Observer):
    """
    Observer untuk Cashier System
    Notify cashier tentang pembayaran yang perlu diproses
    """

    def update(self, order: Order, event_type: str, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")

        if event_type == "created":
            print(f"[CASHIER - {timestamp}] Payment Ready #{order.order_id}")
            print(f"   Amount: Rp {order.total_amount:,.0f}")
            print(f"   Payment Method: {getattr(order, 'payment_method', 'Cash')}")

        elif event_type == "completed":
            print(f"[CASHIER - {timestamp}] Payment Completed #{order.order_id}")
            print(f"   Transaction Successful")

    def get_observer_name(self) -> str:
        return "Cashier Notification System"


class WaiterAlertObserver(Observer):
    """
    Observer untuk Waiter Alert System
    Notify waiter tentang order yang ready untuk deliver
    """

    def update(self, order: Order, event_type: str, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")

        if event_type == "created":
            print(f"[WAITER - {timestamp}] New Order Received #{order.order_id}")
            print(f"   Table: {getattr(order, 'table_number', 'Takeaway')}")
            print(f"   Message: {message}")

        elif event_type == "ready":
            print(f"[WAITER - {timestamp}] Order Ready for Delivery #{order.order_id}")
            print(f"   Please deliver to table!")

        elif event_type == "completed":
            print(f"[WAITER - {timestamp}] Order Completed #{order.order_id}")
            print(f"   Thank you for serving!")

    def get_observer_name(self) -> str:
        return "Waiter Alert System"


class SMSNotificationObserver(Observer):
    """
    Observer untuk SMS Notification Service
    Send SMS ke customer tentang order status
    """

    def update(self, order: Order, event_type: str, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        customer_phone = getattr(order, "customer_phone", "08xx-xxxx-xxxx")

        if event_type == "created":
            sms_message = f"Order #{order.order_id} received. Total: Rp {order.total_amount:,.0f}. Estimated time: 20 mins."
            print(f"[SMS - {timestamp}] Sending to {customer_phone}")
            print(f"   Message: {sms_message}")

        elif event_type == "ready":
            sms_message = f"Your order #{order.order_id} is ready! Please pick up or it will be delivered soon."
            print(f"[SMS - {timestamp}] Sending to {customer_phone}")
            print(f"   Message: {sms_message}")

        elif event_type == "completed":
            sms_message = f"Thank you for your order #{order.order_id}! We hope you enjoyed your meal. Rate us!"
            print(f"[SMS - {timestamp}] Sending to {customer_phone}")
            print(f"   Message: {sms_message}")

    def get_observer_name(self) -> str:
        return "SMS Notification Service"


class EmailNotificationObserver(Observer):
    """
    Observer untuk Email Notification Service
    Send receipt dan notification via email
    """

    def update(self, order: Order, event_type: str, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        customer_email = getattr(order, "customer_email", "customer@example.com")

        if event_type == "created":
            print(f"[EMAIL - {timestamp}] Sending receipt to {customer_email}")
            print(f"   Subject: Order Confirmation #{order.order_id}")
            print(f"   Order details and receipt attached")

        elif event_type == "completed":
            print(f"[EMAIL - {timestamp}] Sending to {customer_email}")
            print(f"   Subject: Thank You for Your Order #{order.order_id}")
            print(f"   Feedback form link included")

    def get_observer_name(self) -> str:
        return "Email Notification Service"


class AuditLogObserver(Observer):
    """
    Observer untuk Audit Log System
    Record semua order events untuk compliance dan analysis
    """

    def __init__(self, log_file: str = "logs/order_audit.log"):
        self.log_file = log_file
        # Create logs directory if not exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

    def update(self, order: Order, event_type: str, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_entry = f"[{timestamp}] ORDER_ID={order.order_id} | EVENT={event_type.upper()} | AMOUNT=Rp{order.total_amount:,.0f} | MESSAGE={message}\n"

        # Write to log file
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
            print(
                f"[AUDIT LOG] Logged: {event_type.upper()} for Order #{order.order_id}"
            )
        except Exception as e:
            print(f"[AUDIT LOG] Error writing log: {e}")

    def get_observer_name(self) -> str:
        return "Audit Log System"


class InventoryObserver(Observer):
    """
    Observer untuk Inventory Management
    Update inventory ketika order dibuat
    """

    def update(self, order: Order, event_type: str, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")

        if event_type == "created":
            print(f"[INVENTORY - {timestamp}] Stock Check for Order #{order.order_id}")
            print(f"   Checking availability...")
            print(f"   Updating stock levels...")

        elif event_type == "cancelled":
            print(
                f"[INVENTORY - {timestamp}] Restoring Stock for Order #{order.order_id}"
            )
            print(f"   Items returned to inventory")

    def get_observer_name(self) -> str:
        return "Inventory Management System"


class OrderSubject:
    """
    Subject (Observable) yang di-observe oleh observers
    Manages list of observers dan notify mereka ketika state changes
    """

    def __init__(self):
        self._observers: List[Observer] = []
        self._order_history: List[Dict[str, Any]] = []

    def attach(self, observer: Observer):
        """Add observer to list"""
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"[SUBJECT] Observer attached: {observer.get_observer_name()}")

    def detach(self, observer: Observer):
        """Remove observer from list"""
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"[SUBJECT] Observer detached: {observer.get_observer_name()}")

    def notify(self, order: Order, event_type: str, message: str = ""):
        """Notify all observers about order changes"""
        print(f"\n{'='*70}")
        print(
            f"[SUBJECT] Notifying {len(self._observers)} observers about: {event_type.upper()}"
        )
        print(f"{'='*70}")

        for observer in self._observers:
            observer.update(order, event_type, message)

        # Record in history
        self._order_history.append(
            {
                "timestamp": datetime.now(),
                "order_id": order.order_id,
                "event_type": event_type,
                "message": message,
                "observers_notified": len(self._observers),
            }
        )

    def get_observers(self) -> List[Observer]:
        """Get list of attached observers"""
        return self._observers.copy()

    def get_history(self) -> List[Dict[str, Any]]:
        """Get notification history"""
        return self._order_history.copy()


class OrderNotificationService:
    """
    Service untuk manage order notifications
    Integrates Observer Pattern dengan Order operations
    """

    def __init__(self):
        self.subject = OrderSubject()
        self._setup_default_observers()

    def _setup_default_observers(self):
        """Setup default observers untuk restaurant operations"""
        self.subject.attach(KitchenDisplayObserver())
        self.subject.attach(CashierNotificationObserver())
        self.subject.attach(WaiterAlertObserver())
        self.subject.attach(SMSNotificationObserver())
        self.subject.attach(EmailNotificationObserver())
        self.subject.attach(AuditLogObserver())
        self.subject.attach(InventoryObserver())

    def create_order_notification(
        self, order: Order, message: str = "New order received"
    ):
        """Notify observers tentang order baru"""
        self.subject.notify(order, "created", message)

    def update_order_notification(self, order: Order, message: str = "Order updated"):
        """Notify observers tentang order update"""
        self.subject.notify(order, "updated", message)

    def ready_order_notification(
        self, order: Order, message: str = "Order ready for delivery"
    ):
        """Notify observers bahwa order sudah siap"""
        self.subject.notify(order, "ready", message)

    def complete_order_notification(
        self, order: Order, message: str = "Order completed"
    ):
        """Notify observers tentang order completion"""
        self.subject.notify(order, "completed", message)

    def cancel_order_notification(self, order: Order, message: str = "Order cancelled"):
        """Notify observers tentang order cancellation"""
        self.subject.notify(order, "cancelled", message)

    def add_custom_observer(self, observer: Observer):
        """Add custom observer"""
        self.subject.attach(observer)

    def remove_observer(self, observer: Observer):
        """Remove observer"""
        self.subject.detach(observer)

    def get_notification_history(self):
        """Get history of all notifications"""
        return self.subject.get_history()


# Test Observer Pattern
if __name__ == "__main__":
    print("=" * 70)
    print("TESTING OBSERVER PATTERN - Order Notification System")
    print("=" * 70)

    # Create notification service
    service = OrderNotificationService()

    # Create sample order
    order = Order(order_id=123, customer_id=1, total_amount=150000)
    order.customer_phone = "0812-3456-7890"
    order.customer_email = "customer@example.com"
    order.table_number = "A5"
    order.payment_method = "Credit Card"
    order.items = [1, 2, 3]  # Simulated items

    # Test 1: Order Created
    print("\n" + "=" * 70)
    print("Test 1: Order Created Event")
    print("=" * 70)

    service.create_order_notification(
        order, "Customer ordered Nasi Goreng Spesial Package"
    )

    # Test 2: Order Ready
    print("\n" + "=" * 70)
    print("Test 2: Order Ready Event")
    print("=" * 70)

    import time

    time.sleep(1)
    service.ready_order_notification(order, "Kitchen finished preparing order")

    # Test 3: Order Completed
    print("\n" + "=" * 70)
    print("Test 3: Order Completed Event")
    print("=" * 70)

    time.sleep(1)
    service.complete_order_notification(order, "Customer received order and paid")

    # Test 4: Order Cancelled (new order)
    print("\n" + "=" * 70)
    print("Test 4: Order Cancelled Event")
    print("=" * 70)

    order2 = Order(order_id=124, customer_id=2, total_amount=75000)
    time.sleep(1)
    service.create_order_notification(order2, "New order created")

    time.sleep(1)
    service.cancel_order_notification(order2, "Customer requested cancellation")

    # Test 5: Notification History
    print("\n" + "=" * 70)
    print("Test 5: Notification History")
    print("=" * 70)

    history = service.get_notification_history()
    print(f"\nTotal Notifications Sent: {len(history)}")
    for i, event in enumerate(history, 1):
        print(
            f"{i}. Order #{event['order_id']} - {event['event_type'].upper()} - {event['observers_notified']} observers"
        )

    # Test 6: Custom Observer
    print("\n" + "=" * 70)
    print("Test 6: Adding Custom Observer")
    print("=" * 70)

    class LoyaltyPointsObserver(Observer):
        def update(self, order: Order, event_type: str, message: str):
            if event_type == "completed":
                points = int(order.total_amount / 10000)
                print(
                    f"[⭐ LOYALTY - {datetime.now().strftime('%H:%M:%S')}] Points Awarded: {points} points"
                )

        def get_observer_name(self) -> str:
            return "Loyalty Points System"

    service.add_custom_observer(LoyaltyPointsObserver())

    order3 = Order(order_id=125, customer_id=1, total_amount=200000)
    service.create_order_notification(order3, "Member order")
    time.sleep(1)
    service.complete_order_notification(order3, "Member completed order")

    print("\n" + "=" * 70)
    print("Observer Pattern Testing Complete!")
    print("=" * 70)
