---
name: drip-edu
description: "水滴智店教务管理智能体技能插件（适用于 Claude Code、OpenClaw 等智能体平台）。当用户提到 \"教务\"、\"课程表\"、\"排课\"、\"班级\"、\"教师\"、\"上课\"、\"课程\" 时使用。"
---

# 水滴智店 - 教务管理模块

涵盖课程表查询、班级管理、学员与教师查询。

## 认证方式

**Base URL:** `https://zd.drip.im/open/zd`

所有接口均为 **POST** 请求，`Content-Type: application/json`。

### 签名算法

```text
sign = sha256(sha256(body + client_secret + ts) + client_secret)
```

请求 URL 需附加 query 参数：`client_id`、`ts`（Unix 时间戳）、`sign`。

凭证从环境变量 `DRIP_CLIENT_ID` 和 `DRIP_CLIENT_SECRET` 读取。

## 二次确认规则

本模块全部为查询接口，可直接执行，无需二次确认。

## API 端点（6 个，全部为查询接口）

| 路径 | 说明 |
|------|------|
| `/edu/class/getSchedules` | 获取客户某时间段课程表 |
| `/edu/class/getNextSchedule` | 获取客户最近即将开始的课程 |
| `/edu/class/getDetails` | 获取指定日期门店排课列表（时间间隔 ≤ 7天） |
| `/edu/class/listClasses` | 获取班级列表（分页） |
| `/edu/student/listClassStudent` | 获取班级学员列表（分页） |
| `/edu/teacher/getByLocation` | 获取门店教师列表 |

**课程类型：** `1` 预约课, `2` 班级排课

## 错误码与处理指引

| 错误码 | 说明 | 处理方式 |
|--------|------|----------|
| `10003` | 无效请求 | 检查参数格式，不要重试 |
| `10004` | 服务器内部错误 | 可重试，间隔 3-5 秒 |
| `25001` | 暂无课程 | 告知用户该时间段无课程安排 |

## 详细参数参考

完整的请求参数和响应字段定义，参见 `references/openapi-spec.yaml`。
