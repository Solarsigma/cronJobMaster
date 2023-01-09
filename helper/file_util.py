from . import input_util

def getScriptFile():
    execFile = ''
    while True:
        execFile = os.path.join("./scripts/", input_util.get_sanitized_input(prompt="Enter script file name: ", type_=str))
        if os.path.exists(execFile):
            os.chmod(execFile, 0o775)
            return execFile
        print("File does not exist. Please try again.")
        print("List of files in 'scripts' folder:")
        for file in os.listdir("./scripts/"):
            if os.path.isfile(os.path.join("./scripts", file)):
                print("\t", file)
