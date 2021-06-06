import cx_Freeze

executables = [cx_Freeze.Executable("spaceinvader.py")]

cx_Freeze.setup(
    name="Space Invader",
    options={"build_exe": {"packages":["pygame"], "include_files":["Images", "Sound"]}},
    executables = executables

    )