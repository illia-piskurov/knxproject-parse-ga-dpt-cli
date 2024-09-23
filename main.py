"""Extract and parse a KNX project file."""
import getopt
import sys
from xknxproject.models import KNXProject
from xknxproject import XKNXProj
from xknxproject.exceptions.exceptions import InvalidPasswordException
import json

def show_help() -> None:
    """Print Help."""
    print("GA - DPT Parse from knxproject.")
    print("")
    print("Usage:")
    print("")
    print(__file__, "-f --file name.knxproj     Name of knxproject file")
    print(__file__, "-p --pass 1234             Project password")
    print(__file__, "-h --help                  Print help")
    print("")

def group_addresses_with_dpt(filename: str, password: str | None) -> None:
    knxproj: XKNXProj = XKNXProj(
        path=filename,
        password=password
    )
    project: KNXProject = knxproj.parse()

    group_addresses = {}
    for v in project['group_addresses'].values():
        if v['dpt'] is not None:
            group_addresses[v['address']] = f"DPT {v['dpt']['main']}.{v['dpt']['sub']:03}"

    with open('output.json', 'w', encoding='utf-8') as file:
        json.dump(group_addresses, file, ensure_ascii=False, indent=4)

def main(argv: list[str]) -> None:
    """Parse command line arguments and start monitor."""
    try:
        opts, _ = getopt.getopt(argv, "hf:p:", ["help", "file=", "pass="])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)

    filename = None
    password = None
    for opt, arg in opts:
        if opt in ["-h", "--help"]:
            show_help()
            sys.exit()
        if opt in ["-f", "--file"]:
            filename = arg
        if opt in ["-p", "--pass"]:
            password = arg
    
    if filename is None:
        print("Error: The --file argument is required.")
        show_help()
        sys.exit(1)

    try:
        group_addresses_with_dpt(filename, password)
    except InvalidPasswordException:
        print("Error: That project file required password.")
        sys.exit(1)
    print("Result saved to output.json")


if __name__ == "__main__":
    main(sys.argv[1:])