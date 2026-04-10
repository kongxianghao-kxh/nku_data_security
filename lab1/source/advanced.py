from phe import paillier
from cryptography.fernet import Fernet
import random

##################### 1. 初始化设置与对称加密 (Client 端操作模拟)
print("=== 初始化阶段 ===")
original_messages = ["Secret_100", "Secret_200", "Secret_300", "Secret_400", "Secret_500", 
                     "Secret_600", "Secret_700", "Secret_800", "Secret_900", "Secret_1000"]
length = len(original_messages)

# 客户端生成对称密钥 k (AES)
symmetric_key = Fernet.generate_key()
cipher_suite = Fernet(symmetric_key)
print("客户端生成的对称密钥 k (保存于本地):", symmetric_key)

# 模拟：用对称密钥 k 加密所有明文，并转化为大整数存入服务器
server_stored_integers = []
for msg in original_messages:
    # 1. 对称加密，得到字节流 (bytes)
    encrypted_bytes = cipher_suite.encrypt(msg.encode('utf-8'))
    # 2. 将字节流转换为大整数 (int)，以便进行 Paillier 同态运算
    encrypted_int = int.from_bytes(encrypted_bytes, byteorder='big')
    server_stored_integers.append(encrypted_int)

print("服务器端存储的数据已全部转换为对称加密后的大整数。")

##################### 2. PIR 阶段：客户端生成公私钥及查询向量 (Client 端操作)
print("\n=== PIR 查询阶段 ===")
# 客户端生成 Paillier 公私钥
public_key, private_key = paillier.generate_paillier_keypair()

# 客户端随机选择一个要读取的位置
pos = random.randint(0, length - 1)
print(f"客户端想要获取的位置为: {pos} (预期明文: {original_messages[pos]})")

# 生成密文选择向量
select_list = []
enc_list = []
for i in range(length):
    select_list.append(i == pos) # 只有 pos 位置是 1(True)，其余是 0(False)
    enc_list.append(public_key.encrypt(select_list[i]))

##################### 3. PIR 阶段：服务器端进行同态掩码运算 (Server 端操作)
print("\n=== 服务器运算阶段 ===")
c = 0
for i in range(length):
    # server_stored_integers[i] 是对称加密后的大整数，enc_list[i] 是同态加密的 0 或 1
    # 标量乘法：整数 * 密文
    c = c + server_stored_integers[i] * enc_list[i] 

print("服务器运算完成，产生聚合密文 (返回给客户端)。")

##################### 4. 解析阶段：客户端进行解密 (Client 端操作)
print("\n=== 客户端解密阶段 ===")
# 第一步：用 Paillier 私钥解密，得到目标信息的对称密文（大整数形式）
m_int = private_key.decrypt(c)

# 第二步：将大整数转回字节流
# 计算所需的字节长度：(位长度 + 7) // 8
byte_length = (m_int.bit_length() + 7) // 8
m_bytes = m_int.to_bytes(byte_length, byteorder='big')

# 第三步：使用本地保存的对称密钥 k 进行 AES 解密
final_plaintext = cipher_suite.decrypt(m_bytes).decode('utf-8')

print("1. Paillier解密得到的大整数:", m_int)
print("2. 转换回的对称密文字节流:", m_bytes[:30], "... (截断显示)")
print("3. 最终通过对称密钥解密得到的明文:", final_plaintext)