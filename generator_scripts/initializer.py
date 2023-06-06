from generator_scripts.cifar_10_runner import cifar_10_run

from .env_initializer import env_initialize
from .mnist_runner import mnist_run
from .pbspro import qdel, qsub

print("Submitting the sleep job for dependency control...")
holding: str = qsub("dependency-hold", "sleep 100", 1)
print(f"Done. ID = {holding}")

env_id = env_initialize([holding])
mnist_run(env_id)
cifar_10_run(env_id)

print(f"Release the initial job {holding} and start job...")
qdel(holding)
print("Done.")
