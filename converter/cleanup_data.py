from names import set_names

for i in range(len(set_names)):
    rm_command = f"rm -rf mnisq_cache/{set_names[i]}/qasm"
    print(rm_command)
    mv_command = f"mv converted/{set_names[i]}/qasm mnisq_cache/{set_names[i]}/"
    print(mv_command)
