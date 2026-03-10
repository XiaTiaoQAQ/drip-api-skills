# drip-openapi 项目指引

## 项目概述

水滴智店 (Drip Smart Store) OpenAPI 的 Claude Code Skill 插件。将水滴智店的开放接口封装为 AI 可调用的 skill。

## 安全规范

- **禁止硬编码** `client_id` 和 `client_secret`，必须从环境变量读取
- 环境变量名称：`DRIP_CLIENT_ID`、`DRIP_CLIENT_SECRET`
- 若用户未配置凭证，提示用户设置环境变量，不要使用占位值发送请求

## 签名算法

所有 API 请求需要双重 SHA256 签名：

```
sign = sha256(sha256(body + client_secret + ts) + client_secret)
```

- `body`：请求体 JSON 字符串
- `ts`：当前 Unix 时间戳（秒）
- 所有接口均为 POST 请求，Base URL: `https://zd.drip.im/open/zd`

## API 调用规范

- 所有金额单位为**分**（1元 = 100分）
- 分页接口 `size` 上限为 100
- `/customer/list` 使用游标分页（`startCursor` 格式：`createTime|id`）
- Webhook 回调不包含 `client_id` 参数

## 错误处理

- `10003`（无效请求）：检查参数格式
- `10004`（服务器错误）：可重试，建议间隔 3-5 秒
- 业务错误码（2xxxx）：向用户说明具体原因，不要重试

## Skill 结构

当前为单一 skill `drip-api`，覆盖全部 API 模块。详见 `skills/drip-api/SKILL.md`。
