import subprocess


cmd = ".\\bin\\windows\\kafka-server-start.bat F:\\kafka_2.12-3.5.2\\config\\server.properties"


# your kafka directory
working_directory = "F:\\kafka_2.12-3.5.2"


subprocess.run(cmd, shell=True, cwd=working_directory)
