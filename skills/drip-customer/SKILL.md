---
name: drip-customer
description: "当用户提到 \"客户\"、\"customer\"、\"会员\"、\"会员卡\"、\"注册\"、\"手机号查询\"、\"学员\"、\"孩子\" 时使用此 skill。"
---

# 水滴智店 - 客户与会员管理模块

涵盖客户信息管理（查询、注册、属性更新、学员管理）和会员卡查询。

## 认证方式

**Base URL:** `https://zd.drip.im/open/zd`

所有接口均为 **POST** 请求，`Content-Type: application/json`。

### 签名算法

```
sign = sha256(sha256(body + client_secret + ts) + client_secret)
```

请求 URL 需附加 query 参数：`client_id`、`ts`（Unix 时间戳）、`sign`。

凭证从环境变量 `DRIP_CLIENT_ID` 和 `DRIP_CLIENT_SECRET` 读取。

## 客户 API 端点（8 个）

| 路径 | 说明 |
|------|------|
| `/customer/getByMobile` | 根据手机号获取客户信息 |
| `/customer/registerByMobile` | 根据手机号注册新客户 |
| `/customer/getExtProps` | 获取所有自定义属性列表 |
| `/customer/list` | 分批获取客户列表（游标分页） |
| `/customer/updateProps` | 更新客户属性（内置属性 + 自定义属性） |
| `/edu/student/getByCustomer` | 获取客户关联的所有学员 |
| `/edu/student/create` | 创建孩子 |
| `/edu/student/getChildren` | 获取客户关联的所有孩子 |

**客户可更新的内置属性：** `realName`, `remarkName`, `gender`, `birth`, `province`, `city`, `district`, `adress`, `nickName`, `avatar`

**游标分页说明：** `/customer/list` 使用 `startCursor` 参数，格式为 `createTime|id`

## 会员 API 端点（1 个）

| 路径 | 说明 |
|------|------|
| `/card/getByMobile` | 根据手机号获取会员卡信息（等级、成长值、有效期） |

## 错误码与处理指引

| 错误码 | 说明 | 处理方式 |
|--------|------|----------|
| `10003` | 无效请求 | 检查参数格式，不要重试 |
| `10004` | 服务器内部错误 | 可重试，间隔 3-5 秒 |
| `23001` | 客户不存在 | 提示用户核实手机号或客户 ID |
| `23003` | 属性不存在或不支持更新 | 检查属性字段名是否正确 |
| `23004` | 属性值格式错误 | 检查属性值的数据类型和格式 |
| `25002` | 姓名已存在 | 告知用户学员姓名重复 |
| `25003` | 信息同步失败 | 可重试，失败后报告 |
| `21001` | 客户信息不存在 | 提示用户核实客户信息 |
| `21002` | 会员信息不存在 | 告知用户未开通会员 |
| `21003` | 会员卡信息不存在 | 告知用户会员卡不存在 |

## 详细参数参考

完整的请求参数和响应字段定义，参见 `references/openapi-spec.yaml`。
