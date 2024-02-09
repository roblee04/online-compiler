import subprocess

def compile_c_program():
    try:
        # Replace 'your_program.c' with the name of your C source file
        # Replace 'your_program' with the desired name of the executable
        subprocess.run(['clang', 'your_program.c', '-o', 'your_program'], check=True)
        print("C program compiled successfully.")
    except subprocess.CalledProcessError as e:
        print("Error: Compilation failed with return code:", e.returncode)

compile_c_program()
