---
name: drip-api
description: "水滴智店全量开放接口智能体技能插件（适用于 Claude Code、OpenClaw 等智能体平台）。当用户提到 \"call Drip API\"、\"use 水滴 API\"、\"integrate with 水滴智店\"、\"查水滴数据\"、\"水滴智店最近\"、\"manage bookings via Drip\"、\"manage tcard\"、\"query customers in Drip\"、\"manage 次卡\"、\"manage 预约\"、\"manage 会员\"、\"manage 积分\"、\"manage 教务\"、\"manage 订单\"、\"manage 场地\" 或任何涉及水滴智店 (Drip Smart Store) 开放 API 的任务时使用。"
---

# 水滴智店开放接口 (Drip Smart Store OpenAPI)

水滴智店是线下商户智能门店 SaaS 平台，提供预约、次卡、会员、教务、积分、订单、场地、客流等模块的开放 API。本技能适用于 Claude Code、OpenClaw 等智能体平台。

## 二次确认规则

对于会产生副作用的写操作接口（如创建订单、核销、退款、发放、转卡、注册、更新属性、修改积分等），**必须先向用户展示即将执行的操作详情，获得用户明确确认后才能执行**。除非用户明确要求"直接执行"或"不需要确认"。

查询类接口（getById、getByIds、filter、list、get 等）可直接执行，无需确认。

确认流程：

1. 组装好请求参数后，先向用户展示操作摘要（接口、关键参数、预期效果）
2. 等待用户确认（如："确认执行"、"好的"、"执行吧"）
3. 用户确认后才发送请求

## 认证方式

**Base URL:** `https://zd.drip.im/open/zd`

所有接口均为 **POST** 请求，`Content-Type: application/json`。

### 请求参数

每个请求 URL 需要附加以下 query 参数：

| 参数 | 类型 | 说明 |
|------|------|------|
| `client_id` | string | 平台分配的客户端标识 |
| `ts` | integer | 当前 Unix 时间戳（秒） |
| `sign` | string | 请求签名 |

### 签名算法

```text
sign = sha256(sha256(body + client_secret + ts) + client_secret)
```

- `body` 为请求体的 JSON 字符串
- `client_secret` 由平台分配
- `ts` 为 Unix 时间戳
- 使用 SHA256 双重哈希

### 请求示例

```bash
# 1. 准备参数
CLIENT_ID="your_client_id"
CLIENT_SECRET="your_client_secret"
TS=$(date +%s)
BODY='{"mobile":"13800138000"}'

# 2. 计算签名
INNER=$(echo -n "${BODY}${CLIENT_SECRET}${TS}" \
  | sha256sum | awk '{print $1}')
SIGN=$(echo -n "${INNER}${CLIENT_SECRET}" \
  | sha256sum | awk '{print $1}')

# 3. 发送请求
ENDPOINT="https://zd.drip.im/open/zd/customer/getByMobile"
curl -X POST \
  "${ENDPOINT}?client_id=${CLIENT_ID}&ts=${TS}&sign=${SIGN}" \
  -H "Content-Type: application/json" \
  -d "${BODY}"
```

> **注意：** Webhook 回调请求不包含 `client_id` 参数。

## 通用响应格式

**成功：**

```json
{
  "success": true,
  "result": { ... }
}
```

**失败：**

```json
{
  "success": false,
  "code": 24001,
  "msg": "次卡不存在"
}
```

## API 端点概览

### 次卡模块 (15 endpoints)

| 路径 | 说明 |
|------|------|
| `/tcard/getById` | 根据 ID 读取次卡信息 |
| `/tcard/getByIds` | 批量读取次卡信息 |
| `/tcard/filter` | 根据条件（类目/服务）过滤次卡 |
| `/tcard/createOrder` | 创建次卡购买订单（未支付） |
| `/tcard/confirmOrder` | 确认订单支付成功 |
| `/tcard/refundOrder` | 次卡订单退款 |
| `/tcard/use` | 核销（使用）次卡 |
| `/tcard/send` | 直接发放次卡给客户（不校验领取限制、不触发发卡通知、不执行赠送逻辑） |
| `/tcard/transfer` | 次卡转卡至另一客户 |
| `/tcard/getUseRecord` | 获取次卡使用记录（分页） |
| `/tcard/getFetches` | 获取客户已领取的次卡列表 |
| `/tcard/getFetchCode` | 获取次卡二维码（注意用户权限检验） |
| `/tcard/getShareRecord` | 获取次卡分享记录 |
| `/tcard/bindShare` | 绑定次卡分享关系 |
| `/tcard/unbindShare` | 解除次卡分享关系 |

**错误码：**

- `24001` 次卡不存在
- `24002` 次卡已过期
- `24003` 客户不存在
- `24004` 无效次卡
- `24005` 次卡领取数量超过限制
- `24006` 订单不存在
- `24007` 无效订单
- `24008` 发放次卡异常
- `24009` 当前有退款正在进行
- `24010` 退款金额超出限制
- `24011` 支付方式不支持退款
- `24012` 支付设置错误
- `24013` 退款失败
- `24014` 次卡领取记录不存在
- `24015` 核销服务不存在
- `24016` 服务次数不足
- `24017` 领取记录状态错误
- `24018` 使用时段错误
- `24019` 领取记录已过期
- `24020` 次卡使用频率超过限制
- `24021` 使用异常
- `24022` 发卡员工不存在
- `24023` 发卡员工不合法
- `24024` 次卡库存不足
- `24025` 转卡目标和来源相同
- `24027` 次卡不支持分享
- `24028` 次卡分享次数超过限制
- `24029` 次卡状态异常
- `24030` 已绑定,请勿重复分享

### 预约模块 (10 endpoints)

| 路径 | 说明 |
|------|------|
| `/booking/getServiceDetail` | 获取预约服务详情（关联组、填写字段、关联服务项目） |
| `/booking/getServiceList` | 获取门店预约服务列表 |
| `/booking/getSpans` | 根据日期获取预约时刻表（可用时段、剩余数） |
| `/booking/prepareBookingOrder` | 获取下单信息（计算价格、折扣） |
| `/booking/createBookingOrder` | 创建预约订单 |
| `/booking/confirmPay` | 确认预约订单支付成功 |
| `/booking/cancelOrder` | 取消预约 |
| `/booking/closeOrder` | 关闭未支付的预约订单 |
| `/booking/getBookingOrder` | 获取预约订单详情 |
| `/booking/listBookingOrder` | 查询预约订单列表（按时间范围分页） |

**预约订单状态码：**

- `0` 待支付
- `1` 预约成功
- `2` 已开单
- `3` 已完成
- `-1` 订单未支付超时关闭
- `-2` 订单已取消
- `-3` 订单已过期
- `-5` 课程缺课

**错误码：**

- `26001` 预约服务不存在
- `26002` 客户不存在
- `26003` 门店不存在
- `26004` 参数非法
- `26005` 锁场信息为空
- `26007` 获取场地计费信息错误
- `26008` 客户在黑名单中
- `26009` 可预约库存发生变化
- `26010` 客户不满足预约条件
- `26011` 客户储值余额不足
- `26012` 未到开始预约时间
- `26013` 已停止预约
- `26014` 无效会员卡折扣
- `26015` 无效优惠券
- `26022` 预约订单不存在
- `26023` 订单不存在
- `26024` 订单状态错误

### 客户模块 (8 endpoints)

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

**客户可更新的内置属性：** `realName`, `remarkName`,
`gender`, `birth`, `province`, `city`, `district`,
`adress`, `nickName`, `avatar`

**错误码：**

- `23001` 客户不存在
- `23003` 属性不存在或不支持更新
- `23004` 属性值格式错误
- `25002` 姓名已存在
- `25003` 信息同步失败

### 教务模块 (6 endpoints)

| 路径 | 说明 |
|------|------|
| `/edu/class/getSchedules` | 获取客户某时间段课程表 |
| `/edu/class/getNextSchedule` | 获取客户最近即将开始的课程 |
| `/edu/class/getDetails` | 获取指定日期门店排课列表（时间间隔 ≤ 7天） |
| `/edu/class/listClasses` | 获取班级列表（分页） |
| `/edu/student/listClassStudent` | 获取班级学员列表（分页） |
| `/edu/teacher/getByLocation` | 获取门店教师列表 |

**课程类型：** `1` 预约课, `2` 班级排课

**错误码：**

- `25001` 暂无课程

### 订单模块 (4 endpoints)

| 路径 | 说明 |
|------|------|
| `/order/confirmBooking` | 预约订单开单（客户到店开始服务） |
| `/order/confirmPickUp` | 确认自提/核销 |
| `/order/queryByCustomer` | 根据客户查询订单列表（分页，支持按类型/支付方式过滤） |
| `/order/countByCustomer` | 根据客户查询订单数量 |

**订单类型：** `10` 会员卡购买, `11` 会员卡升级,
`12` 储值, `13` 预约, `14` 会员卡续费,
`15` 次卡购买-自助, `16` 线下收银,
`18` 次卡购买-商家售卖, `19` 商城购买, `20` 拼团,
`21` 消费补录, `22` 线上购买课程, `24` 积分兑换,
`25` 跨店下单, `26` 门禁, `29` 赛事报名,
`30` 班级报名, `34` 自助售票机, `37` 开台,
`39` 手牌消费

**支付方式：** `1` 微信, `2` 支付宝, `3` 现金,
`4` 银联, `5` 储值卡, `6` 外部自定义支付, `7` 押金

**错误码：**

- `20001` 订单不存在
- `20002` 员工不存在
- `20003` 发货类型错误
- `20004` 订单状态错误
- `20005` 订单类型错误
- `20006` 订单已开单或已自提

### 积分模块 (3 endpoints)

| 路径 | 说明 |
|------|------|
| `/score/get` | 根据手机号获取客户当前积分和累计积分 |
| `/score/mutate` | 修改客户积分（加/减） |
| `/score/listRecord` | 获取积分变更记录（分页） |

**积分来源：** `1` 积分商城兑换, `2` 管理操作,
`3` 会员升级, `4` 邀请开卡, `5` 储值奖励,
`6` 积分导入, `7` 预约, `8` 收款, `9` 次卡购买,
`10` 商城下单抵扣, `11` 拼团购买奖励,
`12` 商城购买奖励, `13` 商城订单退款,
`14` 消费补录, `15` 取消兑换礼品, `16` 接口写入

**错误码：**

- `22001` 积分客户不存在
- `22002` 增减积分类型错误
- `22003` 修改积分失败

### 会员模块 (1 endpoint)

| 路径 | 说明 |
|------|------|
| `/card/getByMobile` | 根据手机号获取会员卡信息（等级、成长值、有效期） |

**错误码：**

- `21001` 客户信息不存在
- `21002` 会员信息不存在
- `21003` 会员卡信息不存在

### 场地模块 (2 endpoints)

| 路径 | 说明 |
|------|------|
| `/booking/playground/getAll` | 获取门店所有预约场地列表 |
| `/booking/playground/getBookingRecords` | 获取场地未开始的预约记录列表 |

### 客流模块 (1 endpoint)

| 路径 | 说明 |
|------|------|
| `/people/getStat` | 获取场馆实时客流统计（当前人数、限制人数、拥挤程度） |

**拥挤程度：** `low`, `medium`, `high`, `full`

### Webhooks (3 events)

需在平台配置回调 URL。回调请求**不包含** `client_id` 参数。

| 事件 | 说明 |
|------|------|
| `BookingOrderStatusChange` | 预约订单状态变更通知 |
| `BookingPlayGroundOccupyStatusChange` | 场地占用状态变更通知 |
| `BookingOrderInfoChange` | 预约订单信息变更通知（用户填写字段和改期） |

**场地占用状态：** `1` 已占用, `-1` 已取消占用

**订单信息修改类型：** `1` 更新字段, `2` 改期

## 通用错误码

- `10003` 无效请求
- `10004` 服务器内部错误

## 金额单位

所有金额字段单位均为 **分**（1元 = 100分），类型为 integer。

## 分页约定

- 大部分列表接口支持 `page` + `size` 分页，`size` 上限通常为 100
- `/customer/list` 使用游标分页：`startCursor` 格式为 `createTime|id`

## 详细参数参考

完整的请求参数和响应字段定义，参见 `references/openapi-spec.yaml`（OpenAPI 3.0 规范）。
