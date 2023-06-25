from names import set_names

BATCH_SIZE = 5000
TRAIN_DATA_SIZE = 60000
TEST_DATA_SIZE = 10000

# python c2.py data/test_mnist_784_f80 converted/test_mnist_784_f80/qasm 0 10

for i in range(len(set_names)):
    if 'train' in set_names[i]:
        batch_count = int(TRAIN_DATA_SIZE / BATCH_SIZE)
    else:
        batch_count = int(TEST_DATA_SIZE / BATCH_SIZE)

    for j in range(batch_count):
        job_str = f"python c2.py data/{set_names[i]} converted/{set_names[i]}/qasm {j*BATCH_SIZE} {(j+1) * BATCH_SIZE} &"
        print(job_str)
