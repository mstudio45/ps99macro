import os, time

try:
    import matplotlib
    import shutil
except:
    os.system("pip install matplotlib")
    import matplotlib
    import shutil

def setup():
    configdir = matplotlib.get_configdir()

    if not os.path.exists(f"{configdir}\stylelib"):
        os.mkdir(f"{configdir}\stylelib")

    if os.path.exists(f"{configdir}\stylelib\\rose-pine.mplstyle"):
        print(f"rose-pine.mplstyle already exists in {configdir}\stylelib\\")
        exit()

    if not os.path.exists("rose-pine-matplotlib"):
        os.system("git clone https://github.com/h4pZ/rose-pine-matplotlib.git")

    for i in os.listdir("rose-pine-matplotlib\\themes"):
        if i.endswith(".mplstyle"):
            print(f"Copying {i} to {configdir}\stylelib\\")
            shutil.copy(f"rose-pine-matplotlib\\themes\\{i}", f"{configdir}\stylelib")

    print(f"Installed rose-pine.mplstyle to {configdir}\stylelib\\")
    print(f"You can delete rose-pine-matplotlib where the main program is located.")
setup()