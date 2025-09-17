from cosmic_language import CosmicLanguageCodec
import re

class EthereumCosmicConverter:
    """
    以太坊EVM地址转宇宙语转换器
    支持将以太坊地址转换为宇宙语编码
    使用十六进制字符直接映射到二进制编码的方式
    """
    
    def __init__(self):
        self.codec = CosmicLanguageCodec()
        
        # 十六进制字符到二进制的直接映射
        self.hex_to_binary = {
            '0': '0000', '1': '0001', '2': '0010', '3': '0011',
            '4': '0100', '5': '0101', '6': '0110', '7': '0111',
            '8': '1000', '9': '1001', 'a': '1010', 'b': '1011',
            'c': '1100', 'd': '1101', 'e': '1110', 'f': '1111'
        }
        
        # 二进制到十六进制的反向映射
        self.binary_to_hex = {v: k for k, v in self.hex_to_binary.items()}
    
    def is_valid_ethereum_address(self, address):
        """
        验证EVM地址格式
        """
        # 检查是否以0x开头且长度为42字符
        if not address.startswith('0x') or len(address) != 42:
            return False
        
        # 检查是否只包含有效的十六进制字符
        hex_part = address[2:]
        return re.match(r'^[0-9a-fA-F]{40}$', hex_part) is not None
    
    def normalize_address(self, address):
        """
        标准化EVM地址（转为小写）
        """
        if not self.is_valid_ethereum_address(address):
            raise ValueError(f"无效的EVM地址: {address}")
        
        return address.lower()
    
    def address_to_cosmic_direct(self, address):
        """
        将以太坊地址直接转换为宇宙语（十六进制字符直接映射）
        每个十六进制字符对应一个宇宙语字符
        """
        try:
            # 验证并标准化地址
            normalized_address = self.normalize_address(address)
            
            # 提取十六进制部分（去掉0x前缀）
            hex_part = normalized_address[2:]
            
            # 直接将每个十六进制字符转换为宇宙语字符
            cosmic_chars = []
            for hex_char in hex_part:
                binary = self.hex_to_binary[hex_char]
                cosmic_char = self.codec.binary_to_block[binary]
                cosmic_chars.append(cosmic_char)
            
            cosmic_encoded = ''.join(cosmic_chars)
            
            return {
                'original_address': address,
                'normalized_address': normalized_address,
                'hex_part': hex_part,
                'cosmic_encoding': cosmic_encoded,
                'encoding_length': len(cosmic_encoded),
                'method': 'direct_hex_mapping'
            }
        
        except Exception as e:
            return {
                'error': str(e),
                'original_address': address
            }
    
    def address_to_cosmic(self, address):
        """
        将以太坊地址转换为宇宙语（使用原始文本编码方式）
        """
        try:
            # 验证并标准化地址
            normalized_address = self.normalize_address(address)
            
            # 使用宇宙语编码器编码地址
            cosmic_encoded = self.codec.encode_text(normalized_address)
            
            return {
                'original_address': address,
                'normalized_address': normalized_address,
                'cosmic_encoding': cosmic_encoded,
                'encoding_length': len(cosmic_encoded),
                'method': 'text_encoding'
            }
        
        except Exception as e:
            return {
                'error': str(e),
                'original_address': address
            }
    
    def cosmic_to_address_direct(self, cosmic_text):
        """
        将宇宙语直接解码为以太坊地址（十六进制字符直接映射）
        """
        try:
            # 检查长度是否正确（40个十六进制字符对应40个宇宙语字符）
            if len(cosmic_text) != 40:
                return {
                    'cosmic_text': cosmic_text,
                    'error': f'宇宙语长度错误，期望40个字符，实际{len(cosmic_text)}个字符',
                    'is_valid': False
                }
            
            # 将每个宇宙语字符转换回十六进制字符
            hex_chars = []
            for cosmic_char in cosmic_text:
                if cosmic_char in self.codec.block_chars:
                    binary = self.codec.block_chars[cosmic_char]
                    hex_char = self.binary_to_hex[binary]
                    hex_chars.append(hex_char)
                else:
                    return {
                        'cosmic_text': cosmic_text,
                        'error': f'无效的宇宙语字符: {cosmic_char}',
                        'is_valid': False
                    }
            
            # 组装完整的以太坊地址
            hex_part = ''.join(hex_chars)
            decoded_address = '0x' + hex_part
            
            # 验证解码结果是否为有效的以太坊地址
            if self.is_valid_ethereum_address(decoded_address):
                return {
                    'cosmic_text': cosmic_text,
                    'hex_part': hex_part,
                    'decoded_address': decoded_address,
                    'is_valid': True,
                    'method': 'direct_hex_mapping'
                }
            else:
                return {
                    'cosmic_text': cosmic_text,
                    'decoded_address': decoded_address,
                    'is_valid': False,
                    'error': '解码结果不是有效的以太坊地址'
                }
        
        except Exception as e:
            return {
                'cosmic_text': cosmic_text,
                'error': str(e),
                'is_valid': False
            }
    
    def cosmic_to_address(self, cosmic_text):
        """
        将宇宙语解码为EVM地址（使用原始文本解码方式）
        """
        try:
            # 解码宇宙语
            decoded_text = self.codec.decode_text(cosmic_text)
            
            # 验证解码结果是否为有效的EVM地址
            if self.is_valid_ethereum_address(decoded_text):
                return {
                    'cosmic_text': cosmic_text,
                    'decoded_address': decoded_text,
                    'is_valid': True,
                    'method': 'text_encoding'
                }
            else:
                return {
                    'cosmic_text': cosmic_text,
                    'decoded_text': decoded_text,
                    'is_valid': False,
                    'error': '解码结果不是有效的EVM地址'
                }
        
        except Exception as e:
            return {
                'cosmic_text': cosmic_text,
                'error': str(e),
                'is_valid': False
            }
    
    def batch_convert_addresses(self, addresses):
        """
        批量转换EVM地址为宇宙语
        """
        results = []
        for address in addresses:
            result = self.address_to_cosmic(address)
            results.append(result)
        return results
    
    def get_address_analysis(self, address):
        """
        分析EVM地址的字符组成
        """
        try:
            normalized_address = self.normalize_address(address)
            analysis = self.codec.analyze_text(normalized_address)
            
            return {
                'address': normalized_address,
                'character_analysis': analysis,
                'total_characters': len(normalized_address)
            }
        
        except Exception as e:
            return {
                'address': address,
                'error': str(e)
            }

# 示例使用
if __name__ == "__main__":
    converter = EthereumCosmicConverter()
    
    # 测试地址
    test_addresses = [
        "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6",
        "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
        "0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed"
    ]
    
    print("=== 以太坊地址转宇宙语示例（直接十六进制映射）===")
    
    for i, address in enumerate(test_addresses):
        print(f"\n--- 测试地址 {i+1} ---")
        print(f"原始地址: {address}")
        
        # 使用直接映射方式
        result_direct = converter.address_to_cosmic_direct(address)
        
        if 'error' in result_direct:
            print(f"直接映射错误: {result_direct['error']}")
        else:
            print(f"标准化地址: {result_direct['normalized_address']}")
            print(f"十六进制部分: {result_direct['hex_part']}")
            print(f"宇宙语编码: {result_direct['cosmic_encoding']}")
            print(f"编码长度: {result_direct['encoding_length']} 字符")
            print(f"编码方式: {result_direct['method']}")
            
            # 显示每个字符的映射
            print("字符映射详情:")
            hex_part = result_direct['hex_part']
            cosmic_part = result_direct['cosmic_encoding']
            for j, (hex_char, cosmic_char) in enumerate(zip(hex_part, cosmic_part)):
                binary = converter.hex_to_binary[hex_char]
                print(f"  位置{j+1:2d}: {hex_char} → {binary} → {cosmic_char}")
            
            # 验证解码
            decode_result = converter.cosmic_to_address_direct(result_direct['cosmic_encoding'])
            if decode_result['is_valid']:
                print(f"解码验证: ✓ 成功 - {decode_result['decoded_address']}")
            else:
                print(f"解码验证: ✗ 失败 - {decode_result.get('error', '未知错误')}")
    
    print("\n=== 对比两种编码方式 ===")
    test_address = test_addresses[0]
    print(f"测试地址: {test_address}")
    
    # 直接映射方式
    result_direct = converter.address_to_cosmic_direct(test_address)
    print(f"\n直接映射方式:")
    print(f"  宇宙语: {result_direct['cosmic_encoding']}")
    print(f"  长度: {result_direct['encoding_length']} 字符")
    
    # 原始文本编码方式
    result_text = converter.address_to_cosmic(test_address)
    print(f"\n文本编码方式:")
    print(f"  宇宙语: {result_text['cosmic_encoding']}")
    print(f"  长度: {result_text['encoding_length']} 字符")
    
    print("\n=== 地址字符分析示例 ===")
    analysis = converter.get_address_analysis(test_addresses[0])
    if 'error' not in analysis:
        print(f"地址: {analysis['address']}")
        print(f"总字符数: {analysis['total_characters']}")
        print(f"字符类型分析: {analysis['character_analysis']}")