import subprocess


def run_ml_cli(files_directory: str,
               output_directory: str,
               url: str,
               ml_cli_template: str,
               process_path: str = "/home/ml-cli/MlCli",
               run_path: str = "/home/ml-cli",
               tasks_path: str = "/home/tasks.json"):
    ml_cli_template = ml_cli_template.replace("${files_directory}$", files_directory)
    ml_cli_template = ml_cli_template.replace("${output_directory}$", output_directory)
    ml_cli_template = ml_cli_template.replace("${url}$", url)
    print("ml_cli_template")
    print(ml_cli_template)

    with open(tasks_path, 'w') as file:
        file.write(ml_cli_template)

    # r'C:\github\ml-cli\src\Ml.Cli\bin\Debug\net6.0\Ml.Cli.exe'
    args = [process_path, "--base-path", "/", '--tasks-path', tasks_path]
    with subprocess.Popen(args,
                          cwd=run_path,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT) as process:
        for line in process.stdout:
            print(line.decode('utf8'))

