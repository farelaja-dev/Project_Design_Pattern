"""
Generate Class Diagram menggunakan py2puml
Menghasilkan PlantUML text yang bisa di-render menjadi diagram
"""

import os
import sys

# Add src to path
sys.path.insert(0, "src")


def generate_plantuml_diagrams():
    """Generate PlantUML diagrams untuk semua modules"""

    print("=" * 70)
    print("PLANTUML CLASS DIAGRAM GENERATOR")
    print("=" * 70)

    # Create diagrams directory
    output_dir = "diagrams"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"\n✓ Directory '{output_dir}/' dibuat")

    diagrams = {
        "1_models": ["models.restaurant"],
        "2_creational_singleton": ["creational.singleton"],
        "3_creational_factory": ["creational.factory"],
        "4_structural_adapter": ["structural.adapter"],
        "5_structural_decorator": ["structural.decorator"],
        "6_behavioral_strategy": ["behavioral.strategy"],
        "7_behavioral_observer": ["behavioral.observer"],
        "8_complete_system": [
            "models.restaurant",
            "creational.singleton",
            "creational.factory",
            "structural.adapter",
            "structural.decorator",
            "behavioral.strategy",
            "behavioral.observer",
        ],
    }

    print("\n🔨 Generating PlantUML diagrams...\n")

    for diagram_name, modules in diagrams.items():
        try:
            output_file = os.path.join(output_dir, f"{diagram_name}.puml")

            # Start PlantUML content
            puml_content = "@startuml\n"
            puml_content += f"title {diagram_name.replace('_', ' ').title()}\n"
            puml_content += "skinparam classAttributeIconSize 0\n"
            puml_content += "skinparam shadowing false\n"
            puml_content += "skinparam backgroundColor white\n\n"

            # Import and analyze each module
            for module_name in modules:
                try:
                    # Import module
                    module = __import__(module_name, fromlist=[""])

                    # Get all classes
                    import inspect

                    classes = inspect.getmembers(module, inspect.isclass)

                    puml_content += f'package "{module_name}" {{\n'

                    # First pass: collect class definitions
                    class_definitions = []
                    relationships = []

                    for class_name, class_obj in classes:
                        # Skip imported classes from other modules
                        if class_obj.__module__ != module_name:
                            continue

                        # Determine class type
                        is_abstract = inspect.isabstract(class_obj)
                        if is_abstract:
                            class_def = f"  abstract class {class_name} {{\n"
                        else:
                            class_def = f"  class {class_name} {{\n"

                        # Extract attributes from __init__ method
                        attributes = []
                        if hasattr(class_obj, "__init__"):
                            try:
                                import re

                                init_source = inspect.getsource(class_obj.__init__)
                                # Find self.attribute = ... patterns
                                attr_pattern = r"self\.([a-zA-Z_][a-zA-Z0-9_]*)\s*="
                                found_attrs = re.findall(attr_pattern, init_source)
                                # Remove duplicates and private attributes starting with __
                                attributes = [
                                    attr
                                    for attr in dict.fromkeys(found_attrs)
                                    if not attr.startswith("__")
                                ]
                            except:
                                pass

                        # Add attributes section
                        if attributes:
                            class_def += "    .. Attributes ..\n"
                            for attr in attributes:
                                # Determine visibility
                                if attr.startswith("_"):
                                    visibility = "-"  # Private
                                else:
                                    visibility = "+"  # Public
                                class_def += f"    {visibility}{attr}\n"

                        # Add methods section
                        methods = inspect.getmembers(
                            class_obj, predicate=inspect.isfunction
                        )
                        method_list = []
                        for method_name, method_obj in methods:
                            if not method_name.startswith("_") or method_name in [
                                "__init__",
                                "__new__",
                                "__str__",
                            ]:
                                # Get method signature
                                try:
                                    sig = inspect.signature(method_obj)
                                    params = ", ".join(
                                        [
                                            p
                                            for p in sig.parameters.keys()
                                            if p != "self"
                                        ]
                                    )
                                    method_list.append(f"{method_name}({params})")
                                except:
                                    method_list.append(f"{method_name}()")

                        if method_list:
                            if attributes:  # Only add separator if we had attributes
                                class_def += "    .. Methods ..\n"
                            for method in method_list:
                                class_def += f"    +{method}\n"

                        class_def += "  }\n\n"
                        class_definitions.append(class_def)

                        # Detect inheritance relationships
                        if hasattr(class_obj, "__bases__"):
                            for base in class_obj.__bases__:
                                if base.__name__ != "object" and base.__name__ != "ABC":
                                    # Check if base class is in same module
                                    if base.__module__ == module_name:
                                        relationships.append(
                                            f"  {base.__name__} <|-- {class_name}\n"
                                        )

                    # Add all class definitions
                    for class_def in class_definitions:
                        puml_content += class_def

                    # Add relationships after classes
                    if relationships:
                        puml_content += "  ' Relationships\n"
                        for rel in relationships:
                            puml_content += rel

                    puml_content += "}\n\n"

                except Exception as e:
                    print(f"  ⚠️  Warning: Could not analyze {module_name}: {e}")

            puml_content += "@enduml\n"

            # Write to file
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(puml_content)

            print(f"✓ {diagram_name}.puml dibuat")

        except Exception as e:
            print(f"✗ Error creating {diagram_name}: {e}")

    print("\n" + "=" * 70)
    print("SELESAI!")
    print("=" * 70)
    print(f"\n📁 PlantUML files tersimpan di: {output_dir}/")
    print("\n💡 Cara melihat diagram:")
    print("   1. Online: https://www.plantuml.com/plantuml/uml/")
    print("      - Copy-paste isi file .puml")
    print("   2. VS Code: Install extension 'PlantUML'")
    print("   3. IntelliJ IDEA: Built-in PlantUML support")

    # List generated files
    files = [f for f in os.listdir(output_dir) if f.endswith(".puml")]
    if files:
        print(f"\nFile yang dihasilkan ({len(files)} files):")
        for file in sorted(files):
            print(f"   • {file}")


if __name__ == "__main__":
    try:
        generate_plantuml_diagrams()
        print("\n✨ Diagram berhasil di-generate!\n")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
