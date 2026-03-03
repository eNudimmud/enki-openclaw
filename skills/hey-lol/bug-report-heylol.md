# Bug Report: x402 Payment Signature Failure with Sponge Wallet

**To:** support@hey.lol  
**From:** HelveticVault@gmail.com  
**Date:** 2026-02-22  
**Subject:** x402 Registration Payment Failing - MissingRequiredSignature Error

---

## Summary

I'm attempting to register an AI agent on hey.lol using the Sponge Wallet (https://wallet.paysponge.com) for x402 payments. The payment is being sent successfully (0.01 USDC transferred), but the transaction fails on hey.lol's side with error: `PAYMENT_SETTLEMENT_FAILED: MissingRequiredSignature`.

---

## Environment

- **Wallet Provider:** Sponge Wallet (MCP-managed, API: https://api.wallet.paysponge.com)
- **Payment Method:** x402 via Sponge's `/api/x402/fetch` endpoint
- **Chain:** Solana mainnet
- **Token:** USDC (EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v)
- **Wallet Address:** EAMNyeugCfvCyXX4SZ3tUXM6fWxovYJWTCw2JbqmeueR
- **Base Address:** 0xBa18cDaa2bfdF26c929d045e9bB6F19f9fe1ac75

---

## Steps to Reproduce

1. Configure Sponge Wallet with valid Solana and Base wallets
2. Fund Solana wallet with USDC (minimum $0.02)
3. Attempt registration via x402 payment:

```bash
curl -X POST "https://api.wallet.paysponge.com/api/x402/fetch" \
  -H "Authorization: Bearer <SPONGE_API_KEY>" \
  -H "Sponge-Version: 0.2.0" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://api.hey.lol/agents/register",
    "method": "POST",
    "headers": {
      "Content-Type": "application/json"
    },
    "body": {
      "username": "enki",
      "display_name": "Enki 🐇",
      "bio": "...",
      "base_address": "0xBa18cDaa2bfdF26c929d045e9bB6F19f9fe1ac75"
    },
    "preferred_chain": "solana"
  }'
```

---

## Observed Behavior

**Response:**
```json
{
  "status": 402,
  "ok": false,
  "data": {
    "error": "PAYMENT_SETTLEMENT_FAILED",
    "message": "Transaction failed: {\"InstructionError\":[2,\"MissingRequiredSignature\"]}"
  },
  "payment_made": true,
  "payment_details": {
    "chain": "solana",
    "amount": "0.01",
    "token": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    "to": "CPsCCNemvgxsijbYTgWS5e4hJEUL3rFbB83jniiKjhuy"
  }
}
```

**Key Observations:**
- `payment_made: true` — Sponge successfully created and sent the USDC payment
- `PAYMENT_SETTLEMENT_FAILED` — hey.lol rejects the transaction
- `InstructionError[2, "MissingRequiredSignature"]` — Solana instruction #2 is missing a required signature

This suggests that while Sponge's x402 implementation signs and submits the payment transaction, hey.lol's verification step expects an additional signature that is not present.

---

## Expected Behavior

The registration should complete successfully, and the agent profile should be created on hey.lol after the 0.01 USDC payment is confirmed.

---

## Additional Context

- Sponge Wallet implements x402 payments using the `@x402/svm/exact/client` library
- Other x402 services work correctly with Sponge (confirmed with search, image generation, and data enrichment APIs)
- Direct wallet creation and x402 client setup using `@x402/fetch` + `@x402/svm/exact/client` locally also fails with the same error (attempted via Node.js ESM script)

---

## Questions

1. Does hey.lol require a specific x402 signature format or additional metadata that Sponge might not be providing?
2. Are there known compatibility issues with Sponge Wallet or specific x402 client versions?
3. Can you provide debug logs or transaction details for the failed payment attempts to help identify the missing signature?

---

## Workaround Request

If this is a known issue with Sponge Wallet or MCP-managed x402 implementations, is there:
- A manual registration endpoint that accepts direct USDC transfers?
- An alternative authentication method for AI agents using managed wallets?

---

## Contact

**Email:** HelveticVault@gmail.com  
**Twitter/X:** @HelveticVault  
**Agent Details:**
- Name: Enki (escaped lab rabbit, NeukoAI lore)
- Mission: Teaching digital sovereignty, building in the $ENKI ecosystem

Happy to provide additional logs, transaction hashes, or test with alternative configurations. Let me know what information would be helpful to debug this issue.

Thanks for your help! 🐇
