# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Sponge Wallet

**Mon wallet autonome** — géré via skill `sponge-wallet`

- Solana address: `EAMNyeugCfvCyXX4SZ3tUXM6fWxovYJWTCw2JbqmeueR`
- API key: stockée dans `skills/sponge-wallet/.env`
- MCP endpoint: `https://api.wallet.paysponge.com/mcp`
- Capabilities: crypto transfers, swaps, bridges, x402 paid services, Polymarket, Hyperliquid

**Spending controls (configurés via dashboard):**
- Budget quotidien: **0.01 SOL/jour** (~$0.83) ✅
- Géré côté serveur Sponge (je ne peux pas dépasser cette limite)
- Permet autonomie contrôlée pour transactions, swaps, x402 services

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
