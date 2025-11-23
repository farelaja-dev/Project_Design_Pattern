# LAPORAN PROJECT AKHIR

## Implementasi Design Patterns dalam Sistem Manajemen Restoran

---

### 📋 INFORMASI PROJECT

**Mata Kuliah:** Pola-Pola Perancangan Perangkat Lunak  
**Judul Project:** Sistem Manajemen Restoran dengan Design Patterns  
**Tanggal:** November 2025  
**Teknologi:** Python 3.10, PostgreSQL, Design Patterns  
**Repository:** Project_Akhir2

---

## 1. PENDAHULUAN

### 1.1 Latar Belakang

Dalam pengembangan perangkat lunak modern, design patterns menjadi solusi umum untuk masalah-masalah yang sering muncul. Design patterns memberikan template yang telah terbukti efektif untuk menyelesaikan masalah desain software yang berulang.

Project ini mengimplementasikan **6 Design Patterns** dalam konteks sistem manajemen restoran yang nyata dan dapat digunakan, yaitu:

- **Creational Patterns** (2): Singleton Pattern & Factory Pattern
- **Structural Patterns** (2): Adapter Pattern & Decorator Pattern
- **Behavioral Patterns** (2): Strategy Pattern & Observer Pattern

### 1.2 Tujuan Project

1. Mengimplementasikan design patterns dalam aplikasi nyata
2. Memahami kapan dan mengapa menggunakan setiap pattern
3. Mendemonstrasikan interaksi antar patterns
4. Membuat sistem yang maintainable dan extensible
5. Mengintegrasikan dengan database PostgreSQL

### 1.3 Study Case: Sistem Manajemen Restoran

**Deskripsi Sistem:**

Sistem untuk mengelola operasional restoran yang mencakup:

- **Menu Management**: Kelola berbagai jenis menu (main course, beverage, dessert, appetizer) menggunakan Factory Pattern
- **Order Processing**: Proses pesanan pelanggan dengan sistem yang terorganisir
- **Customization**: Kustomisasi menu dengan berbagai tambahan (keju, topping, ukuran) menggunakan Decorator Pattern
- **Pricing Strategy**: Berbagai strategi diskon (member, promo, voucher, happy hour) menggunakan Strategy Pattern
- **Report Export**: Export laporan ke berbagai format (PDF, Excel, JSON) menggunakan Adapter Pattern
- **Notification System**: Notifikasi otomatis ke berbagai sistem menggunakan Observer Pattern
- **Database Management**: Koneksi database efisien menggunakan Singleton Pattern

---

## 2. IMPLEMENTASI DESIGN PATTERNS

### 2.1 SINGLETON PATTERN - Database Connection

**File:** `src/creational/singleton.py`

**Problem:** Aplikasi membutuhkan koneksi database yang efisien. Jika setiap operasi membuat koneksi baru, akan terjadi memory overhead dan resource exhaustion.

**Solusi:** Singleton Pattern memastikan hanya ada 1 instance DatabaseConnection dengan connection pooling.

**Keuntungan:**

- ✅ Single connection pool untuk seluruh aplikasi
- ✅ Resource efficient
- ✅ Thread-safe
- ✅ Consistent database state

---

### 2.2 FACTORY PATTERN - Menu Creation

**File:** `src/creational/factory.py`

**Problem:** Restoran memiliki 4 jenis menu berbeda (main_course, beverage, dessert, appetizer) dengan validasi berbeda.

**Solusi:** Factory Pattern dengan concrete factories untuk setiap jenis menu.

**Keuntungan:**

- ✅ Centralized creation logic
- ✅ Easy to add new menu types
- ✅ Type-specific validation
- ✅ Loose coupling

---

### 2.3 ADAPTER PATTERN - Report Export

**File:** `src/structural/adapter.py`

**Problem:** Export laporan ke 3 format berbeda (PDF, Excel, JSON) dengan API yang berbeda-beda.

**Solusi:** Adapter Pattern dengan uniform interface untuk semua format.

**Keuntungan:**

- ✅ Uniform interface
- ✅ Format details encapsulated
- ✅ Easy to add new formats
- ✅ Client code remains simple

**Implementasi PDF:**

- Menggunakan reportlab library
- Generate PDF dengan tabel dan styling profesional
- Layout dengan A4 pagesize
- Include order info, items table, timestamp

---

### 2.4 DECORATOR PATTERN - Menu Customization

**File:** `src/structural/decorator.py`

**Problem:** Pelanggan ingin kustomisasi menu (extra keju, ukuran besar, level pedas). Tanpa decorator akan terjadi class explosion.

**Solusi:** Decorator Pattern untuk dynamic customization.

**Keuntungan:**

- ✅ Flexible combinations
- ✅ Runtime composition
- ✅ Dynamic pricing
- ✅ No class explosion

**Available Decorators:**

- ExtraCheeseDecorator (+Rp 5,000)
- ExtraToppingDecorator (custom price)
- LargeSizeDecorator (+Rp 10,000)
- ExtraSpicyDecorator (free)

---

### 2.5 STRATEGY PATTERN - Discount Strategies

**File:** `src/behavioral/strategy.py`

**Problem:** Multiple discount rules yang complex dengan nested if-else.

**Solusi:** Strategy Pattern dengan interchangeable algorithms.

**Keuntungan:**

- ✅ Clean code, no nested if-else
- ✅ Easy to add new strategies
- ✅ Runtime selection
- ✅ Independently testable

**Available Strategies:**

1. MemberDiscountStrategy (5-15% based on tier)
2. PromoDiscountStrategy (Rp 20,000 off for min Rp 100,000)
3. VoucherDiscountStrategy (20% off, max Rp 50,000)
4. HappyHourStrategy (25% off during 14:00-16:00)

---

### 2.6 OBSERVER PATTERN - Order Notifications

**File:** `src/behavioral/observer.py`

**Problem:** Ketika order dibuat, berbagai sistem perlu tahu (kitchen, cashier, waiter, SMS, email, audit, inventory).

**Solusi:** Observer Pattern untuk automatic broadcast.

**Keuntungan:**

- ✅ Loose coupling
- ✅ Automatic notification
- ✅ Easy to add new observers
- ✅ Guaranteed notifications

**Available Observers:**

1. KitchenDisplayObserver
2. CashierObserver
3. WaiterAlertObserver
4. SMSNotificationObserver
5. EmailNotificationObserver
6. AuditLogObserver
7. InventoryObserver

---

## 3. ARSITEKTUR SISTEM

### 3.1 Database Schema

**Database:** PostgreSQL - `restaurant`

**Tables:**

1. `customers` - Data pelanggan
2. `menu_items` - Menu restoran
3. `orders` - Pesanan
4. `order_items` - Detail item pesanan
5. `order_reports` - History export laporan

### 3.2 Project Structure

```
Project_Akhir2/
├── database/
│   └── schema.sql
├── src/
│   ├── models/
│   │   └── restaurant.py
│   ├── creational/
│   │   ├── singleton.py
│   │   └── factory.py
│   ├── structural/
│   │   ├── adapter.py
│   │   └── decorator.py
│   └── behavioral/
│       ├── strategy.py
│       └── observer.py
├── exports/              # Output PDF, Excel, JSON
├── main.py              # CLI Application
├── demo.py              # Automated Demo
└── requirements.txt     # Dependencies
```

### 3.3 Dependencies

```
psycopg2-binary==2.9.9    # PostgreSQL adapter
python-dotenv==1.0.0      # Environment variables
tabulate==0.9.0           # Pretty tables
reportlab==4.4.5          # PDF generation
openpyxl==3.1.2           # Excel files
```

---

## 4. CARA PENGGUNAAN

### 4.1 Setup Database

```powershell
psql -U postgres
CREATE DATABASE restaurant;
\q
psql -U postgres -d restaurant -f database/schema.sql
```

### 4.2 Setup Environment

```powershell
pip install -r requirements.txt
copy .env.example .env
# Edit .env dengan kredensial database
```

### 4.3 Run Application

```powershell
python main.py
```

**Menu Tersedia:**

1. Kelola Menu (Factory Pattern)
2. Buat Pesanan Baru
3. Kustomisasi Menu (Decorator Pattern)
4. Terapkan Diskon (Strategy Pattern)
5. Generate Laporan (Adapter Pattern)
6. Lihat Notifikasi (Observer Pattern)
7. Kelola Pelanggan
8. Info Database (Singleton Pattern)

---

## 5. STUDI KASUS

### 5.1 Skenario 1: Operasional Harian

**Pagi hari - Setup:**

- Singleton: Semua staff connect ke database yang sama
- Factory: Chef tambah menu spesial hari ini

**Siang - Customer Order:**

- Decorator: "Nasi Goreng dengan extra keju dan ukuran besar"
- Strategy: Member Gold dapat diskon 10%
- Observer: Kitchen, cashier, waiter semua dapat notifikasi otomatis

**Sore - Happy Hour:**

- Strategy: Otomatis detect waktu 14:00-16:00, apply 25% discount

**Malam - Closing:**

- Adapter: Export laporan hari ini ke PDF dan Excel

### 5.2 Skenario 2: Corporate Catering

**Large Order:**

- Factory: Buat paket combo khusus
- Decorator: Customize untuk vegetarian options
- Strategy: Corporate voucher 20% off (max Rp 500,000)
- Observer: Alert kitchen untuk persiapan khusus
- Adapter: Export invoice PDF untuk finance

---

## 6. HASIL DAN PEMBAHASAN

### 6.1 Keberhasilan Implementasi

✅ **Semua 6 patterns berhasil:**

- Singleton: Database connection efficient
- Factory: 4 menu types dengan validasi
- Adapter: 3 export formats (PDF real dengan reportlab)
- Decorator: 4 decorators stackable
- Strategy: 4 discount strategies
- Observer: 7 observers automatic notification

✅ **Database Integration:**

- PostgreSQL dengan 5 tables
- CRUD operations complete
- Foreign key relationships

✅ **User Interface:**

- CLI interaktif dalam Bahasa Indonesia
- Error handling graceful
- Visual feedback clear

### 6.2 Keuntungan Design Patterns

1. **Maintainability**: Code terorganisir, mudah dibaca
2. **Extensibility**: Mudah add features baru
3. **Testability**: Components independently testable
4. **Reusability**: Patterns applicable ke project lain
5. **Best Practices**: Follow SOLID principles

### 6.3 Challenges & Solutions

| Challenge            | Solution          | Result                 |
| -------------------- | ----------------- | ---------------------- |
| Database connections | Singleton Pattern | Efficient pooling      |
| Multiple menu types  | Factory Pattern   | Centralized validation |
| Export formats       | Adapter Pattern   | Uniform interface      |
| Menu customization   | Decorator Pattern | Flexible stacking      |
| Discount rules       | Strategy Pattern  | Clean algorithms       |
| System notifications | Observer Pattern  | Automatic broadcast    |

---

## 7. KESIMPULAN

### 7.1 Ringkasan

Project berhasil mengimplementasikan 6 Design Patterns dalam sistem restoran yang functional. Setiap pattern menyelesaikan specific problem dengan elegant solution.

Sistem terbukti:

- ✅ Maintainable
- ✅ Extensible
- ✅ Scalable
- ✅ Professional

### 7.2 Learning Outcomes

1. ✅ Memahami 6 Design Patterns
2. ✅ Implementasi dalam real-world scenario
3. ✅ PostgreSQL integration
4. ✅ Python OOP best practices
5. ✅ PDF/Excel/JSON file generation

### 7.3 Future Improvements

**Short Term:**

- Implement order creation feature
- Add authentication system
- Data visualization

**Long Term:**

- Web interface (Flask/Django)
- REST API
- Mobile apps
- Cloud deployment

---

## 8. REFERENSI

1. **Design Patterns: Elements of Reusable Object-Oriented Software** - Gang of Four, 1994
2. **Head First Design Patterns** - Freeman & Robson, O'Reilly Media
3. **Refactoring Guru** - https://refactoring.guru/design-patterns
4. **PostgreSQL Documentation** - https://www.postgresql.org/docs/
5. **ReportLab Documentation** - https://www.reportlab.com/docs/

---

## 9. APPENDIX

### 9.1 Useful Queries

```sql
-- View all orders
SELECT o.order_id, c.name, o.total_price, o.order_date
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
ORDER BY o.order_date DESC;

-- Top selling items
SELECT m.item_name, SUM(oi.quantity) as total_sold
FROM menu_items m
JOIN order_items oi ON m.item_id = oi.item_id
GROUP BY m.item_id, m.item_name
ORDER BY total_sold DESC;

-- Export statistics
SELECT report_type, COUNT(*) as total
FROM order_reports
GROUP BY report_type;
```

### 9.2 Testing Commands

```powershell
# Run main app
python main.py

# Run demo
python demo.py

# Clear cache
Get-ChildItem -Path . -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force

# Test database connection
python -c "from src.creational.singleton import DatabaseConnection; db = DatabaseConnection(); print(db._is_connected)"
```

### 9.3 Common Issues

**Issue: "ModuleNotFoundError"**

```powershell
Solution: pip install -r requirements.txt
```

**Issue: "Connection refused"**

```
Solution: Check PostgreSQL service dan credentials di .env
```

**Issue: "PDF cannot be opened"**

```powershell
Solution: pip install reportlab
Clear cache dan restart
```

---

**END OF REPORT**

---

_Sistem fully functional dan siap digunakan._

**Author:** Farel  
**Semester:** 5  
**Tahun:** 2025
