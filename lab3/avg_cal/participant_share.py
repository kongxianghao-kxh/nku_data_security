import ss_function as ss_f

p = 1000000007
user_id = int(input("请输入参与者 ID (1-3): "))
secret = int(input(f"请输入参与者 {user_id} 的私有数值: "))

# (2,3) 门限：多项式次数为 1 (t-1)
shares_x = [1, 2, 3]
f = ss_f.get_polynomial(secret, 1, p, str(user_id))

for i in range(1, 4):
    share_y = ss_f.count_polynomial(f, shares_x[i-1], p)
    with open(f'share_{user_id}_to_{i}.txt', 'w') as f_out:
        f_out.write(str(share_y))
print(f"参与者 {user_id} 的份额分发完毕。")
