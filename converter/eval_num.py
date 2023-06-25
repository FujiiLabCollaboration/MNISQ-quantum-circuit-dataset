import re
from math import pi

def conv_str(line):
    pi_mul_pattern = re.compile(r'pi\*([+-]?\d+(?:\.\d*)?|.\d+)')
    pi_div_pattern = re.compile(r'pi/([+-]?\d+(?:\.\d*)?|.\d+)')

    line = pi_mul_pattern.sub(lambda match : str(pi*float(match.group(1))), line)
    line = pi_div_pattern.sub(lambda match : str(pi/float(match.group(1))), line)

    mul_pattern = re.compile(r'-\d\*([+-]?\d+(?:\.\d*)?|.\d+)')
    div_pattern = re.compile(r'-\d/([+-]?\d+(?:\.\d*)?|.\d+)')
    line = mul_pattern.sub(lambda match : str(eval(match.group(0))), line)
    line = div_pattern.sub(lambda match : str(eval(match.group(0))), line)

    mul_pattern = re.compile(r'\d\*([+-]?\d+(?:\.\d*)?|.\d+)')
    div_pattern = re.compile(r'\d/([+-]?\d+(?:\.\d*)?|.\d+)')
    line = mul_pattern.sub(lambda match : str(eval(match.group(0))), line)
    line = div_pattern.sub(lambda match : str(eval(match.group(0))), line)

    return line

q = "u(2.322995378992683,-3.141592653589793,1.5707963267948966) q[2];"
s = conv_str(q)
print("before:", q)
print("after :", s)

q = "u(2.322995378992683,-1*-3.141592653589793,1.5707963267948966) q[2];"
s = conv_str(q)
print("before:", q)
print("after :", s)

q = "u(2.322995378992683,2*-3.141592653589793,1.5707963267948966) q[2];"
s = conv_str(q)
print("before:", q)
print("after :", s)
