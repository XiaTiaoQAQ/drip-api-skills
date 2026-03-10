---
name: drip-openapi
version: 1.0.0
description: "水滴智店开放接口 Claude Code Skill 插件 - 支持预约、次卡、会员、教务、积分、订单等 API 调用"
---

# 水滴智店 OpenAPI Skill

本插件提供水滴智店 (Drip Smart Store) 全部开放接口的 AI 调用能力。

## 触发条件

当用户提到以下关键词时激活本 skill：
- "水滴 API"、"水滴智店"、"Drip API"
- "次卡"、"预约"、"会员"、"积分"、"教务"、"订单"、"场地"、"客流"

## 子 Skill

根据用户需求选择对应的模块：

| Skill | 说明 | 触发关键词 |
|-------|------|------------|
| [drip-tcard](skills/drip-tcard/SKILL.md) | 次卡管理（15 个接口） | 次卡、核销、发放、转卡、分享 |
| [drip-booking](skills/drip-booking/SKILL.md) | 预约 + 场地 + 客流 + Webhook（16 个接口） | 预约、场地、客流、时刻表、webhook |
| [drip-customer](skills/drip-customer/SKILL.md) | 客户 + 会员（9 个接口） | 客户、会员、注册、手机号、学员 |
| [drip-edu](skills/drip-edu/SKILL.md) | 教务管理（6 个接口） | 课程表、排课、班级、教师 |
| [drip-order](skills/drip-order/SKILL.md) | 订单 + 积分（7 个接口） | 订单、开单、自提、积分 |

## 完整 API 参考

如需查看全部接口的统一文档：[drip-api](skills/drip-api/SKILL.md)

## 前置要求

- 环境变量 `DRIP_CLIENT_ID` 和 `DRIP_CLIENT_SECRET`（由水滴平台分配）
