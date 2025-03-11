class DES:
    # 初始置换表
    IP = [58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17, 9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7]

    # 逆初始置换表
    IP_INV = [40, 8, 48, 16, 56, 24, 64, 32,
              39, 7, 47, 15, 55, 23, 63, 31,
              38, 6, 46, 14, 54, 22, 62, 30,
              37, 5, 45, 13, 53, 21, 61, 29,
              36, 4, 44, 12, 52, 20, 60, 28,
              35, 3, 43, 11, 51, 19, 59, 27,
              34, 2, 42, 10, 50, 18, 58, 26,
              33, 1, 41, 9, 49, 17, 57, 25]

    # 扩展置换表，将32位扩展为48位
    E = [32, 1, 2, 3, 4, 5,
         4, 5, 6, 7, 8, 9,
         8, 9, 10, 11, 12, 13,
         12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21,
         20, 21, 22, 23, 24, 25,
         24, 25, 26, 27, 28, 29,
         28, 29, 30, 31, 32, 1]

    # P盒置换
    P = [16, 7, 20, 21, 29, 12, 28, 17,
         1, 15, 23, 26, 5, 18, 31, 10,
         2, 8, 24, 14, 32, 27, 3, 9,
         19, 13, 30, 6, 22, 11, 4, 25]

    # S盒，每个S盒将6位输入映射为4位输出
    S_BOXES = [
        # S1
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
        ],
        # S2
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
        ],
        # S3
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
        ],
        # S4
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
        ],
        # S5
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
        ],
        # S6
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
        ],
        # S7
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
        ],
        # S8
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
        ]
    ]

    # 密钥置换表PC-1，用于密钥生成的第一步，去掉校验位
    PC1 = [57, 49, 41, 33, 25, 17, 9,
           1, 58, 50, 42, 34, 26, 18,
           10, 2, 59, 51, 43, 35, 27,
           19, 11, 3, 60, 52, 44, 36,
           63, 55, 47, 39, 31, 23, 15,
           7, 62, 54, 46, 38, 30, 22,
           14, 6, 61, 53, 45, 37, 29,
           21, 13, 5, 28, 20, 12, 4]

    # 密钥置换表PC-2，用于压缩56位密钥为48位子密钥
    PC2 = [14, 17, 11, 24, 1, 5,
           3, 28, 15, 6, 21, 10,
           23, 19, 12, 4, 26, 8,
           16, 7, 27, 20, 13, 2,
           41, 52, 31, 37, 47, 55,
           30, 40, 51, 45, 33, 48,
           44, 49, 39, 56, 34, 53,
           46, 42, 50, 36, 29, 32]

    # 每轮移位表
    SHIFT = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    def __init__(self):
        pass

    def permute(self, block, table):
        """根据给定的置换表对数据进行置换"""
        return [block[i-1] for i in table]

    def split(self, block):
        """将数据块分为左右两半"""
        return block[:len(block)//2], block[len(block)//2:]

    def left_shift(self, block, count):
        """循环左移位"""
        return block[count:] + block[:count]

    def xor(self, block1, block2):
        """异或操作"""
        return [b1 ^ b2 for b1, b2 in zip(block1, block2)]

    def string_to_bit_array(self, text):
        """将字符串转换为位数组"""
        result = []
        for char in text:
            bits = bin(ord(char))[2:].zfill(8)
            result.extend([int(bit) for bit in bits])
        return result

    def bit_array_to_string(self, array):
        """将位数组转换为字符串"""
        result = ""
        for i in range(0, len(array), 8):
            byte = array[i:i+8]
            result += chr(int(''.join([str(bit) for bit in byte]), 2))
        return result

    def hex_to_bit_array(self, hex_string):
        """将十六进制字符串转换为位数组"""
        bin_string = bin(int(hex_string, 16))[2:].zfill(len(hex_string) * 4)
        return [int(bit) for bit in bin_string]

    def bit_array_to_hex(self, array):
        """将位数组转换为十六进制字符串"""
        hex_string = hex(int(''.join([str(bit) for bit in array]), 2))[2:]
        return hex_string.zfill(len(array) // 4)

    def expand(self, block):
        """使用E表扩展32位数据块为48位"""
        return self.permute(block, self.E)

    def substitute(self, block):
        """S盒替代"""
        output = []
        for i in range(8):
            # 取6位作为当前S盒的输入
            chunk = block[i*6:(i+1)*6]
            # 计算行和列
            row = chunk[0] * 2 + chunk[5]
            col = chunk[1] * 8 + chunk[2] * 4 + chunk[3] * 2 + chunk[4]
            # 查S盒获得输出值
            val = self.S_BOXES[i][row][col]
            # 转换为4位二进制
            bin_val = bin(val)[2:].zfill(4)
            output.extend([int(bit) for bit in bin_val])
        return output

    def f_function(self, half_block, subkey):
        """DES的F函数"""
        # 扩展
        expanded = self.expand(half_block)
        # 与子密钥异或
        xored = self.xor(expanded, subkey)
        # S盒替代
        substituted = self.substitute(xored)
        # P盒置换
        return self.permute(substituted, self.P)

    def generate_subkeys(self, key, rounds=16):
        """生成子密钥"""
        # 将密钥转换为位数组
        if isinstance(key, str):
            if len(key) == 16:  # 假设是十六进制字符串
                key_bits = self.hex_to_bit_array(key)
            else:
                # 处理ASCII密钥
                key_bits = self.string_to_bit_array(key)
        else:
            key_bits = key
        
        # 确保密钥是64位
        if len(key_bits) < 64:
            key_bits.extend([0] * (64 - len(key_bits)))
        elif len(key_bits) > 64:
            key_bits = key_bits[:64]
            
        # PC1置换
        key = self.permute(key_bits, self.PC1)
        
        # 分割为左右两部分
        left, right = self.split(key)
        
        subkeys = []
        # 为每一轮生成子密钥
        for i in range(rounds):
            # 决定移位次数
            shift_count = self.SHIFT[i] if i < len(self.SHIFT) else 1
            
            # 循环左移
            left = self.left_shift(left, shift_count)
            right = self.left_shift(right, shift_count)
            
            # 合并左右两部分
            combined = left + right
            
            # PC2置换
            subkey = self.permute(combined, self.PC2)
            subkeys.append(subkey)
            
        return subkeys

    def encrypt_block(self, block, key, rounds=16):
        """加密单个64位块"""
        # 生成子密钥
        subkeys = self.generate_subkeys(key, rounds)
        
        # 初始置换
        block = self.permute(block, self.IP)
        
        # 分割为左右两部分
        left, right = self.split(block)
        
        # 进行rounds轮迭代
        for i in range(rounds):
            # 保存旧的右半部分
            old_right = right
            
            # 应用F函数并与左半部分异或
            right = self.xor(left, self.f_function(right, subkeys[i]))
            
            # 左边变为旧的右边
            left = old_right
        
        # 最后一轮后交换左右两半
        combined = right + left
        
        # 逆初始置换
        return self.permute(combined, self.IP_INV)

    def decrypt_block(self, block, key, rounds=16):
        """解密单个64位块"""
        # 生成子密钥，与加密相同但顺序相反
        subkeys = self.generate_subkeys(key, rounds)
        subkeys.reverse()  # 反转子密钥顺序
        
        # 初始置换
        block = self.permute(block, self.IP)
        
        # 分割为左右两部分
        left, right = self.split(block)
        
        # 进行rounds轮迭代
        for i in range(rounds):
            # 保存旧的右半部分
            old_right = right
            
            # 应用F函数并与左半部分异或
            right = self.xor(left, self.f_function(right, subkeys[i]))
            
            # 左边变为旧的右边
            left = old_right
        
        # 最后一轮后交换左右两半
        combined = right + left
        
        # 逆初始置换
        return self.permute(combined, self.IP_INV)

    def pad_data(self, data):
        """使数据长度为8的倍数，PKCS#5填充"""
        pad_len = 8 - (len(data) % 8)
        return data + bytes([pad_len]) * pad_len

    def unpad_data(self, data):
        """移除PKCS#5填充"""
        pad_len = data[-1]
        if pad_len > 8:
            return data  # 不是有效的填充
        for i in range(1, pad_len + 1):
            if data[-i] != pad_len:
                return data  # 不是有效的填充
        return data[:-pad_len]

    def encrypt(self, plaintext, key, rounds=16, mode="ECB", iv=None, counter=None):
        """加密数据，支持多种运行模式"""
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        
        # 填充数据使其长度为8的倍数
        padded_data = self.pad_data(plaintext)
        
        # 如果需要IV且未提供，则使用全零IV
        if mode != "ECB" and iv is None:
            iv = b'\x00' * 8
        
        # 确保IV是64位
        if mode != "ECB" and len(iv) != 8:
            if len(iv) < 8:
                iv = iv + b'\x00' * (8 - len(iv))
            else:
                iv = iv[:8]
        
        # 转换IV为位数组
        if mode != "ECB" and iv is not None:
            iv_bits = []
            for byte in iv:
                iv_bits.extend([int(bit) for bit in bin(byte)[2:].zfill(8)])
        
        ciphertext = b''
        
        # 根据不同模式处理加密
        if mode == "ECB":  # 电子密码本模式
            # ECB模式：各个块独立加密
            for i in range(0, len(padded_data), 8):
                block = padded_data[i:i+8]
                bit_block = []
                for byte in block:
                    bit_block.extend([int(bit) for bit in bin(byte)[2:].zfill(8)])
                
                encrypted_block = self.encrypt_block(bit_block, key, rounds)
                
                block_bytes = b''
                for j in range(0, len(encrypted_block), 8):
                    byte_bits = encrypted_block[j:j+8]
                    byte_val = int(''.join(str(bit) for bit in byte_bits), 2)
                    block_bytes += bytes([byte_val])
                
                ciphertext += block_bytes
        
        elif mode == "CBC":  # 密码块链接模式
            # CBC模式：当前块与前一个密文块异或后加密
            prev_cipher_bits = iv_bits
            
            for i in range(0, len(padded_data), 8):
                block = padded_data[i:i+8]
                bit_block = []
                for byte in block:
                    bit_block.extend([int(bit) for bit in bin(byte)[2:].zfill(8)])
                
                # 与前一密文块异或
                xored_block = self.xor(bit_block, prev_cipher_bits)
                
                # 加密
                encrypted_block = self.encrypt_block(xored_block, key, rounds)
                
                # 保存当前密文块用于下一轮
                prev_cipher_bits = encrypted_block
                
                block_bytes = b''
                for j in range(0, len(encrypted_block), 8):
                    byte_bits = encrypted_block[j:j+8]
                    byte_val = int(''.join(str(bit) for bit in byte_bits), 2)
                    block_bytes += bytes([byte_val])
                
                ciphertext += block_bytes
        
        elif mode == "CFB":  # 密码反馈模式
            # CFB模式：加密前一密文块然后与当前明文块异或
            feedback = iv_bits
            
            for i in range(0, len(padded_data), 8):
                block = padded_data[i:i+8]
                bit_block = []
                for byte in block:
                    bit_block.extend([int(bit) for bit in bin(byte)[2:].zfill(8)])
                
                # 加密反馈值
                encrypted_feedback = self.encrypt_block(feedback, key, rounds)
                
                # 与当前明文异或得到密文
                cipher_block = self.xor(encrypted_feedback, bit_block)
                
                # 更新反馈值为当前密文
                feedback = cipher_block
                
                block_bytes = b''
                for j in range(0, len(cipher_block), 8):
                    byte_bits = cipher_block[j:j+8]
                    byte_val = int(''.join(str(bit) for bit in byte_bits), 2)
                    block_bytes += bytes([byte_val])
                
                ciphertext += block_bytes
        
        elif mode == "OFB":  # 输出反馈模式
            # OFB模式：加密前一输出块与当前明文异或
            feedback = iv_bits
            
            for i in range(0, len(padded_data), 8):
                block = padded_data[i:i+8]
                bit_block = []
                for byte in block:
                    bit_block.extend([int(bit) for bit in bin(byte)[2:].zfill(8)])
                
                # 加密反馈值
                encrypted_feedback = self.encrypt_block(feedback, key, rounds)
                
                # 更新反馈值
                feedback = encrypted_feedback
                
                # 与当前明文异或得到密文
                cipher_block = self.xor(encrypted_feedback, bit_block)
                
                block_bytes = b''
                for j in range(0, len(cipher_block), 8):
                    byte_bits = cipher_block[j:j+8]
                    byte_val = int(''.join(str(bit) for bit in byte_bits), 2)
                    block_bytes += bytes([byte_val])
                
                ciphertext += block_bytes
        
        elif mode == "CTR":  # 计数器模式
            # CTR模式：加密计数器与明文块异或
            if counter is None:
                # 默认从0开始
                counter_value = 0
            else:
                counter_value = counter
                
            for i in range(0, len(padded_data), 8):
                block = padded_data[i:i+8]
                bit_block = []
                for byte in block:
                    bit_block.extend([int(bit) for bit in bin(byte)[2:].zfill(8)])
                
                # 创建计数器块
                counter_bytes = counter_value.to_bytes(8, byteorder='big')
                counter_bits = []
                for byte in counter_bytes:
                    counter_bits.extend([int(bit) for bit in bin(byte)[2:].zfill(8)])
                
                # 加密计数器
                encrypted_counter = self.encrypt_block(counter_bits, key, rounds)
                
                # 与当前明文异或得到密文
                cipher_block = self.xor(encrypted_counter, bit_block)
                
                block_bytes = b''
                for j in range(0, len(cipher_block), 8):
                    byte_bits = cipher_block[j:j+8]
                    byte_val = int(''.join(str(bit) for bit in byte_bits), 2)
                    block_bytes += bytes([byte_val])
                
                ciphertext += block_bytes
                counter_value += 1
            
        return ciphertext
    
    def decrypt(self, ciphertext, key, rounds=16, mode="ECB", iv=None, counter=None):
        """解密数据，支持多种运行模式"""
        # 如果需要IV且未提供，则使用全零IV
        if mode != "ECB" and iv is None:
            iv = b'\x00' * 8
        
        # 确保IV是64位
        if mode != "ECB" and len(iv) != 8:
            if len(iv) < 8:
                iv = iv + b'\x00' * (8 - len(iv))
            else:
                iv = iv[:8]
        
        # 转换IV为位数组
        if mode != "ECB" and iv is not None:
            iv_bits = []
            for byte in iv:
                iv_bits.extend([int(bit) for bit in bin(byte)[2:].zfill(8)])
                
        plaintext = b''
        
        # 根据不同模式处理解密
        if mode == "ECB":  # 电子密码本模式
            # ECB模式：各个块独立解密
            for i in range(0, len(ciphertext), 8):
                block = ciphertext[i:i+8]
                bit_block = []
                for byte in block:
                    bit_block.extend([int(bit) for bit in bin(byte)[2:].zfill(8)])
                
                decrypted_block = self.decrypt_block(bit_block, key, rounds)
                
                block_bytes = b''
                for j in range(0, len(decrypted_block), 8):
                    byte_bits = decrypted_block[j:j+8]
                    byte_val = int(''.join(str(bit) for bit in byte_bits), 2)
                    block_bytes += bytes([byte_val])
                
                plaintext += block_bytes
        
        elif mode == "CBC":  # 密码块链接模式
            # CBC模式：解密后与前一密文块异或
            prev_cipher_bits = iv_bits
            
            for i in range(0, len(ciphertext), 8):
                block = ciphertext[i:i+8]
                bit_block = []
                for byte in block:
                    bit_block.extend([int(bit) for bit in bin(byte)[2:].zfill(8)])
                
                # 保存当前密文用于异或
                current_cipher = bit_block.copy()
                
                # 解密
                decrypted_block = self.decrypt_block(bit_block, key, rounds)
                
                # 与前一密文块异或得到明文
                plain_block = self.xor(decrypted_block, prev_cipher_bits)
                
                # 更新前一密文块
                prev_cipher_bits = current_cipher
                
                block_bytes = b''
                for j in range(0, len(plain_block), 8):
                    byte_bits = plain_block[j:j+8]
                    byte_val = int(''.join(str(bit) for bit in byte_bits), 2)
                    block_bytes += bytes([byte_val])
                
                plaintext += block_bytes
        
        elif mode == "CFB":  # 密码反馈模式
            # CFB模式：加密前一密文块然后与当前密文异或
            feedback = iv_bits
            
            for i in range(0, len(ciphertext), 8):
                block = ciphertext[i:i+8]
                bit_block = []
                for byte in block:
                    bit_block.extend([int(bit) for bit in bin(byte)[2:].zfill(8)])
                
                # 加密反馈值
                encrypted_feedback = self.encrypt_block(feedback, key, rounds)
                
                # 与当前密文异或得到明文
                plain_block = self.xor(encrypted_feedback, bit_block)
                
                # 更新反馈值为当前密文
                feedback = bit_block
                
                block_bytes = b''
                for j in range(0, len(plain_block), 8):
                    byte_bits = plain_block[j+j+8]
                    byte_val = int(''.join(str(bit) for bit in byte_bits), 2)
                    block_bytes += bytes([byte_val])
                
                plaintext += block_bytes
        
        elif mode == "OFB":  # 输出反馈模式
            # OFB模式：加密前一输出块与当前密文异或
            feedback = iv_bits
            
            for i in range(0, len(ciphertext), 8):
                block = ciphertext[i:i+8]
                bit_block = []
                for byte in block:
                    bit_block.extend([int(bit) for bit in bin(byte)[2:].zfill(8)])
                
                # 加密反馈值
                encrypted_feedback = self.encrypt_block(feedback, key, rounds)
                
                # 更新反馈值
                feedback = encrypted_feedback
                
                # 与当前密文异或得到明文
                plain_block = self.xor(encrypted_feedback, bit_block)
                
                block_bytes = b''
                for j in range(0, len(plain_block), 8):
                    byte_bits = plain_block[j:j+8]
                    byte_val = int(''.join(str(bit) for bit in byte_bits), 2)
                    block_bytes += bytes([byte_val])
                
                plaintext += block_bytes
        
        elif mode == "CTR":  # 计数器模式
            # CTR模式：加密计数器与密文块异或
            if counter is None:
                # 默认从0开始
                counter_value = 0
            else:
                counter_value = counter
                
            for i in range(0, len(ciphertext), 8):
                block = ciphertext[i:i+8]
                bit_block = []
                for byte in block:
                    bit_block.extend([int(bit) for bit in bin(byte)[2:].zfill(8)])
                
                # 创建计数器块
                counter_bytes = counter_value.to_bytes(8, byteorder='big')
                counter_bits = []
                for byte in counter_bytes:
                    counter_bits.extend([int(bit) for bit in bin(byte)[2:].zfill(8)])
                
                # 加密计数器
                encrypted_counter = self.encrypt_block(counter_bits, key, rounds)
                
                # 与当前密文异或得到明文
                plain_block = self.xor(encrypted_counter, bit_block)
                
                block_bytes = b''
                for j in range(0, len(plain_block), 8):
                    byte_bits = plain_block[j:j+8]
                    byte_val = int(''.join(str(bit) for bit in byte_bits), 2)
                    block_bytes += bytes([byte_val])
                
                plaintext += block_bytes
                counter_value += 1
                
        return self.unpad_data(plaintext)
