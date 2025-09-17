# 宇宙语编码器 - 以太坊EVM地址版

根据[宇宙语主程序](https://github.com/0x3fffff/cosmic-language)改编而来
主程序作者：0x3fffff

一个支持将文本和以太坊EVM地址转换为宇宙语（块字符）编码的Python工具库。


## 更新内容

v1.1：新增直接转换模式（出现40个宇宙语字符）

## 项目简介

本项目实现了一个通用的宇宙语编码系统，使用特殊的块字符（如 ▀▄█▌▐ 等）来编码文本内容。项目特别增加了对以太坊EVM地址的支持，可以将以太坊地址安全地转换为宇宙语编码。

## 功能特性

### 核心功能
- 📝 **文本编码**: 支持所有GB18030字符的编码，包括汉字、英文、数字、符号等
- 🔄 **双向转换**: 支持编码和解码操作
- 🛡️ **校验机制**: 每4个内容字符配1个校验字符，确保数据完整性
- 📊 **字符分析**: 提供详细的字符类型分析功能

### 以太坊专用功能
- 🔗 **EVM地址支持**: 专门针对以太坊地址的编码转换
- ✅ **地址验证**: 自动验证以太坊地址格式的有效性
- 🔄 **批量处理**: 支持批量转换多个以太坊地址
- 📈 **详细分析**: 提供地址字符组成的详细分析


## 安装要求
- [宇宙语主程序](https://github.com/0x3fffff/cosmic-language)
- Python 3.8+
- 无需额外依赖包

## 快速开始
以太坊地址转换（v1.0旧版）

```python
from cosmic_language import CosmicLanguageCodec
import re

class EthereumCosmicConverter:
    """
    以太坊EVM地址转宇宙语转换器
    支持将EVM地址转换为宇宙语编码
    """
    
    def __init__(self):
        self.codec = CosmicLanguageCodec()
    
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
    
    def address_to_cosmic(self, address):
        """
        将EVM地址转换为宇宙语
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
                'encoding_length': len(cosmic_encoded)
            }
        
        except Exception as e:
            return {
                'error': str(e),
                'original_address': address
            }
    
    def cosmic_to_address(self, cosmic_text):
        """
        将宇宙语解码为EVM地址
        """
        try:
            # 解码宇宙语
            decoded_text = self.codec.decode_text(cosmic_text)
            
            # 验证解码结果是否为有效的EVM地址
            if self.is_valid_ethereum_address(decoded_text):
                return {
                    'cosmic_text': cosmic_text,
                    'decoded_address': decoded_text,
                    'is_valid': True
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
    print('EVM地址转宇宙语')
    print('版本号v1.0')
    # 测试地址
    test_addresses = [
        "0xab5801a7d398351b8be11c439e05c5b3259aec9b"#, #填入要转换的EVM地址
        #"0x0xab5801a7d398351b8be11c439e05c5b3259aec9b"
    ]
    
    print("=== EVM地址转宇宙语示例 ===")
    
    for address in test_addresses:
        print(f"\n原始地址: {address}")
        result = converter.address_to_cosmic(address)
        
        if 'error' in result:
            print(f"错误: {result['error']}")
        else:
            print(f"标准化地址: {result['normalized_address']}")
            print(f"宇宙语编码: {result['cosmic_encoding']}")
            print(f"编码长度: {result['encoding_length']} 字符")
            
            # 验证解码
            decode_result = converter.cosmic_to_address(result['cosmic_encoding'])
            if decode_result['is_valid']:
                print(f"解码验证: ✓ 成功")
            else:
                print(f"解码验证: ✗ 失败 - {decode_result.get('error', '未知错误')}")
    
    print("\n=== 地址字符分析示例 ===")
    analysis = converter.get_address_analysis(test_addresses[0])
    if 'error' not in analysis:
        print(f"地址: {analysis['address']}")
        print(f"总字符数: {analysis['total_characters']}")
        print(f"字符类型分析: {analysis['character_analysis']}")
```

## 宇宙语字符映射

本项目使用16个特殊的块字符来表示4位二进制数据：

| 字符 | 二进制 | 字符 | 二进制 | 字符 | 二进制 | 字符 | 二进制 |
|------|--------|------|--------|------|--------|------|---------|
| ▓    | 0000   | ▗    | 0001   | ▖    | 0010   | ▄    | 0011    |
| ▝    | 0100   | ▐    | 0101   | ▞    | 0110   | ▟    | 0111    |
| ▘    | 1000   | ▚    | 1001   | ▌    | 1010   | ▙    | 1011    |
| ▀    | 1100   | ▜    | 1101   | ▛    | 1110   | █    | 1111    |

## 编码原理

### 字符编码流程
1. **字符分析**: 根据GB18030编码获取字符的字节表示
2. **类型识别**: 识别字符类型（单字节、双字节、三字节、四字节）
3. **二进制转换**: 将字节数据转换为二进制字符串
4. **分组编码**: 每4位二进制对应一个块字符
5. **校验生成**: 每4个内容字符生成1个校验字符

### 以太坊地址特殊处理
- **格式验证**: 检查0x前缀和40位十六进制字符
- **标准化**: 转换为小写格式确保一致性
- **完整性**: 保持地址的完整42字符长度

## API 参考

### CosmicLanguageCodec 类

#### 主要方法
- `encode_text(text)`: 编码文本为宇宙语
- `decode_text(encoded_text)`: 解码宇宙语为文本
- `encode_char(char)`: 编码单个字符
- `analyze_text(text)`: 分析文本字符组成

### EthereumCosmicConverter 类

#### 主要方法
- `address_to_cosmic(address)`: 以太坊地址转宇宙语
- `cosmic_to_address(cosmic_text)`: 宇宙语转以太坊地址
- `is_valid_ethereum_address(address)`: 验证地址格式
- `batch_convert_addresses(addresses)`: 批量转换地址
- `get_address_analysis(address)`: 分析地址字符组成

## 使用场景

### 数据存储
- 将敏感的以太坊地址以宇宙语形式存储
- 文本数据的特殊编码存储

### 数据传输
- 在不支持特殊字符的系统中传输编码数据
- 避免地址格式检测的数据传输

### 艺术创作
- 将文本转换为视觉艺术形式
- 创建基于块字符的图案设计

### 教育演示
- 演示编码解码原理
- 区块链地址格式教学

## 注意事项

1. **字符支持**: 主要支持GB18030字符集，部分特殊字符可能使用UTF-8备选编码
2. **地址格式**: 仅支持标准以太坊地址格式（0x + 40位十六进制）
3. **数据完整性**: 编码后的数据包含校验信息，解码时会自动验证
4. **性能考虑**: 长文本编码会产生较长的宇宙语字符串

## 错误处理

项目包含完善的错误处理机制：
- 无效字符编码时返回错误标记
- 以太坊地址格式验证
- 解码时的校验失败处理
- 详细的错误信息返回

## ⭐️ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=MChuanying001/cosmic-EVM&type=Date)](https://www.star-history.com/#MChuanying001/cosmic-EVM&Date)

---

**如果你觉得这个项目有趣，请给它一个 ⭐️！**

---

*我们一起将宇宙语发扬光大，让Ai可以真正翻译方块字符！* 🚀✨
