"""
RESTAURANT MANAGEMENT SYSTEM - Main Interactive Application
Demonstrasi 6 Design Patterns dalam Sistem Manajemen Restoran
"""

import os
import sys
from datetime import datetime, time
from typing import Optional

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from models.restaurant import Customer, MenuItem, Order
from creational.singleton import DatabaseConnection
from creational.factory import MenuService, MenuItemFactoryProvider
from structural.adapter import ReportExportService
from structural.decorator import (
    MenuDecoratorService,
    ExtraCheeseDecorator,
    ExtraToppingDecorator,
    LargeSizeDecorator,
)
from behavioral.strategy import (
    PricingContext,
    MemberDiscountStrategy,
    PromoDiscountStrategy,
    VoucherDiscountStrategy,
    HappyHourStrategy,
)
from behavioral.observer import OrderNotificationService


class RestaurantApp:
    """Main Application Class"""

    def __init__(self):
        self.db = DatabaseConnection()
        self.menu_service = MenuService()
        self.report_service = ReportExportService()
        self.notification_service = OrderNotificationService()
        self.current_order_items = []

    def clear_screen(self):
        """Clear console screen"""
        os.system("cls" if os.name == "nt" else "clear")

    def print_header(self, title: str):
        """Print formatted header"""
        print("\n" + "=" * 70)
        print(f"{title.center(70)}")
        print("=" * 70)

    def press_enter(self):
        """Wait for user to press enter"""
        input("\nTekan Enter untuk melanjutkan...")

    def display_main_menu(self):
        """Display main menu"""
        self.clear_screen()
        self.print_header("SISTEM MANAJEMEN RESTORAN")
        print("\n🏪 Menu Utama:")
        print("  1. 📋 Kelola Menu Makanan (Factory Pattern)")
        print("  2. 🛒 Buat Pesanan Baru")
        print("  3. ✨ Kustomisasi Menu (Decorator Pattern)")
        print("  4. 💰 Terapkan Diskon (Strategy Pattern)")
        print("  5. 📊 Generate Laporan (Adapter Pattern)")
        print("  6. 🔔 Lihat Notifikasi (Observer Pattern)")
        print("  7. 👥 Kelola Pelanggan")
        print("  8. 💾 Info Database (Singleton Pattern)")
        print("  0. 🚪 Keluar")
        print("=" * 70)

    # ========================= FACTORY PATTERN =========================

    def menu_management(self):
        """Menu management using Factory Pattern"""
        while True:
            self.clear_screen()
            self.print_header("KELOLA MENU (Factory Pattern)")

            print("\n📋 Pilihan Menu:")
            print("  1. Lihat Semua Menu")
            print("  2. Lihat Menu Berdasarkan Tipe")
            print("  3. Tambah Menu Baru")
            print("  4. Update Menu")
            print("  5. Hapus Menu")
            print("  0. Kembali ke Menu Utama")

            choice = input("\nPilihan Anda: ").strip()

            if choice == "1":
                self.view_all_menu()
            elif choice == "2":
                self.view_menu_by_type()
            elif choice == "3":
                self.add_menu_item()
            elif choice == "4":
                self.update_menu_item()
            elif choice == "5":
                self.delete_menu_item()
            elif choice == "0":
                break

    def view_all_menu(self):
        """View all menu items"""
        self.clear_screen()
        self.print_header("SEMUA MENU")

        menus = self.menu_service.get_all_menu()

        if not menus:
            print("\n⚠️  Tidak ada menu yang ditemukan!")
        else:
            current_type = None
            for menu in menus:
                if menu["item_type"] != current_type:
                    current_type = menu["item_type"]
                    print(f"\n{'='*70}")
                    print(f"📁 {current_type.upper()}")
                    print(f"{'='*70}")

                print(f"  [{menu['item_id']}] {menu['item_name']}")
                print(f"      💵 Rp {float(menu['base_price']):,.0f}")
                if menu["description"]:
                    print(f"      📝 {menu['description']}")

        self.press_enter()

    def view_menu_by_type(self):
        """View menu by type"""
        self.clear_screen()
        self.print_header("LIHAT MENU BERDASARKAN TIPE")

        print(
            "\nTipe yang tersedia:",
            ", ".join(MenuItemFactoryProvider.get_available_types()),
        )
        item_type = input("Masukkan tipe menu: ").strip().lower()

        try:
            menus = self.menu_service.get_menu_by_type(item_type)

            if not menus:
                print(f"\n⚠️  Menu {item_type} tidak ditemukan!")
            else:
                print(f"\n{'='*70}")
                print(f"{item_type.upper()} MENU")
                print(f"{'='*70}")

                for menu in menus:
                    print(f"\n  [{menu.item_id}] {menu.item_name}")
                    print(f"      💵 Rp {menu.base_price:,.0f}")
                    print(f"      📝 {menu.description}")

        except Exception as e:
            print(f"\n❌ Error: {e}")

        self.press_enter()

    def add_menu_item(self):
        """Add new menu item using Factory Pattern"""
        self.clear_screen()
        self.print_header("TAMBAH MENU BARU (Factory Pattern)")

        print(
            "\nTipe yang tersedia:",
            ", ".join(MenuItemFactoryProvider.get_available_types()),
        )

        try:
            item_type = input("Tipe menu: ").strip().lower()
            item_name = input("Nama menu: ").strip()
            base_price = float(input("Harga dasar: ").strip())
            description = input("Deskripsi (opsional): ").strip()

            # Default customer_id (chef/owner)
            customer_id = 1

            # Create menu item using factory
            menu_item = self.menu_service.create_menu_item(
                customer_id=customer_id,
                item_type=item_type,
                item_name=item_name,
                base_price=base_price,
                description=description,
            )

            print(f"\n✅ Menu berhasil ditambahkan!")
            print(f"   ID: {menu_item.item_id}")
            print(f"   Nama: {menu_item.item_name}")
            print(f"   Harga: Rp {menu_item.base_price:,.0f}")

        except Exception as e:
            print(f"\n❌ Error: {e}")

        self.press_enter()

    def update_menu_item(self):
        """Update menu item"""
        self.clear_screen()
        self.print_header("UPDATE MENU")

        try:
            item_id = int(input("ID Menu yang akan diupdate: ").strip())

            # Get current item
            current = self.menu_service.get_menu_item(item_id)
            if not current:
                print(f"\n❌ Menu {item_id} tidak ditemukan!")
                self.press_enter()
                return

            print(f"\nSaat ini: {current.item_name} - Rp {current.base_price:,.0f}")

            new_name = input("Nama baru (Enter untuk skip): ").strip()
            new_price_str = input("Harga baru (Enter untuk skip): ").strip()
            new_desc = input("Deskripsi baru (Enter untuk skip): ").strip()

            new_price = float(new_price_str) if new_price_str else None

            self.menu_service.update_menu_item(
                item_id=item_id,
                item_name=new_name if new_name else None,
                base_price=new_price,
                description=new_desc if new_desc else None,
            )

            print(f"\n✅ Menu berhasil diupdate!")

        except Exception as e:
            print(f"\n❌ Error: {e}")

        self.press_enter()

    def delete_menu_item(self):
        """Delete menu item"""
        self.clear_screen()
        self.print_header("HAPUS MENU")

        try:
            item_id = int(input("ID Menu yang akan dihapus: ").strip())

            confirm = (
                input(f"Apakah Anda yakin ingin menghapus menu {item_id}? (ya/tidak): ")
                .strip()
                .lower()
            )

            if confirm == "ya":
                self.menu_service.delete_menu_item(item_id)
                print(f"\n✅ Menu berhasil dihapus!")
            else:
                print("\n❌ Penghapusan dibatalkan.")

        except Exception as e:
            print(f"\n❌ Error: {e}")

        self.press_enter()

    # ========================= DECORATOR PATTERN =========================

    def customize_menu(self):
        """Customize menu items using Decorator Pattern"""
        self.clear_screen()
        self.print_header("KUSTOMISASI MENU (Decorator Pattern)")

        try:
            # Show available menu
            print("\nMenu yang Tersedia:")
            menus = self.menu_service.get_all_menu()
            for i, menu in enumerate(menus[:10], 1):
                print(
                    f"  {i}. {menu['item_name']} - Rp {float(menu['base_price']):,.0f}"
                )

            item_id = int(input("\nMasukkan ID menu untuk dikustomisasi: ").strip())

            base_item = self.menu_service.get_menu_item(item_id)
            if not base_item:
                print(f"\n❌ Menu tidak ditemukan!")
                self.press_enter()
                return

            print(
                f"\nMenu Dasar: {base_item.item_name} - Rp {base_item.base_price:,.0f}"
            )

            # Available decorators
            print("\n✨ Kustomisasi yang Tersedia:")
            print("  1. Extra Keju (+Rp 5,000)")
            print("  2. Extra Topping")
            print("  3. Ukuran Besar (+Rp 10,000)")
            print("  4. Extra Pedas")

            decorators_config = []

            while True:
                choice = input("\nTambah kustomisasi (1-4, 0 untuk selesai): ").strip()

                if choice == "0":
                    break
                elif choice == "1":
                    decorators_config.append({"type": "cheese"})
                    print("  ✓ Ditambahkan: Extra Keju")
                elif choice == "2":
                    topping_name = input("  Nama topping: ").strip()
                    decorators_config.append({"type": "topping", "name": topping_name})
                    print(f"  ✓ Ditambahkan: Extra {topping_name}")
                elif choice == "3":
                    decorators_config.append({"type": "large"})
                    print("  ✓ Ditambahkan: Ukuran Besar")
                elif choice == "4":
                    level = int(input("  Level pedas (1-5): ").strip())
                    decorators_config.append({"type": "spicy", "level": level})
                    print(f"  ✓ Ditambahkan: Extra Pedas Level {level}")

            if decorators_config:
                # Apply decorators
                customized = MenuDecoratorService.apply_decorators(
                    base_item, decorators_config
                )

                print(f"\n{'='*70}")
                print(f"PESANAN KUSTOM")
                print(f"{'='*70}")
                print(f"{customized}")

                # Show breakdown
                print(f"\n💰 Rincian Harga:")
                breakdown = MenuDecoratorService.get_price_breakdown(customized)
                for item in breakdown["items"]:
                    print(f"  • {item['name']}: Rp {item['price']:,.0f}")
                print(f"  {'-'*60}")
                print(f"  TOTAL: Rp {breakdown['total']:,.0f}")

        except Exception as e:
            print(f"\n❌ Error: {e}")

        self.press_enter()

    # ========================= STRATEGY PATTERN =========================

    def apply_discounts(self):
        """Apply discount strategies"""
        self.clear_screen()
        self.print_header("TERAPKAN DISKON (Strategy Pattern)")

        try:
            original_amount = float(input("Masukkan jumlah awal: Rp ").strip())

            print("\n💰 Strategi Diskon yang Tersedia:")
            print("  1. Diskon Member (5-15%)")
            print("  2. Diskon Promo (Potongan Rp 20,000 untuk min Rp 100,000)")
            print("  3. Diskon Voucher (20% off, maks Rp 50,000)")
            print("  4. Happy Hour (25% off, 14:00-16:00)")

            choice = input("\nPilih strategi (1-4): ").strip()

            context = PricingContext()

            if choice == "1":
                print("\nTingkat Member: silver, gold, platinum")
                tier = input("Masukkan tingkat member: ").strip().lower()
                context.set_strategy(MemberDiscountStrategy())
                result = context.calculate_price(original_amount, member_tier=tier)

            elif choice == "2":
                context.set_strategy(PromoDiscountStrategy())
                result = context.calculate_price(original_amount)

            elif choice == "3":
                context.set_strategy(VoucherDiscountStrategy())
                result = context.calculate_price(original_amount)

            elif choice == "4":
                context.set_strategy(HappyHourStrategy())
                current_time = datetime.now().time()
                result = context.calculate_price(
                    original_amount, order_time=current_time
                )

            else:
                print("\n❌ Pilihan tidak valid!")
                self.press_enter()
                return

            print(f"\n{'='*70}")
            print(f"HASIL PERHITUNGAN")
            print(f"{'='*70}")
            print(f"Jumlah Awal    : Rp {result['original_amount']:,.0f}")
            print(f"Diskon         : Rp {result['discount']:,.0f}")
            print(f"Jumlah Akhir   : Rp {result['final_amount']:,.0f}")
            print(f"Strategi       : {result['strategy_name']}")
            print(
                f"Penghematan    : {(result['discount']/result['original_amount']*100):.1f}%"
            )

        except Exception as e:
            print(f"\n❌ Error: {e}")

        self.press_enter()

    # ========================= ADAPTER PATTERN =========================

    def generate_reports(self):
        """Generate reports using Adapter Pattern"""
        self.clear_screen()
        self.print_header("GENERATE LAPORAN (Adapter Pattern)")

        try:
            # Show available orders
            query = "SELECT order_id, customer_id, total_price FROM orders ORDER BY order_id DESC LIMIT 10"
            orders = self.db.execute_query_dict(query)

            if not orders:
                print("\n⚠️  Tidak ada pesanan yang ditemukan!")
                self.press_enter()
                return

            print("\nPesanan yang Tersedia:")
            for order in orders:
                print(
                    f"  Pesanan #{order['order_id']} - Rp {float(order['total_price']):,.0f}"
                )

            order_id = int(input("\nMasukkan ID pesanan untuk di-export: ").strip())

            print(
                "\n📄 Format yang Tersedia:",
                ", ".join(self.report_service.get_supported_formats()),
            )
            format_type = input("Pilih format: ").strip().lower()

            # Export report
            exported_path = self.report_service.export_report(
                order_id, format_type, "exports"
            )

            print(f"\n✅ Laporan berhasil di-export!")
            print(f"   Path: {exported_path}")
            print(f"   Format: {format_type.upper()}")

        except Exception as e:
            print(f"\n❌ Error: {e}")

        self.press_enter()

    # ========================= OBSERVER PATTERN =========================

    def view_notifications(self):
        """View notifications using Observer Pattern"""
        self.clear_screen()
        self.print_header("NOTIFIKASI PESANAN (Observer Pattern)")

        print("\n🔔 Demonstrasi Observer Pattern:")
        print("    Ketika pesanan dibuat, beberapa sistem akan otomatis dinotifikasi:")
        print("    • Sistem Display Dapur")
        print("    • Notifikasi Kasir")
        print("    • Alert Pelayan")
        print("    • Notifikasi SMS")
        print("    • Notifikasi Email")
        print("    • Log Audit")
        print("    • Manajemen Inventori")

        test = input("\nJalankan demo notifikasi? (ya/tidak): ").strip().lower()

        if test == "ya":
            # Create demo order
            demo_order = Order(order_id=999, customer_id=1, total_amount=125000)
            demo_order.customer_phone = "0812-3456-7890"
            demo_order.customer_email = "demo@restaurant.com"
            demo_order.table_number = "A5"

            print(f"\n{'='*70}")
            print("Membuat Demo Pesanan...")
            print(f"{'='*70}")

            self.notification_service.create_order_notification(
                demo_order, "Demo pesanan: Nasi Goreng + Es Teh"
            )

            print(f"\n{'='*70}")
            print("✅ Semua observer berhasil dinotifikasi!")
            print(f"{'='*70}")

        self.press_enter()

    # ========================= OTHER FEATURES =========================

    def manage_customers(self):
        """Manage customers"""
        self.clear_screen()
        self.print_header("KELOLA PELANGGAN")

        query = "SELECT * FROM customers ORDER BY customer_id"
        customers = self.db.execute_query_dict(query)

        print("\n👥 Pelanggan:")
        for customer in customers:
            status = "⭐ Member" if customer["is_member"] else "Reguler"
            print(f"  [{customer['customer_id']}] {customer['name']} - {status}")

        self.press_enter()

    def database_info(self):
        """Show database info (Singleton Pattern demonstration)"""
        self.clear_screen()
        self.print_header("INFO DATABASE (Singleton Pattern)")

        print("\n💾 Database Connection Pool (Singleton):")
        print(f"   Database: {getattr(self.db, 'dbname', 'N/A')}")
        print(f"   User: {getattr(self.db, 'user', 'N/A')}")
        print(
            f"   Host: {getattr(self.db, 'host', 'N/A')}:{getattr(self.db, 'port', 'N/A')}"
        )
        print(
            f"   Status: {'Terhubung ✓' if getattr(self.db, '_is_connected', False) else 'Tidak Terhubung ✗'}"
        )

        # Test singleton
        print("\n🔬 Testing Singleton Pattern:")
        db2 = DatabaseConnection()
        print(f"   Instance yang sama? {self.db is db2} ✓")
        print(f"   Alamat memori: {hex(id(self.db))}")

        # Show table stats
        if getattr(self.db, "_is_connected", False):
            print("\n📊 Statistik Database:")

            queries = [
                ("Pelanggan", "SELECT COUNT(*) FROM customers"),
                ("Menu", "SELECT COUNT(*) FROM menu_items"),
                ("Pesanan", "SELECT COUNT(*) FROM orders"),
                ("Item Pesanan", "SELECT COUNT(*) FROM order_items"),
                ("Laporan", "SELECT COUNT(*) FROM order_reports"),
            ]

            for name, query in queries:
                try:
                    result = self.db.execute_query(query, fetch=True)
                    count = result[0][0] if result else 0
                    print(f"   {name}: {count}")
                except:
                    print(f"   {name}: N/A")
        else:
            print("\n⚠️  Database tidak terhubung. Silakan cek konfigurasi .env:")
            print(f"   - DB_HOST: {getattr(self.db, 'host', 'N/A')}")
            print(f"   - DB_PORT: {getattr(self.db, 'port', 'N/A')}")
            print(f"   - DB_NAME: {getattr(self.db, 'dbname', 'N/A')}")
            print(f"   - DB_USER: {getattr(self.db, 'user', 'N/A')}")

        self.press_enter()

    # ========================= MAIN LOOP =========================

    def run(self):
        """Run application"""
        while True:
            self.display_main_menu()

            choice = input("\nPilihan Anda: ").strip()

            if choice == "1":
                self.menu_management()
            elif choice == "2":
                print("\n⚠️  Fitur pembuatan pesanan - Segera hadir!")
                self.press_enter()
            elif choice == "3":
                self.customize_menu()
            elif choice == "4":
                self.apply_discounts()
            elif choice == "5":
                self.generate_reports()
            elif choice == "6":
                self.view_notifications()
            elif choice == "7":
                self.manage_customers()
            elif choice == "8":
                self.database_info()
            elif choice == "0":
                print("\n👋 Terima kasih telah menggunakan Sistem Manajemen Restoran!")
                print("   Sampai jumpa!\n")
                break
            else:
                print("\n❌ Pilihan tidak valid! Silakan coba lagi.")
                self.press_enter()


if __name__ == "__main__":
    print("=" * 70)
    print("SISTEM MANAJEMEN RESTORAN")
    print("Implementasi Design Patterns dalam Python")
    print("=" * 70)
    print("\n⚠️  Pastikan database PostgreSQL sudah berjalan dan terkonfigurasi!")
    print("   Setup database: database/schema.sql")
    print("   Environment: file .env\n")

    try:
        app = RestaurantApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Aplikasi dihentikan. Sampai jumpa!\n")
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        print("   Silakan cek koneksi dan konfigurasi database.\n")
