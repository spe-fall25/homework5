import subprocess
import base64
import argparse

parser = argparse.ArgumentParser(description="Run telerun submit and save BMP outputs")
parser.add_argument("file", help="Source file to submit (e.g., code.cu or code.cpp)")
args = parser.parse_args()

source_file = args.file

# Run the job
result = subprocess.run(
    ["telerun", "submit", source_file],
    capture_output=True,
    text=True
)

log = result.stdout

# Print everything before the first FILE line
first_file_idx = log.find("FILE ")
if first_file_idx != -1:
    print(log[:first_file_idx].rstrip())
    base64_lines = log[first_file_idx:].splitlines()
else:
    base64_lines = []

i = 0
while i < len(base64_lines):
    line = base64_lines[i].strip()
    if line.startswith("FILE ") and line.endswith(".bmp BASE64:"):
        filename = line.split()[1]  # get filename
        i += 1
        if i < len(base64_lines):
            b64data = base64_lines[i].strip()  # only the next line
            if b64data:
                with open(filename, "wb") as f:
                    f.write(base64.b64decode(b64data))
                print(f"\nSaved output file: {filename}")
    i += 1