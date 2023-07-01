import subprocess
import  tkinter as tk
from tkinter import filedialog
from PIL import Image
from datetime import datetime
import time
import sys
import match_and_log as log


# ******************************************
#            Important Notes
# ******************************************
# Enter folder's location FIRST
# Example: cd  C:\Users\luigi\Desktop\LPR_Pipeline
# Change folder path to the same location
#
# If running for this first time, run the following commands before:
# 1) pip install -r requirements.txt
# 2) python setup.py develop --no_cuda_ext


# Absolute folder path (Change accordingly)
folder_path = 'C:/Users/luigi/Desktop/LPR_Pipeline'

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

# Automatic Pipeline
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

# Saves current date and time
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

# *************************************
# ***** Preprocessing: Deblurring *****
# *************************************
st = time.time()
string_to_edit = 'python ./basicsr/demo.py -opt options/test/REDS/NAFNet-width64.yml --input_path image_path --output_path ./Output_Images/TEST_img.jpg'
command = string_to_edit.replace('image_path', file_path)
results = subprocess.run(command, cwd=folder_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#output = results.stdout.decode("utf-8") # For debugging purposes
#print(output)


# ********************************
# *********** OpenALPR ***********
# ********************************
alpr_path = folder_path + "/alpr.exe"
string_to_edit = f'{alpr_path} -c us deblurred_image_path --clock'
command = string_to_edit.replace('deblurred_image_path', "./Output_Images/TEST_img.jpg")
results = subprocess.run(command, cwd=folder_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output = results.stdout.decode("utf-8")
lines = output.splitlines()

# Gets most confident license plate identified
identified = False
first_result = ""
for line in lines:
    if line.startswith(' '):
        first_result = line.split()[1]
        identified = True
        break
    else:
        # No camera ID or Zone specification yet
        first_result = "No plate identified (Sensor Triggered)"

display_string = first_result + " " + formatted_datetime + "\n"
print("\n\n\nIdentified License plate: ", display_string)

zone = 1 # DELETE LATER

if(identified):
    detection_info = {
        "plate": first_result,
        "zone": zone,
        "lastSeen": formatted_datetime
    }   
    log.match_and_log(detection_info)
else:
    log_file = open("log.txt", "a")
    log_file.write(display_string)
    log_file.close()


# get the end and execution time
et = time.time()
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')