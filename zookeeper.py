import subprocess


cmd = "zkServer"

# your kafka directory
working_directory = "F:\kafka_2.12-3.5.2"


subprocess.run(cmd, shell=True, cwd=working_directory)
