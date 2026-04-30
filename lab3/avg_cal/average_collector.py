import ss_function as ss_f

p = 1000000007
# 选取参与者 1 和 2 的聚合结果进行重构
ids = [1, 2]
collected_shares = []

for i in ids:
    with open(f'aggregated_share_{i}.txt', 'r') as f:
        collected_shares.append(int(f.read()))

# 1. 重构总和
total_sum = ss_f.restructure_polynomial(ids, collected_shares, 2, p)

# 2. 计算平均值
# 注意：在有限域内除法需用逆元，但实验演示通常直接在实数域除以 3 更直观
average = total_sum / 3

print(f"--- 实验结果 ---")
print(f"重构出的数据总和为: {total_sum}")
print(f"三人的数据平均值为: {average:.2f}")
