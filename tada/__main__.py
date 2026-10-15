import argparse
from pathlib import Path
import sqlite3
import sys
from .adapters import normalize
from .core import dumps, loads
from .fixtures import write
from .storage import connect, ingest


def transform(bundle, strict=False):
    if not isinstance(bundle, list):
        raise ValueError(
            "Input must be an array of provider/entity/context/record envelopes"
        )
    result = []
    for index, item in enumerate(bundle):
        try:
            record = normalize(
                item["provider"], item["entity"], item["record"], item["context"]
            )
        except (KeyError, ValueError, TypeError) as exc:
            raise ValueError(f"Invalid envelope at index {index}: {exc}") from exc
        if strict and record["diagnostics"]:
            raise ValueError(
                f"Strict mode rejected envelope {index} with {len(record['diagnostics'])} diagnostics"
            )
        result.append(record)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Local provider data normalization platform"
    )
    commands = parser.add_subparsers(dest="command", required=True)
    gen = commands.add_parser("generate", help="Generate deterministic synthetic data")
    gen.add_argument("--output", default="fixtures")
    gen.add_argument("--seed", type=int, default=42)
    for name in ("normalize", "ingest", "validate"):
        sub = commands.add_parser(name)
        sub.add_argument("input")
        sub.add_argument("--strict", action="store_true")
        if name == "normalize":
            sub.add_argument("--output", default="local/normalized.json")
        if name == "ingest":
            sub.add_argument("--db", default="local/tada.sqlite")
    export = commands.add_parser("export")
    export.add_argument("--db", default="local/tada.sqlite")
    export.add_argument("--output", default="local/export.json")
    server = commands.add_parser("serve")
    server.add_argument("--db", default="local/tada.sqlite")
    server.add_argument("--port", type=int, default=8080)
    args = parser.parse_args(argv)
    try:
        if args.command == "generate":
            write(args.output, args.seed)
            print("Synthetic fixtures generated")
            return 0
        if args.command == "serve":
            from .server import serve

            serve(args.db, args.port)
            return 0
        if args.command == "export":
            db = connect(args.db)
            try:
                records = [
                    loads(r[0])
                    for r in db.execute("SELECT document FROM records ORDER BY id")
                ]
            finally:
                db.close()
        else:
            bundle = loads(Path(args.input).read_text())
            if args.command == "validate":
                from .contracts import source_errors

                errors = []
                for i, item in enumerate(bundle):
                    for error in source_errors(
                        item["provider"], item["entity"], item["record"]
                    ):
                        errors.append({"envelope": i, **error})
                if errors:
                    print(dumps(errors, indent=2))
                    return 1
                print(f"{len(bundle)} source fixtures satisfy their selected schemas")
                return 0
            records = transform(bundle, args.strict)
            if args.command == "ingest":
                db = connect(args.db)
                try:
                    count = ingest(db, records)
                finally:
                    db.close()
                print(f"Imported {count} records atomically")
                return 0
        destination = Path(args.output)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(dumps(records, indent=2, sort_keys=True) + "\n")
        print(f"Wrote {len(records)} records to {destination}")
        return 0
    except (OSError, ValueError, sqlite3.Error) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except ImportError:
        print(
            'Install validation dependencies with: pip install -e ".[test]"',
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
