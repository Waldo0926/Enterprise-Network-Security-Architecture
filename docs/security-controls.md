# Security controls

## Edge and DMZ

- stateful firewall and NAT with default-deny inbound policy;
- public HTTPS and mail services isolated in a DMZ;
- TLS-only administration and modern TLS for public services;
- IDS/IPS visibility at the edge and key internal choke points;
- separate public DNS and VPN termination.

## Identity and access

- central identity provider;
- MFA for VPN and privileged access;
- WPA3-Enterprise / 802.1X, with EAP-TLS preferred for managed devices;
- RADIUS confined to the infrastructure segment;
- administrative access originates from the management/jump-host segment.

## Endpoint and data protection

- full-disk encryption;
- patching and EDR;
- salted password hashes using a modern password KDF (for applications that must store passwords);
- centralised logging with retention appropriate to the organisation's operational and legal needs.

## Segmentation

- separate corporate LAN and enterprise Wi-Fi segments;
- guest network denied access to internal zones;
- printers/IoT isolated and reachable only on required service ports;
- production/OT represented as a separate, non-routed security domain with explicit bidirectional deny rules.

## Recovery

- configuration backups;
- tested service/database backups;
- documented restoration procedures;
- secondary DNS and recovery paths for critical public services.
