import json

def write_output_to_file(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=None)

    ## read the file contents and modify them (each NV on 1 line)
    with open(path, "r") as f:
        contents = f.read()
        # Replace newlines with ',\n' except for lines that contain a list value
        contents = contents.replace("], ", "],\n\t")
        contents = contents.replace("{", "{\n\t")
        contents = contents.replace("]}", "]\n}")
        # print(contents)

    ## overwrite the file with the modified contents
    with open(path, "w") as f:
        f.write(contents)