# Model 层反向工程（从 Hotfix 代码推导数据定义）

> 当 Hotfix 代码已存在但 Model Component 文件缺失时使用。
> 用 subagent 批量读取 → 提取字段引用 → 输出结构化清单。

---

## 子代理 Prompt 模板

```
从服务端 Hotfix 代码中提取 {ComponentName} 的所有字段引用，反向推导 Model 层需要的字段。

读取这些文件：
- {path}/PlayerXxxComponentSystem.cs
- {path}/PlayerXxxComponentNetLogic.cs
- {path}/PlayerXxxComponentEvent.cs (if exists)
- {path}/docs/{模块}/{模块}-服务器.md (设计文档)

对每个 Component，提取：
1. 数据载体类名（如 NerveData）及其字段（类型+名称）
   — 注意：简单模块可能不需要独立的 Data 类，直接用 Dictionary
2. Component 的字典字段（如 Dictionary<int, short> m_dicTier）
3. Component 的标量字段（如 int m_nDrawTimeTotal）
4. IsCan+Do 方法签名列表（参数+返回类型）
5. 任何 BsonIgnore / BsonDictionaryOptions 等特性
6. Component 类声明信息（[ComponentOf(...)], 父类, 接口）

输出一个结构化的字段清单，用于生成 Model 层的 .cs 文件。
最终给出可以直接复制使用的完整类定义。
```

## 关键检查点

- **字典是否存在**：遍历所有 self.m_dicXxx 引用
- **标量是否存在**：遍历所有 self.m_nXxx / self.m_lXxx / self.m_szXxx 引用
- **数据载体类**：检查是否有 new XxxData() 或 .m_nField 等嵌套字段访问
- **Bson 特性**：字典字段必须有 [BsonDictionaryOptions(DictionaryRepresentation.ArrayOfArrays)]
- **接口匹配**：服务端 Model 必须有 ICacheNode；客户端 Model 不需要

## 常见模式

| 模块复杂度 | Model 结构 | 示例 |
|:---|:---|:---|
| 简单 | 1-2个字典 或 1个标量 | Nerve: Dictionary×2; Raffle: int×1 |
| 中等 | 字典 + 数据载体类 | DNA: Dictionary<int, DNAData> |
| 复杂 | 多字典 + 多数据载体类 + 标量 | Shop: 多子结构 |
