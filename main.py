from tkinter import *
from sympy import symbols, expand, collect

ws = Tk()
ws.title('S-AES')
ws.geometry('225x250')
ws["bg"] = "gray80"

Label(ws, bg='gray81', text="Введите фразу: ").place(x=50, y=30)
decimal_number_ = Entry(ws)
decimal_number_.place(x=50, y=50)

Label(ws, bg='gray81', text="Введите ключ: ").place(x=50, y=80)
decimal_number_key_ = Entry(ws)
decimal_number_key_.place(x=50, y=100)

def input_number():
    decimal_number = decimal_number_.get()
    return decimal_number

def input_key():
    decimal_number_key = decimal_number_key_.get()
    return decimal_number_key

dict = {
    '0000': '1001', '0001': '1110', '0010': '0101', '0011': '0001',
    '0100': '1000', '0101': '1011', '0110': '1101', '0111': '1010',
    '1000': '0110', '1001': '0111', '1010': '1111', '1011': '0011',
    '1100': '1100', '1101': '0100', '1110': '0000', '1111': '0010'
}

table = {
    '0': '0000', '1': '0001', '2': '0010', '3': '0011',
    '4': '0100', '5': '0101', '6': '0110', '7': '0111',
    '8': '1000', '9': '1001', 'a': '1010', 'b': '1011',
    'c': '1100', 'd': '1101', 'e': '1110', 'f': '1111'
}

reverse_table = {
    '0000': '0', '0001': '1', '0010': '2' ,'0011': '3',
    '0100': '4', '0101': '5', '0110': '6', '0111': '7',
    '1000': '8', '1001': '9', '1010': 'a', '1011': 'b',
    '1100': 'c', '1101': 'd', '1110': 'e', '1111': 'f'
}

def summ_with_key(data, key):
    result = ''
    for i in range(0, 4):
        if data[i] == key[i]:
            result += "0"
        else:
            result += "1"
    return result

def binary_addition(data1, data2):
    result = ''
    for i in range(0, 5):
        if data1[i] == data2[i]:
            result += "0"
        else:
            result += "1"
    return result

def contains_x(input_str):
    parts = input_str.split()
    return "x" in parts

def check(temp):
    str = ''

    if 'x**4' in temp:
        str = str + '1'
    else:
        str = str + '0'

    if 'x**3' in temp:
        str = str + '1'
    else:
        str = str + '0'

    if 'x**2' in temp:
        str = str + '1'
    else:
        str = str + '0'

    if contains_x(temp):
        str = str + '1'
    else:
        str = str + '0'

    if '1' in temp:
        str = str + '1'
    else:
        str = str + '0'

    return str

def del_elements(data):
    x = symbols('x')

    coeff_dict = collect(data, x).as_coefficients_dict()
    filtered_coeff_dict = {term: coeff for term, coeff in coeff_dict.items() if not (coeff.has(2))}
    filtered_polynomial = sum(term * coeff for term, coeff in filtered_coeff_dict.items())

    return filtered_polynomial

def mix_colums(const1, data1, const2, data2):
    string1 = f"{const1} ({data1})"
    string2 = f"{const2} ({data2})"

    if (data1 == ''):
        summ1 = '00000'
    else:
        expanded_polynomial = expand(str(string1))
        temp1 = del_elements(expanded_polynomial)
        temp1_bin = check(str(temp1))
        if 'x**4' in str(temp1):
            summ1 = binary_addition(temp1_bin, '10011')
        else:
            summ1 = temp1_bin

    if (data2 == ''):
        summ2 = '00000'
    else:
        # упростили многочлен
        expanded_polynomial2 = expand(str(string2))
        # удалили двойные элементы
        temp2 = del_elements(expanded_polynomial2)
        temp2_bin = check(str(temp2))
        if 'x**4' in str(temp2):
            summ2 = binary_addition(temp2_bin, '10011')
        else:
            summ2 = temp2_bin

    answer = binary_addition(summ1, summ2)
    return answer

def Answer():
    data = input_number()
    key = input_key()

    data1 = data[0]
    data2 = data[2]
    data3 = data[1]
    data4 = data[3]

    k001 = key[0]  # строка 1.1
    k101 = key[2]  # строка 1.2
    k011 = key[1]  # строка 2.1
    k111 = key[3]  # строка 2.2

    k002 = summ_with_key(dict[table[k111][:2] + table[k111][2:]], table[k001])
    k102 = summ_with_key(summ_with_key(dict[table[k011][:2] + table[k011][2:]], table[k101]), '0001')
    k012 = summ_with_key(k002, table[k011])
    k112 = summ_with_key(k102, table[k111])

    k003 = summ_with_key(dict[k112], k002)
    k103 = summ_with_key(summ_with_key(dict[k012], k102), '0010')
    k013 = summ_with_key(k003, k012)
    k113 = summ_with_key(k103, k112)

    # Сложение исходных данных с ключем
    summ1 = summ_with_key(table[data1], table[k001])
    summ2 = summ_with_key(table[data2], table[k101])
    summ3 = summ_with_key(table[data3], table[k011])
    summ4 = summ_with_key(table[data4], table[k111])

    # Замена полубайтов
    halfbyte1 = dict[summ1[:2] + summ1[2:]]
    halfbyte2 = dict[summ2[:2] + summ2[2:]]
    halfbyte3 = dict[summ3[:2] + summ3[2:]]
    halfbyte4 = dict[summ4[:2] + summ4[2:]]

    # Сдвиг
    temp = halfbyte2
    halfbyte2 = halfbyte4
    halfbyte4 = temp

    desired_bits = 4  # Желаемое количество бит
    s00_bin = bin(int(reverse_table[halfbyte1], 16))[2:].zfill(desired_bits)
    s10_bin = bin(int(reverse_table[halfbyte2], 16))[2:].zfill(desired_bits)
    s01_bin = bin(int(reverse_table[halfbyte3], 16))[2:].zfill(desired_bits)
    s11_bin = bin(int(reverse_table[halfbyte4], 16))[2:].zfill(desired_bits)

    const1 = '(x + 1) * '
    const2 = 'x * '

    halfbytes = [s00_bin, s10_bin, s01_bin, s11_bin]
    result_transform = []

    for bytes in halfbytes:
        test = ''

        if bytes[0] == '1':
            test = test + "x**3"
        if bytes[1] == '1':
            test = test + " + x**   2"
        if bytes[2] == '1':
            test = test + ' + x'
        if bytes[3] == '1':
            test = test + ' + 1'

        result_transform.append(test.lstrip(' +'))

    s001 = mix_colums(const1, result_transform[0], const2, result_transform[1])[1:]
    s101 = mix_colums(const2, result_transform[0], const1, result_transform[1])[1:]
    s011 = mix_colums(const1, result_transform[2], const2, result_transform[3])[1:]
    s111 = mix_colums(const2, result_transform[2], const1, result_transform[3])[1:]

    summ_mix1 = summ_with_key(s001, k002)
    summ_mix2 = summ_with_key(s101, k102)
    summ_mix3 = summ_with_key(s011, k012)
    summ_mix4 = summ_with_key(s111, k112)

    halfbyte1_2 = dict[summ_mix1[:2] + summ_mix1[2:]]
    halfbyte2_2 = dict[summ_mix2[:2] + summ_mix2[2:]]
    halfbyte3_2 = dict[summ_mix3[:2] + summ_mix3[2:]]
    halfbyte4_2 = dict[summ_mix4[:2] + summ_mix4[2:]]

    temp = halfbyte2_2
    halfbyte2_2 = halfbyte4_2
    halfbyte4_2 = temp

    last_summ1 = summ_with_key(k003, halfbyte1_2)
    last_summ2 = summ_with_key(k103, halfbyte2_2)
    last_summ3 = summ_with_key(k013, halfbyte3_2)
    last_summ4 = summ_with_key(k113, halfbyte4_2)

    print("Answer:", reverse_table[last_summ1], reverse_table[last_summ3], reverse_table[last_summ2], reverse_table[last_summ4])
    answer = str(reverse_table[last_summ1] + reverse_table[last_summ3] + reverse_table[last_summ2] + reverse_table[last_summ4])
    Label(ws, bg='gray81', text=f'Результат: {answer}').place(x=65, y=180)
btn = Button(ws, text="Зашифровать", command=Answer)
btn.place(x=65, y=135)
ws.mainloop()
