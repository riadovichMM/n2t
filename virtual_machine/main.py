from virtual_machine import virtual_machine

def main():
    vm = virtual_machine()
    vm.get_files_codes()
    vm.process()
    vm.write_asm_in_file()
    

main()