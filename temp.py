nama_voucher = "iv43"
kode_voucher = "iv43" 
harga = "99000"
digipos = "12"
jumlah_voucher = "13" 
waktu = "03-06-2023"

with open("kodevch.txt", "r") as file:
    lines = file.readlines()

formatted_lines = []
for line in lines:
    line = line.strip()
    formatted_line = "{}#{}#{}#{}#{}\n".format(
        kode_voucher, nama_voucher, line, harga, waktu)
    formatted_lines.append(formatted_line)

with open("kodevch.txt", "w") as file:
    file.writelines(formatted_lines)



# mendapat jumlah baris
with open("kodevch.txt", "r") as file:
    lines = file.readlines()

num_lines = len(lines)
print("Jumlah baris dalam file: ", num_lines)
