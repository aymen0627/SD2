import subprocess
import  tkinter as tk
from tkinter import filedialog
from PIL import Image
from datetime import datetime
import time
import sys


# ******************************************
#            Important Notes
# ******************************************
# Enter folder's location FIRST
# Example: cd  C:\Users\luigi\Desktop\LPR_Pipeline
#
# If running for this first time, run the following commands before:
# 1) pip install -r requirements.txt
# 2) python setup.py develop --no_cuda_ext

# Argument Parsing
n = len(sys.argv)
print("Total arguments passed:", n)

# Argument length checking
if(n == 1):
    print("No path (argument) selected. Bye.")
    sys.exit()

if(n > 2):
    print("Too many arguments. Bye.")
    sys.exit()
 
# Arguments passed
print("\nName of Python script:", sys.argv[0])
 
print("\nArguments passed: ", sys.argv[1])

# Argument testing purposes only
#sys.exit()


# Semi-automatic Pipeline
# User selects image from folder
root = tk.Tk()
root.withdraw()
# file_path = filedialog.askopenfilename()
file_path = sys.argv[1]
try:
    im = Image.open(file_path)
except FileNotFoundError:
    print("FileNotFoundError. Bye!")
    sys.exit()
except TypeError:
    print("TypeError. Bye!")
    sys.exit()
except ValueError:
    print("ValueError. Bye!")
    sys.exit()
    
#print(file_path) # For debugging purposes
#im.show() # Display image before deblurring


# ***** Preprocessing: Deblurring *****
st = time.time()
string_to_edit = 'python ./basicsr/demo.py -opt options/test/REDS/NAFNet-width64.yml --input_path image_path --output_path ./Output_Images/TEST_img.jpg'
command = string_to_edit.replace('image_path', file_path)
results = subprocess.run(command, cwd='C:/Users/luigi/Desktop/LPR_Pipeline', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#output = results.stdout.decode("utf-8") # For debugging purposes
#print(output)

# get the end time
et = time.time()
# get the execution time
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')


# ***** OpenALPR *****
st = time.time()

string_to_edit = 'C:/Users/luigi/Desktop/LPR_Pipeline/alpr.exe -c us deblurred_image_path --clock'
command = string_to_edit.replace('deblurred_image_path', "./Output_Images/TEST_img.jpg")
results = subprocess.run(command, cwd='C:/Users/luigi/Desktop/LPR_Pipeline', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output = results.stdout.decode("utf-8")

# get the end time
et = time.time()
# get the execution time
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')

lines = output.splitlines()

# Gets most confident license plate identified
first_result = ""
for line in lines:
    if line.startswith(' '):
        first_result = line.split()[1]
        break
    else:
        # No camera ID or Zone specification yet
        first_result = "No plate identified (Sensor Triggered)"


current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

display_string = first_result + " @ " + formatted_datetime + "\n"
print("\n\n\nIdentified License plate: ", display_string)

log_file = open("log.txt", "a")
log_file.write(display_string)
log_file.close()