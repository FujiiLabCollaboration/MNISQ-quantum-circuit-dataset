from names import set_names

for i in range(len(set_names)):
    mv_command = f"mv {set_names[i]} base_{set_names[i]}"
    print(mv_command)
