with open("../result files/539-561km_mean_error.txt") as input_file:
    with open("output_Scenario1.txt", "w") as output_file:
        for line in input_file:
            second_num = line.split()[1]
            output_file.write(second_num + ", ")
with open("../result files/525-535km_mean_error.txt") as input_file:
    with open("output_Scenario2.txt", "w") as output_file:
        for line in input_file:
            second_num = line.split()[1]
            output_file.write(second_num + ", ")