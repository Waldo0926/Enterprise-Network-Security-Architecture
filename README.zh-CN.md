# 企业网络安全架构

[English](README.md)

这是一个完全虚构的企业网络安全设计，并将关键设计转化为 **architecture-as-code**：规范的 CIDR/VLAN 规划、默认拒绝防火墙策略、网络分段、DMZ、远程访问、企业 Wi-Fi、明确的 OT 信任边界，以及自动化验证和威胁模型文档。

> 本项目是课程结束后的作品集重构，**不是原始作业提交**。组织、拓扑、地址和策略均为虚构，不描述 Monash University 或任何真实生产网络。

## 为什么这样重构

网络图很容易画，但也很容易出现网段重叠、CIDR 边界错误、策略引用不存在的 zone 等问题。因此这个版本把地址和防火墙规则写成 JSON，再用 Python 自动检查。

验证器会检查：

- CIDR 边界是否合法；
- 内部网段是否全部位于 `10.20.0.0/21`；
- 是否存在网段重叠；
- gateway 是否为可用地址；
- VLAN ID 是否重复；
- 防火墙是否默认拒绝；
- 策略是否引用合法 zone；
- Guest 与 OT 隔离规则是否明确存在。

## 地址规划

| Zone | 子网 | 可用主机数 | 用途 |
|---|---|---:|---|
| Corporate LAN | `10.20.0.0/23` | 510 | 受管终端 |
| Corporate Wi-Fi | `10.20.2.0/23` | 510 | 802.1X 无线客户端 |
| Guest | `10.20.4.0/24` | 254 | 仅访问互联网 |
| IoT / Print | `10.20.5.0/25` | 126 | 打印机与受限 IoT |
| Management | `10.20.5.128/26` | 62 | Jump host / 管理面 |
| DMZ | `10.20.5.192/26` | 62 | 对外服务 |
| Infrastructure | `10.20.6.0/25` | 126 | Identity、RADIUS、DNS、日志 |
| VPN pool | `10.20.6.128/25` | 126 | 远程客户端 |

示例 OT 环境位于独立的 `10.30.0.0/24` 安全域，并在防火墙策略中明确禁止与企业 IT 网络双向访问。

## 运行

无需第三方 Python 包：

```bash
PYTHONPATH=. python scripts/validate_architecture.py
python -m unittest discover -s tests -v
```

## 展示的能力

- default-deny 与 least privilege；
- DMZ 与对外服务隔离；
- VLAN segmentation / inter-zone ACL；
- WPA3-Enterprise / 802.1X / RADIUS；
- MFA 远程和高权限访问；
- 独立管理网络；
- Guest / IoT containment；
- IT/OT 信任边界；
- 日志、EDR、磁盘加密与恢复策略；
- CI 中自动验证网络架构。

## 来源说明

这个项目是在学习 Monash University **FIT1047 Introduction to Computer Systems, Networks and Security** 里的企业网络安全概念后重新实现的。原课程场景和地址方案与本项目不同；本仓库不包含 assessment specification、原提交文件或真实基础设施信息。
