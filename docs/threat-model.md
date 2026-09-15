# Threat model

This is a fictional Sales & Marketing enterprise used to demonstrate network-security design. It does not describe a real organisation or production environment.

## Assets

- customer/lead PII and order information;
- marketing assets and CMS credentials;
- mailboxes and identity credentials;
- managed endpoints;
- administrative credentials;
- availability of public web/mail services.

## Primary threats

| Threat | Example impact | Main controls |
|---|---|---|
| Credential theft / phishing | Mail, CRM or VPN account takeover | MFA, EAP-TLS, central identity, EDR, logging |
| Internet-facing service exploit | Web/mail compromise | DMZ, default-deny edge policy, patching, IDS/IPS, TLS |
| Lateral movement | Workstation compromise spreads internally | VLAN segmentation, inter-zone ACLs, management jump host |
| Lost laptop | Disclosure of customer or campaign data | Full-disk encryption, strong authentication, remote management |
| Guest/IoT pivot | Unmanaged device reaches corporate assets | Guest internet-only policy, IoT/print isolation, explicit ACLs |
| OT compromise | Business IT reaches operational systems | Separate address space and explicit bidirectional deny policy |
| Data exfiltration | Sensitive records leave the organisation | Egress logging, least privilege, monitored choke points |

## Trust boundaries

1. Internet ↔ DMZ
2. DMZ ↔ internal segments
3. Corporate clients ↔ infrastructure services
4. Guest/IoT ↔ corporate networks
5. Management ↔ managed systems
6. Corporate IT ↔ isolated OT
7. Remote VPN clients ↔ approved internal applications

## Design philosophy

The project uses a **default-deny** policy and then adds narrowly scoped business flows. The JSON policy is deliberately readable and machine-validatable so the written architecture and the implementable policy do not silently drift apart.
