# drip-openapi

水滴智店 (Drip Smart Store) 开放接口 Claude Code Skill、OpenClaw Skills 插件。

## 简介

将水滴智店 OpenAPI 封装为 Claude Code Skill，让 Claude Code或者Openclaw 等支持通用skills协议的工具能够直接调用水滴智店的全部开放接口，涵盖预约、次卡、客户、教务、订单、积分、会员、场地、客流等 9 大模块，共 50+ 个 API 端点。

## 快速开始

### 1. 安装

```bash
# 方式一：克隆仓库
git clone <repo-url> && cd drip-openapi

# 方式二：下载 ZIP 并解压到 Claude Code skill 目录
```

### 2. 配置凭证

复制环境变量模板并填入你的凭证：

```bash
cp .env.example .env
# 编辑 .env，填入平台分配的 client_id 和 client_secret
```

### 3. 使用

在 Claude Code 中直接用自然语言调用水滴 API：

```
"帮我查询手机号 13800138000 的客户信息"
"查看明天上午的预约时刻表"
"给客户增加 100 积分"
"查询最近 7 天的预约订单"
"获取门店所有场地列表"
```

## 功能模块

| 模块 | 接口数 | 核心能力 |
|------|--------|----------|
| 次卡管理 | 15 | 查询、购买、核销、发放、转卡、分享 |
| 预约管理 | 10 | 服务列表、时刻表、创建/取消/关闭订单 |
| 客户管理 | 8 | 查询、注册、属性更新、学员管理 |
| 教务管理 | 6 | 课程表、班级、教师 |
| 订单管理 | 4 | 开单、自提、查询 |
| 积分管理 | 3 | 查询、增减、记录 |
| 会员查询 | 1 | 会员卡信息 |
| 场地管理 | 2 | 场地列表、预约记录 |
| 客流统计 | 1 | 实时客流 |
| Webhooks | 3 | 订单状态变更、场地占用变更、订单信息变更 |

## 认证方式

所有接口使用双重 SHA256 签名认证：

```
sign = sha256(sha256(body + client_secret + ts) + client_secret)
```

详见 [API 参考文档](skills/drip-api/SKILL.md)。

## 项目结构

```
drip-openapi/
├── CLAUDE.md                          # Claude Code 项目指引
├── SKILL.md                           # Skill 统一入口
├── README.md                          # 本文件
├── .env.example                       # 环境变量模板
├── .gitignore
├── .claude-plugin/
│   └── plugin.json                    # 插件元数据
└── skills/
    └── drip-api/
        ├── SKILL.md                   # API 参考文档
        └── references/
            └── openapi-spec.yaml      # OpenAPI 3.0 完整规范
```

## 技术说明

- **Base URL:** `https://zd.drip.im/open/zd`
- **请求方式:** 全部 POST，Content-Type: application/json
- **金额单位:** 分（1 元 = 100 分）
- **分页:** `page` + `size`（上限 100），客户列表使用游标分页

## License

MIT
