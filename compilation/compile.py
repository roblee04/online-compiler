import subprocess
import sys
def compile_c_program():

    file = sys.argv[1]
    with open(file) as f: string = f.read()

    try:
        # Replace 'your_program.c' with the name of your C source file
        # Replace 'your_program' with the desired name of the executable
        subprocess.run(['clang', file, '-o', 'compiled_c'], check=True)
        print("C program compiled successfully.")
    except subprocess.CalledProcessError as e:
        print("Error: Compilation failed with return code:", e.returncode)

compile_c_program()
