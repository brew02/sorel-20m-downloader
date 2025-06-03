import zlib
import os 

current_path = os.getcwd() + "\\bin"
for filename in os.listdir(current_path):
    filepath = os.path.join(current_path, filename)

    file_suffix = "_extracted"
    if(filename.endswith(file_suffix)):
        continue

    if os.path.isfile(filepath):
        try:
            with open(filepath, "br+") as file:
                content = file.read()
                decompressed = zlib.decompress(content)
                file.seek(0)
                file.write(decompressed)
                file.truncate()
                print(f"Extracted {filename}")
            
            os.rename(filepath, filepath + file_suffix)
        except Exception as e:
            print(f"Error reading {filename}: {e}")
