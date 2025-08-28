import argparse
import magic
import mimetypes
import os
import sys

def fix_file_extensions(directory):
    """
    Analyzes files in a directory, and adds the appropriate extension to files that don't have one.
    """
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        sys.exit(1)

    examined_files = 0
    renamed_files = 0
    ignored_files = 0

    # Custom mime type to extension mapping
    custom_mappings = {
        'application/pdf': '.pdf',
        'application/zip': '.zip',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
        'application/msword': '.doc',
        'application/x-rar': '.rar',
        'application/epub+zip': '.epub',
        'text/xml': '.xml',
        'image/vnd.djvu': '.djvu',
        'application/x-mobipocket-ebook': '.mobi'
    }

    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    examined_files = len(files)

    for filename in files:
        filepath = os.path.join(directory, filename)

        # Ignore files with extensions already
        if os.path.splitext(filename)[1]:
            ignored_files += 1
            continue

        # Ignore shell scripts by checking magic number
        try:
            file_type = magic.from_file(filepath)
            if 'shell script' in file_type.lower():
                print(f"Ignoring shell script: {filename}")
                ignored_files += 1
                continue
        except Exception as e:
            print(f"Could not check file type for {filename}: {e}")
            ignored_files += 1
            continue

        try:
            mime = magic.from_file(filepath, mime=True)

            if mime in custom_mappings:
                extension = custom_mappings[mime]
            else:
                extension = mimetypes.guess_extension(mime)

            if extension == '.bin':
                if 'docx' in filename.lower():
                    extension = '.docx'
                elif 'pptx' in filename.lower():
                    extension = '.pptx'
                elif 'xlsx' in filename.lower():
                    extension = '.xlsx'
                elif 'epub' in filename.lower():
                    extension = '.epub'
                elif 'zip' in filename.lower():
                    extension = '.zip'
                elif 'doc' in filename.lower():
                    extension = '.doc'


            if extension:
                # mimetypes can guess '.jpe' for jpeg, so standardize to '.jpg'
                if extension == '.jpe':
                    extension = '.jpg'

                new_filepath = filepath + extension
                print(f"Renaming {filename} to {os.path.basename(new_filepath)}")
                os.rename(filepath, new_filepath)
                renamed_files += 1
            else:
                print(f"Could not determine extension for {filename} (mime: {mime})")
                ignored_files += 1

        except Exception as e:
            print(f"Error processing {filename}: {e}")
            ignored_files += 1

    print("\n--- Summary ---")
    print(f"Total files examined: {examined_files}")
    print(f"Total files renamed: {renamed_files}")
    print(f"Total files ignored: {ignored_files}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyzes files in a directory and adds the appropriate extension to files that don't have one."
    )
    parser.add_argument("directory", help="The path to the directory to analyze.")
    args = parser.parse_args()

    fix_file_extensions(args.directory)

if __name__ == "__main__":
    main()
