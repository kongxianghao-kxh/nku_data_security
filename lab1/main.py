from phe import paillier
import numpy as np

class PIRServer:
    def __init__(self, messages):
        # 服务器存储的明文消息列表
        self.messages = messages
        self.m = len(messages)

    def process_query(self, encrypted_vector):
        """
        核心逻辑：计算 Σ(E(v_j) * m_j)
        在 Paillier 中，密文的幂运算等同于明文乘法：E(v)^m = E(v * m)
        密文的乘法运算等同于明文加法：E(a) * E(b) = E(a + b)
        """
        if len(encrypted_vector) != self.m:
            raise ValueError("Query vector length mismatch")

        # 初始化结果为 E(0)
        # 这里的实现技巧：第一个元素的密文幂运算作为起点
        result = encrypted_vector[0] * self.messages[0]
        
        for i in range(1, self.m):
            # 同态累加：result = result + (E(v_i) * m_i)
            # 注意：phe 库重载了 * 和 ** 运算符
            temp = encrypted_vector[i] * self.messages[i]
            result = result + temp
            
        return result

class PIRClient:
    def __init__(self, m):
        # 生成公钥和私钥
        self.public_key, self.private_key = paillier.generate_paillier_keypair()
        self.m = m

    def create_query(self, target_index):
        """创建一个加密的 One-Hot 向量"""
        query_vector = []
        for i in range(self.m):
            val = 1 if i == target_index else 0
            # 对 0 或 1 进行加密
            query_vector.append(self.public_key.encrypt(val))
        return query_vector

    def decrypt_response(self, encrypted_res):
        """解密服务器返回的结果"""
        return self.private_key.decrypt(encrypted_res)

# --- 实验演示 ---
if __name__ == "__main__":
    # 1. 模拟服务器数据
    raw_data = [101, 202, 303, 404, 505]
    server = PIRServer(raw_data)
    print(f"服务器消息列表: {raw_data}")

    # 2. 客户端准备
    client = PIRClient(m=len(raw_data))
    target = 2  # 假设客户端想获取索引为 2 的消息 (即 303)
    print(f"客户端目标索引: {target}")

    # 3. 客户端生成查询并发送给服务器
    query = client.create_query(target)

    # 4. 服务器计算（服务器无法看到 query 里的明文，因为是加密的）
    response = server.process_query(query)

    # 5. 客户端解密
    retrieved_msg = client.decrypt_response(response)
    print(f"客户端检索到的结果: {retrieved_msg}")

    assert retrieved_msg == raw_data[target]
    print("验证成功：隐私信息获取完成。")