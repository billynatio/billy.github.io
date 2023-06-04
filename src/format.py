with open("kodevch.txt", "r") as file:
    lines = file.readlines()

formatted_lines = []
for line in lines:
    line = line.strip()
    formatted_line = "{}#{}#{}#{}#{}\n".format(line, kode_voucher, nama_voucher, filtered_lines, harga, waktu)
    formatted_lines.append(formatted_line)

with open("kodevch.txt", "w") as file:
    file.writelines(formatted_lines)
