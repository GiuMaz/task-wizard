import os
import subprocess
import sys


def logged(fun):
    def logged_fun(self, *args):
        print("SUPERVISOR: Called function", fun.__name__, *args, file=sys.stderr)
        ret = fun(self, *args)
        print("SUPERVISOR: Function", fun.__name__, *args, "returned", ret, file=sys.stderr)
        return ret
    return logged_fun


class AlgorithmProcess:

    def __init__(self, supervisor, id, algorithm_name):
        self.supervisor = supervisor
        self.id = id
        self.algorithm_name = algorithm_name
        self.executable_path = os.path.join(self.supervisor.task_run_dir, "algorithms", algorithm_name, "algorithm")

    def start(self):
        self.downward_pipe = os.mkfifo(
            os.path.join(self.supervisor.task_run_dir, "algorithm_downward.%d.pipe" % (self.id,)))
        self.upward_pipe = os.mkfifo(
            os.path.join(self.supervisor.task_run_dir, "algorithm_upward.%d.pipe" % (self.id,)))

        self.process = subprocess.Popen(
            [self.executable_path],
            universal_newlines=True,
            stdin=open(self.downward_pipe, "r"),
            stdout=open(self.upward_pipe, "w"),
            bufsize=1
        )


class ReadFile:

    def __init__(self, supervisor, id, file_name):
        self.supervisor = supervisor
        self.id = id
        self.file_name = file_name
        self.file_path = os.path.join(self.supervisor.task_run_dir, "read_files", file_name, "data.txt")

    def open(self):
        os.symlink(
            os.path.join("..", self.file_path),
            os.path.join(self.supervisor.driver_sandbox_dir, "read_file.%d.txt" % (self.id,)))


class Supervisor:

    def __init__(self, task_run_dir):
        self.algorithm_processes = {}
        self.read_files = {}
        self._next_id = 0

        self.task_run_dir = task_run_dir
        self.driver_sandbox_dir = os.path.join(task_run_dir, "driver_sandbox")
        self.driver_path = os.path.join(self.task_run_dir, "driver", "driver")

    def next_id(self):
        self._next_id += 1
        return self._next_id

    @logged
    def algorithm_start(self, algorithm_name):
        id = self.next_id()
        process = AlgorithmProcess(self, id, algorithm_name)
        self.algorithm_processes[id] = process

        process.start()

        return id

    @logged
    def algorithm_status(self, algorithm_id):
        pass

    @logged
    def algorithm_kill(self, algorithm_id):
        pass

    @logged
    def read_file_open(self, file_name):
        id = self.next_id()
        read_file = ReadFile(self, id, file_name)
        self.read_files[id] = read_file

        read_file.open()

        return id

    @logged
    def read_file_close(self, file_id):
        pass

    def on_command(self, command, arg):
        commands = {
            "algorithm_start": str,
            "algorithm_status": int,
            "algorithm_kill": int,
            "read_file_open": str,
            "read_file_close": str
        }

        if command not in commands:
            raise ValueError("Unrecognized command: " + command)

        arg_type = commands[command]
        return getattr(self, command)(arg_type(arg))

    def run(self):
        os.mkdir(self.driver_sandbox_dir)

        driver = subprocess.Popen(
            [self.driver_path],
            cwd=self.driver_sandbox_dir,
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            bufsize=1  # line buffered
        )

        while True:
            line = driver.stdout.readline()
            if not line:
                print("SUPERVISOR: control pipe closed, terminating.")
                break
            print("SUPERVISOR: received line", list(line))
            command, arg = line.rstrip().split(" ", 2)
            result = self.on_command(command, arg)
            print(result, file=driver.stdin)