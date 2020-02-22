import os
json_file_addr="C:\\Users\\sk45472\Documents\\Unreal Projects\\JsonParsing18Version\\Content\\JsonFiles\\Backup.json"

def main():
    setup_file_path = os.path.realpath(__file__)
    setup_dir_path = os.path.dirname(setup_file_path)
    if not(setup_dir_path in os.sys.path):
        os.sys.path.append(setup_dir_path)
    print(os.sys.path)

if __name__== "__main__":
      main()
