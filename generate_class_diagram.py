"""
Script untuk generate Class Diagram otomatis dari source code
Menggunakan pyreverse (pylint) untuk analyze code dan generate UML diagram
"""

import os
import subprocess
import sys


def generate_class_diagram():
    """Generate class diagram dari semua modules dalam src/"""

    print("=" * 70)
    print("CLASS DIAGRAM GENERATOR")
    print("Menganalisis code dan membuat UML Class Diagram...")
    print("=" * 70)

    # Output directory
    output_dir = "diagrams"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"\n✓ Directory '{output_dir}/' dibuat")

    # Modules to analyze
    modules = [
        "src.models.restaurant",
        "src.creational.singleton",
        "src.creational.factory",
        "src.structural.adapter",
        "src.structural.decorator",
        "src.behavioral.strategy",
        "src.behavioral.observer",
    ]

    print("\n📦 Modules yang akan dianalisis:")
    for module in modules:
        print(f"   • {module}")

    # Generate class diagram for each category
    categories = {
        "models": ["src.models.restaurant"],
        "creational": ["src.creational.singleton", "src.creational.factory"],
        "structural": ["src.structural.adapter", "src.structural.decorator"],
        "behavioral": ["src.behavioral.strategy", "src.behavioral.observer"],
        "all": modules,
    }

    print("\n🔨 Generating diagrams...\n")

    for category, mods in categories.items():
        try:
            # Construct pyreverse command
            cmd = [
                "pyreverse",
                "-o",
                "png",  # Output format PNG
                "-p",
                f"restaurant_{category}",  # Project name
                "-d",
                output_dir,  # Output directory
                "--colorized",  # Add colors
            ] + [m.replace(".", "/") + ".py" for m in mods]

            # Run pyreverse
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.abspath(__file__)),
            )

            if result.returncode == 0:
                print(f"✓ Class diagram '{category}' berhasil dibuat")
                print(f"  Output: diagrams/classes_restaurant_{category}.png")
            else:
                print(f"✗ Gagal membuat diagram '{category}'")
                if result.stderr:
                    print(f"  Error: {result.stderr}")

        except Exception as e:
            print(f"✗ Error pada '{category}': {e}")

    print("\n" + "=" * 70)
    print("SELESAI!")
    print("=" * 70)
    print("\n📁 Class diagrams tersimpan di folder: diagrams/")
    print("\nFile yang dihasilkan:")

    # List generated files
    if os.path.exists(output_dir):
        files = [f for f in os.listdir(output_dir) if f.endswith(".png")]
        if files:
            for file in sorted(files):
                file_path = os.path.join(output_dir, file)
                file_size = os.path.getsize(file_path) / 1024  # KB
                print(f"   • {file} ({file_size:.1f} KB)")
        else:
            print("   (Tidak ada file yang dihasilkan)")

    print("\n💡 Tips:")
    print("   - Buka file PNG dengan image viewer atau browser")
    print("   - Untuk detail lebih, lihat classes_restaurant_all.png")
    print("   - Setiap pattern memiliki diagram terpisah")

    return True


def generate_package_diagram():
    """Generate package diagram untuk menunjukkan struktur project"""

    print("\n" + "=" * 70)
    print("PACKAGE DIAGRAM GENERATOR")
    print("=" * 70)

    output_dir = "diagrams"

    try:
        cmd = [
            sys.executable,
            "-m",
            "pylint.pyreverse",
            "-o",
            "png",
            "-p",
            "restaurant_packages",
            "-d",
            output_dir,
            "--colorized",
            "src",
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__)),
        )

        if result.returncode == 0:
            print("✓ Package diagram berhasil dibuat")
            print("  Output: diagrams/packages_restaurant_packages.png")
        else:
            print("✗ Gagal membuat package diagram")

    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    try:
        # Generate class diagrams
        generate_class_diagram()

        # Generate package diagram
        generate_package_diagram()

        print("\n✨ Class diagrams berhasil di-generate!")
        print("   Silakan cek folder 'diagrams/' untuk melihat hasilnya.\n")

    except KeyboardInterrupt:
        print("\n\n⚠️  Proses dibatalkan oleh user.\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback

        traceback.print_exc()
