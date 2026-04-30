p = 1000000007
user_id = int(input("请输入参与者 ID (1-3) 进行聚合: "))

local_sum = 0
for i in range(1, 4):
    with open(f'share_{i}_to_{user_id}.txt', 'r') as f:
        local_sum = (local_sum + int(f.read())) % p

with open(f'aggregated_share_{user_id}.txt', 'w') as f_out:
    f_out.write(str(local_sum))
print(f"参与者 {user_id} 本地份额聚合完毕。")
