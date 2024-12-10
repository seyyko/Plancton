start = 800
actual = start
string_start = ""
string_end = ""
open, close = "{", "}"

def is_full_second(n:int) -> bool:
    last_two_char = str(n)[-2:]
    return last_two_char == "60"

def int_to_strArray(n:int) -> str:
    s = str(n)
    if len(s) > 3:
        return "".join((s[0], s[1])), "".join((s[2], s[3]))
    return "".join(("0", s[0])), "".join((s[1], s[2]))

while actual <= 1930:
    if is_full_second(actual):
        actual += 40
    hour, min = int_to_strArray(actual)
    string_start += f""".g-start-{hour}h{min}{open}
    grid-row-start: {actual-800};
{close}
"""
    string_end += f""".g-end-{hour}h{min}{open}
    grid-row-end: {actual-800};
{close}
"""
    actual += 15

print(string_start)