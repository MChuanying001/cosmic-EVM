# 宇宙语编码器 - 以太坊EVM地址版

根据[宇宙语主程序](https://github.com/0x3fffff/cosmic-language)改编而来

一个支持将文本和以太坊EVM地址转换为宇宙语（块字符）编码的Python工具库。

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
- Python 3.6+
- 无需额外依赖包

## 快速开始

### 1. 基础文本编码

```python
from cosmic_language import CosmicLanguageCodec

# 创建编解码器实例
codec = CosmicLanguageCodec()

# 编码文本
text = "Hello 世界!"
encoded = codec.encode_text(text)
print(f"原文: {text}")
print(f"宇宙语: {encoded}")

# 解码文本
decoded = codec.decode_text(encoded)
print(f"解码结果: {decoded}")
```

### 2. 以太坊地址转换

```python
from ethereum_cosmic import EthereumCosmicConverter

# 创建以太坊转换器实例
converter = EthereumCosmicConverter()

# 转换以太坊地址
address = "0xab5801a7d398351b8be11c439e05c5b3259aec9b"
result = converter.address_to_cosmic(address)

if 'error' not in result:
    print(f"原始地址: {result['original_address']}")
    print(f"宇宙语编码: {result['cosmic_encoding']}")
    
    # 验证解码
    decode_result = converter.cosmic_to_address(result['cosmic_encoding'])
    if decode_result['is_valid']:
        print("✓ 解码验证成功")
else:
    print(f"错误: {result['error']}")
```

### 3. 运行示例程序

```bash
# 运行基础示例
python cosmic.py

# 运行以太坊地址示例
python ethereum_cosmic.py
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
