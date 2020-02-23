import os
json_file_addr="C:\\Users\\Behzad-PC\\mavbench_stuff\\env-gen-ue4-my\\Content\\JsonFiles\\EnvGenConfig.json"
host_ip_addr = "10.243.49.33" # radhika host ip

def main():
    setup_file_path = os.path.realpath(__file__)
    setup_dir_path = os.path.dirname(setup_file_path)
    if not(setup_dir_path in os.sys.path):
        os.sys.path.append(setup_dir_path)
    os.sys.path.append("..")
    print(os.sys.path)

main()
