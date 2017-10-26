import sys

from proxy import exampleinterface

from turingarena.protocol.plumber.client import Implementation
from turingarena.protocol.proxy.python.library import ProxyEngine
from turingarena.sandbox.client import Algorithm

solution = Implementation(
    interface_name="exampleinterface",
    algorithm=Algorithm("solution"),
)

with solution.run() as connection:
    class Data:
        pass


    data = Data()
    data.N = 10
    data.M = 100
    data.A = [i * i for i in range(data.N)]

    proxy = ProxyEngine(interface=exampleinterface, instance=data, connection=connection)
    S = proxy.call("solve", [3], {"test": lambda a, b: a + b})

print("Answer:", S, file=sys.stderr)
