from __future__ import annotations

import ipaddress
import json
from pathlib import Path
from typing import Any


class ValidationError(ValueError):
    pass


def load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_network_plan(plan: dict[str, Any]) -> list[str]:
    messages: list[str] = []
    base = ipaddress.ip_network(plan["base_network"], strict=True)
    segments = plan["segments"]
    networks: list[tuple[str, ipaddress.IPv4Network]] = []
    vlans: set[int] = set()

    for segment in segments:
        name = segment["name"]
        network = ipaddress.ip_network(segment["subnet"], strict=True)
        gateway = ipaddress.ip_address(segment["gateway"])

        if not network.subnet_of(base):
            raise ValidationError(f"{name}: {network} is outside base network {base}")
        if gateway not in network or gateway in (network.network_address, network.broadcast_address):
            raise ValidationError(f"{name}: gateway {gateway} is not a usable address in {network}")
        if segment["vlan"] is not None:
            vlan = int(segment["vlan"])
            if vlan in vlans:
                raise ValidationError(f"duplicate VLAN ID: {vlan}")
            vlans.add(vlan)
        networks.append((name, network))
        messages.append(f"OK {name}: {network} ({network.num_addresses - 2} usable IPv4 hosts)")

    for i, (name_a, net_a) in enumerate(networks):
        for name_b, net_b in networks[i + 1 :]:
            if net_a.overlaps(net_b):
                raise ValidationError(f"overlap: {name_a} {net_a} vs {name_b} {net_b}")

    for isolated in plan.get("isolated_networks", []):
        ipaddress.ip_network(isolated["subnet"], strict=True)
        if isolated.get("routed_to_corporate") is not False:
            raise ValidationError(f"{isolated['name']}: expected explicit corporate isolation")
        messages.append(f"OK isolated network: {isolated['name']} {isolated['subnet']}")

    return messages


def validate_firewall_policy(plan: dict[str, Any], policy: dict[str, Any]) -> list[str]:
    if policy.get("default_action") != "deny":
        raise ValidationError("firewall policy must be default-deny")

    known = {segment["name"] for segment in plan["segments"]}
    known |= {item["name"] for item in plan.get("isolated_networks", [])}
    known |= {"internet", "internal"}

    ids: set[str] = set()
    messages: list[str] = []
    for rule in policy["rules"]:
        rule_id = rule["id"]
        if rule_id in ids:
            raise ValidationError(f"duplicate firewall rule id: {rule_id}")
        ids.add(rule_id)
        if rule["source"] not in known:
            raise ValidationError(f"{rule_id}: unknown source {rule['source']}")
        if rule["destination"] not in known:
            raise ValidationError(f"{rule_id}: unknown destination {rule['destination']}")
        if rule["action"] not in {"allow", "deny"}:
            raise ValidationError(f"{rule_id}: invalid action {rule['action']}")
        if rule["protocol"] not in {"tcp", "udp", "icmp", "any"}:
            raise ValidationError(f"{rule_id}: invalid protocol {rule['protocol']}")
        ports = rule.get("ports", [])
        if any(not 1 <= int(port) <= 65535 for port in ports):
            raise ValidationError(f"{rule_id}: invalid port")
        messages.append(f"OK {rule_id}: {rule['source']} -> {rule['destination']} {rule['action']}")

    required_denies = {
        ("guest", "internal"),
        ("internal", "production-ot"),
        ("production-ot", "internal"),
    }
    actual_denies = {
        (rule["source"], rule["destination"])
        for rule in policy["rules"]
        if rule["action"] == "deny"
    }
    missing = required_denies - actual_denies
    if missing:
        raise ValidationError(f"missing explicit isolation denies: {sorted(missing)}")

    return messages


def validate_files(network_path: str | Path, firewall_path: str | Path) -> list[str]:
    plan = load_json(network_path)
    policy = load_json(firewall_path)
    return validate_network_plan(plan) + validate_firewall_policy(plan, policy)
