import sys
from pathlib import Path
# pip.exe install -r ./requirements.txt -t ./lib

sys.path.append(str(Path()))
sys.path.append(str(Path().joinpath("lib")))
sys.path.append(str(Path().joinpath("plugin")))
