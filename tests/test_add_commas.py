
def rev_string(str_: str):
    """"""
    rev_str = ""
    l, r = 0, len(str_)-1
    while r >= 0:
        rev_str += str_[r]
        r -= 1
    return rev_str

def add_commas(num: str):
    """ add commas to large numbers to make them more readable """
    new_num = ""
    rev_num = num[::-1]
    if len(num) < 4: return num

    for idx, char in enumerate(rev_num):
        if idx % 3 == 0 and idx != 0:
            new_num = char + "," + new_num
        else:
            new_num = char + new_num

    return new_num



a = 61763832
b = 101593300
c = 123
d = 12345678910
# 61763832 --> 61,763,832
# 101593300 --> 101,593,300


new_a = add_commas(str(a))
new_b = add_commas(str(b))
new_c = add_commas(str(c))
new_d = add_commas(str(d))

print(f"Original: {a}")
print(f"Original: {b}")
print(f"Original: {c}")
print(f"Original: {d}")
print(f"formatted: {new_a}")
print(f"formatted: {new_b}")
print(f"formatted: {new_c}")
print(f"formatted: {new_d}")