import os
import subprocess
import sys

from mnisq.internal.dataset import (
    load_raw_dataset,
    merge_dataset,
    save_raw_dataset,
)

file_name = sys.argv[1]
count = int(sys.argv[2])

result = {}
for x in range(count):
    part_items = load_raw_dataset(f"data/{file_name}_{x+1}")
    if x == 0:
        result = part_items
    else:
        result = merge_dataset(result, part_items)

save_raw_dataset(result, f"data/{file_name}")
subprocess.run(
    f"cd data && zip -r ../outcome/{os.path.basename(file_name)}.zip {file_name}",
    shell=True,
)
