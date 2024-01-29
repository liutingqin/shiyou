def replace_repeated_chars(s):
    # 创建一个新的字符串用于存储结果
    result = []

    # 遍历输入字符串的每个字符
    for i in range(len(s)):
        # 判断当前字符是否在前十个字符中出现过
        if s[i] in s[max(i-10, 0):i]:
            result.append('-')  # 如果出现过，添加 '-'
        else:
            result.append(s[i])  # 否则，添加原字符

    # 将结果列表转换成字符串并返回
    return ''.join(result)

# 测试代码
input_str1 = "abcdefaxc"
output_str1 = replace_repeated_chars(input_str1)
print("Input:", input_str1, "Output:", output_str1)

input_str2 = "abcaefbxcqwertba"
output_str2 = replace_repeated_chars(input_str2)
print("Input:", input_str2, "Output:", output_str2)
