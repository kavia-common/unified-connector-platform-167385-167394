import json
from pathlib import Path

"""
Utility script to generate and write the OpenAPI schema to interfaces/openapi.json.

Safe to run from any working directory:
    python -m src.api.generate_openapi
"""

def _resolve_output_dir() -> Path:
    """
    Resolve the interfaces directory relative to the backend_service folder,
    regardless of the current working directory.
    """
    # Locate this file, then go up to backend_service directory and into interfaces
    this_file = Path(__file__).resolve()
    backend_root = this_file.parents[3]  # .../backend_service
    return backend_root / "interfaces"

def main():
    # Import app lazily to avoid side effects during module import
    from src.api.main import app

    # Get the OpenAPI schema
    openapi_schema = app.openapi()

    # Write to file under backend_service/interfaces
    output_dir = _resolve_output_dir()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "openapi.json"

    with output_path.open("w") as f:
        json.dump(openapi_schema, f, indent=2)
    print(f"OpenAPI schema written to: {output_path}")

if __name__ == "__main__":
    main()
