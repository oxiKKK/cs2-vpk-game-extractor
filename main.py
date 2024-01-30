import vpk
import argparse
import os
import datetime

parser = argparse.ArgumentParser(
    prog="cs2-vpk-extractor", description="Given an input directory, locates all .vpk files and extracts them to the output directory.")

parser.add_argument("-d", "--cs2dir", help="cs2 directory", required=True)
parser.add_argument("-o", "--outputdir", help="output directory", default=".")
parser.add_argument("-v", "--verbose",
                    help="enables verbosity", action="store_true")

args = parser.parse_args()


def extract_vpk_file(
        filepath: str,  # .vpk file
        outputdir: str  # output directory for extracted files
) -> None:
    """extracts a vpk file to the output directory"""
    try:
        with vpk.open(filepath) as vpkfile:
            for filepath in vpkfile:
                exported_file_path = os.path.join(
                    outputdir, filepath)
                exported_filedir_path = os.path.dirname(exported_file_path)

                if args.verbose:
                    print(' extracting', filepath, 'to', exported_file_path)

                if not os.path.exists(exported_filedir_path):
                    os.makedirs(exported_filedir_path)

                vpkfile[filepath].save(exported_file_path)
                continue

                try:
                    with open(exported_file_path, 'wb') as f:
                        f.write(vpkfile[filepath].read())
                except Exception as e:
                    print(' ', e)
    except Exception as e:
        pass


def main() -> None:
    if not os.path.exists(args.cs2dir):
        print("Error: cs2 directory does not exist")
        return

    print('cs2 directory is', args.cs2dir)
    print('output directory is', args.outputdir)

    for root, dirs, files in os.walk(args.cs2dir):
        for filename in files:
            if not filename.endswith(".vpk"):
                continue

            vpk_file = os.path.join(root, filename)
            out_dir = os.path.join(args.outputdir, 'export')
            extract_vpk_file(vpk_file, out_dir)


if __name__ == "__main__":
    main()
