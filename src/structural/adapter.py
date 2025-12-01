"""
ADAPTER PATTERN - Report Export Adapters
Mengadaptasi laporan restoran ke berbagai format export (PDF, Excel, JSON)
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any
import json
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.restaurant import OrderReport
from creational.singleton import DatabaseConnection


class ReportExporter(ABC):
    """
    Abstract Adapter untuk export laporan

    Teori:
    - Adapter Pattern adalah structural pattern yang memungkinkan objects dengan
      incompatible interfaces bekerja bersama
    - Adapter bertindak sebagai wrapper antara dua objects
    - Mengkonversi interface dari satu class ke interface yang expected oleh client

    Use Case Restaurant:
    - Laporan restoran dalam format internal (OrderReport object)
    - Client butuh format berbeda: PDF untuk print, Excel untuk analisis, JSON untuk API
    - Adapter mengkonversi OrderReport ke format yang diminta tanpa modify original class
    """

    @abstractmethod
    def export(self, report: OrderReport, filepath: str) -> str:
        """Export report ke format tertentu"""
        pass

    @abstractmethod
    def get_extension(self) -> str:
        """Get file extension untuk format ini"""
        pass


class PDFReportAdapter(ReportExporter):
    """
    Adapter untuk export laporan ke format PDF
    Mengadaptasi OrderReport data ke PDF format
    """

    def export(self, report: OrderReport, filepath: str) -> str:
        """
        Export report ke PDF format menggunakan reportlab
        """
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from reportlab.platypus import (
            SimpleDocTemplate,
            Table,
            TableStyle,
            Paragraph,
            Spacer,
        )
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

        if not filepath.endswith(".pdf"):
            filepath += ".pdf"

        # Create PDF
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=18,
            textColor=colors.HexColor("#2c3e50"),
            spaceAfter=30,
            alignment=TA_CENTER,
        )

        # Title
        title = Paragraph("LAPORAN PESANAN RESTORAN", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.3 * inch))

        # Order Info Table
        info_data = [
            ["Report ID:", str(report.report_id or "N/A")],
            ["Order ID:", str(report.order_id)],
            ["Customer:", report.customer_name],
            ["Total Items:", str(report.total_items)],
            ["Total Amount:", f"Rp {report.total_amount:,.0f}"],
            [
                "Created:",
                (
                    report.created_at.strftime("%Y-%m-%d %H:%M:%S")
                    if report.created_at
                    else "N/A"
                ),
            ],
        ]

        info_table = Table(info_data, colWidths=[2 * inch, 4 * inch])
        info_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#ecf0f1")),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#2c3e50")),
                    ("ALIGN", (0, 0), (0, -1), "RIGHT"),
                    ("ALIGN", (1, 0), (1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ]
            )
        )
        elements.append(info_table)
        elements.append(Spacer(1, 0.4 * inch))

        # Items Table
        if report.items_details:
            # Items header
            items_header = Paragraph("<b>ORDER ITEMS</b>", styles["Heading2"])
            elements.append(items_header)
            elements.append(Spacer(1, 0.2 * inch))

            # Items table data
            items_data = [["Item", "Quantity", "Price", "Subtotal"]]
            for item in report.items_details:
                items_data.append(
                    [
                        item.get("item_name", "Unknown"),
                        str(item.get("quantity", 0)),
                        f"Rp {item.get('price', 0):,.0f}",
                        f"Rp {item.get('subtotal', 0):,.0f}",
                    ]
                )

            items_table = Table(
                items_data, colWidths=[2.5 * inch, 1 * inch, 1.5 * inch, 1.5 * inch]
            )
            items_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3498db")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 11),
                        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                        ("FONTSIZE", (0, 1), (-1, -1), 9),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                        ("TOPPADDING", (0, 0), (-1, -1), 8),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                        (
                            "ROWBACKGROUNDS",
                            (0, 1),
                            (-1, -1),
                            [colors.white, colors.HexColor("#ecf0f1")],
                        ),
                    ]
                )
            )
            elements.append(items_table)

        # Footer
        elements.append(Spacer(1, 0.5 * inch))
        footer_style = ParagraphStyle(
            "Footer",
            parent=styles["Normal"],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER,
        )
        footer = Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", footer_style
        )
        elements.append(footer)

        # Build PDF
        doc.build(elements)

        print(f"[PDF ADAPTER] Report exported to: {filepath}")
        return filepath

    def get_extension(self) -> str:
        return ".pdf"


class ExcelReportAdapter(ReportExporter):
    """
    Adapter untuk export laporan ke format Excel
    Mengadaptasi OrderReport data ke Excel format
    """

    def export(self, report: OrderReport, filepath: str) -> str:
        """
        Export report ke Excel format
        Note: Ini simulasi, production code akan gunakan library seperti openpyxl
        """
        if not filepath.endswith(".xlsx"):
            filepath += ".xlsx"

        # Simulasi Excel content dalam CSV format (dalam production gunakan openpyxl)
        excel_content = "LAPORAN PESANAN RESTORAN (EXCEL)\n\n"
        excel_content += "Report Information\n"
        excel_content += f"Report ID,{report.report_id or 'N/A'}\n"
        excel_content += f"Order ID,{report.order_id}\n"
        excel_content += f"Customer,{report.customer_name}\n"
        excel_content += f"Total Items,{report.total_items}\n"
        excel_content += f"Total Amount,Rp {report.total_amount:,.0f}\n"
        excel_content += f"Created,{report.created_at.strftime('%Y-%m-%d %H:%M:%S') if report.created_at else 'N/A'}\n\n"

        excel_content += "Order Items\n"
        excel_content += "Item Name,Quantity,Price,Subtotal\n"

        if report.items_details:
            for item in report.items_details:
                excel_content += f"{item.get('item_name', 'Unknown')},"
                excel_content += f"{item.get('quantity', 0)},"
                excel_content += f"Rp {item.get('price', 0):,.0f},"
                excel_content += f"Rp {item.get('subtotal', 0):,.0f}\n"

        excel_content += f"\nGenerated,{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

        # Save to file (simulasi dengan .csv untuk simplicity)
        actual_filepath = filepath.replace(".xlsx", ".csv")
        with open(actual_filepath, "w", encoding="utf-8") as f:
            f.write(excel_content)

        print(f"[EXCEL ADAPTER] Report exported to: {actual_filepath}")
        return actual_filepath

    def get_extension(self) -> str:
        return ".xlsx"


class JSONReportAdapter(ReportExporter):
    """
    Adapter untuk export laporan ke format JSON
    Mengadaptasi OrderReport data ke JSON format
    """

    def export(self, report: OrderReport, filepath: str) -> str:
        """Export report ke JSON format"""
        if not filepath.endswith(".json"):
            filepath += ".json"

        # Convert OrderReport to JSON-serializable dict
        json_data = {
            "report_info": {
                "report_id": report.report_id,
                "order_id": report.order_id,
                "customer_name": report.customer_name,
                "total_items": report.total_items,
                "total_amount": float(report.total_amount),
                "created_at": (
                    report.created_at.isoformat() if report.created_at else None
                ),
            },
            "items": report.items_details if report.items_details else [],
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "format": "JSON",
                "version": "1.0",
            },
        }

        # Save to file with pretty formatting
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        print(f"[JSON ADAPTER] Report exported to: {filepath}")
        return filepath

    def get_extension(self) -> str:
        return ".json"


class ReportExportService:
    """
    Service untuk export laporan dengan berbagai format
    Menggunakan Adapter Pattern untuk support multiple formats
    Menggunakan Singleton Pattern untuk database access
    """

    _adapters = {
        "pdf": PDFReportAdapter(),
        "excel": ExcelReportAdapter(),
        "json": JSONReportAdapter(),
    }

    def __init__(self):
        self.db = DatabaseConnection()

    @classmethod
    def get_adapter(cls, format_type: str) -> ReportExporter:
        """Get adapter berdasarkan format type"""
        adapter = cls._adapters.get(format_type.lower())
        if not adapter:
            raise ValueError(
                f"Unsupported format: {format_type}. Available: {cls.get_supported_formats()}"
            )
        return adapter

    @classmethod
    def get_supported_formats(cls):
        """Get list of supported export formats"""
        return list(cls._adapters.keys())

    def get_order_report(self, order_id: int) -> OrderReport:
        """
        Generate OrderReport dari database
        """
        # Get order data
        order_query = """
            SELECT o.*, c.name as customer_name, c.is_member
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            WHERE o.order_id = %s
        """
        order_result = self.db.execute_query_dict(order_query, (order_id,))

        if not order_result:
            raise ValueError(f"Order {order_id} not found")

        order = order_result[0]

        # Get order items
        items_query = """
            SELECT oi.*, m.item_name, m.item_type
            FROM order_items oi
            JOIN menu_items m ON oi.item_id = m.item_id
            WHERE oi.order_id = %s
        """
        items_result = self.db.execute_query_dict(items_query, (order_id,))

        # Create OrderReport
        report = OrderReport(
            order_id=order["order_id"],
            customer_name=order["customer_name"],
            total_items=len(items_result),
            total_amount=float(order["total_price"]),
        )

        # Add items details
        report.items_details = []
        for item in items_result:
            subtotal = float(item["quantity"]) * float(item["price"])
            report.items_details.append(
                {
                    "item_name": item["item_name"],
                    "quantity": item["quantity"],
                    "price": float(item["price"]),
                    "subtotal": subtotal,
                }
            )

        return report

    def export_report(
        self, order_id: int, format_type: str, output_dir: str = "exports"
    ) -> str:
        """
        Export order report ke format tertentu

        Args:
            order_id: ID order yang akan di-export
            format_type: Format export (pdf, excel, json)
            output_dir: Directory untuk save file

        Returns:
            Path to exported file
        """
        # Create output directory if not exists
        os.makedirs(output_dir, exist_ok=True)

        # Get report data
        report = self.get_order_report(order_id)

        # Get appropriate adapter
        adapter = self.get_adapter(format_type)

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"order_{order_id}_report_{timestamp}"
        filepath = os.path.join(output_dir, filename)

        # Export using adapter
        exported_path = adapter.export(report, filepath)

        # Save report record to database
        self._save_report_record(report, format_type, exported_path)

        return exported_path

    def _save_report_record(self, report: OrderReport, format_type: str, filepath: str):
        """Save report record to database"""
        query = """
            INSERT INTO order_reports (order_id, report_type, report_path)
            VALUES (%s, %s, %s)
            RETURNING report_id
        """
        result = self.db.execute_query(
            query, (report.order_id, format_type.upper(), filepath), fetch=True
        )
        report.report_id = result[0][0]
        print(f"[SERVICE] Report record saved with ID: {report.report_id}")

    def get_all_reports(self):
        """Get all generated reports"""
        query = """
            SELECT r.*, o.customer_id, c.name as customer_name
            FROM order_reports r
            JOIN orders o ON r.order_id = o.order_id
            JOIN customers c ON o.customer_id = c.customer_id
            ORDER BY r.created_at DESC
        """
        return self.db.execute_query_dict(query)


# Test Adapter Pattern
if __name__ == "__main__":
    print("=" * 70)
    print("TESTING ADAPTER PATTERN - Report Export System")
    print("=" * 70)

    service = ReportExportService()

    print("\nSupported formats:", service.get_supported_formats())

    try:
        # Test export report to all formats
        order_id = 1

        print(f"\n" + "=" * 70)
        print(f"Exporting Order #{order_id} to multiple formats...")
        print("=" * 70)

        # Get report data first
        report = service.get_order_report(order_id)
        print(f"\nOrder Report:")
        print(f"  Customer: {report.customer_name}")
        print(f"  Total Items: {report.total_items}")
        print(f"  Total Amount: Rp {report.total_amount:,.0f}")

        print(f"\n  Items:")
        for item in report.items_details:
            print(
                f"    • {item['item_name']} x{item['quantity']} = Rp {item['subtotal']:,.0f}"
            )

        # Export to PDF
        print("\n" + "=" * 70)
        pdf_path = service.export_report(order_id, "pdf", "exports")
        print(f"PDF exported successfully")

        # Export to Excel
        print("\n" + "=" * 70)
        excel_path = service.export_report(order_id, "excel", "exports")
        print(f"Excel exported successfully")

        # Export to JSON
        print("\n" + "=" * 70)
        json_path = service.export_report(order_id, "json", "exports")
        print(f"JSON exported successfully")

        # Show all reports
        print("\n" + "=" * 70)
        print("All Generated Reports:")
        print("=" * 70)
        reports = service.get_all_reports()
        for r in reports[:5]:
            print(
                f"  • Order #{r['order_id']} - {r['report_type']} - {r['customer_name']}"
            )

    except Exception as e:
        print(f"Error: {e}")
        print("Make sure database is setup and has orders data")
