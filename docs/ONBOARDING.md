# Janet Home Automation — Onboarding

**New user flow:** INDEX → QUICKSTART → first voice command in ~30 minutes

---

## Step 1: Understand What This Is (5 min)

Read [SUMMARY.md](SUMMARY.md) for:
- What's implemented (backend, janet-seed, janet-max)
- What's coming (iOS, Watch, Desktop)
- Architecture and key features

---

## Step 2: Prerequisites

- **Home Assistant** running on your network
- **janet-seed** (Janet backend)
- **Long-lived access token** from HA

See [QUICKSTART.md](QUICKSTART.md) for details.

---

## Step 3: Configure Backend (10 min)

1. Set `HOME_ASSISTANT_URL` and `HOME_ASSISTANT_TOKEN` for janet-seed
2. Test connection (see [QUICKSTART](QUICKSTART.md#step-1-configure-janet-seed-backend-5-minutes))
3. If firewall blocks: [TROUBLESHOOTING_FIREWALL.md](TROUBLESHOOTING_FIREWALL.md)

---

## Step 4: First Voice Command (5 min)

With janet-seed running and HA configured:

- Say: "Hey Janet, open Home Assistant dashboard"
- Or: "Hey Janet, turn on [entity]"

See [DASHBOARD_ACCESS.md](DASHBOARD_ACCESS.md) for dashboard commands.

---

## Constitutional Fit (Janet UX)

- **Soul Check**: Unlocking doors, disabling security, large temp changes require confirmation
- **Privacy**: All local network; no cloud; data never leaves home
- **Offline queue**: Commands queue when offline, execute when back online

---

## Next Steps

- **Developers:** [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md), [IOS_SHORTCUTS.md](IOS_SHORTCUTS.md)
- **Project managers:** [ROADMAP.md](ROADMAP.md)
- **Troubleshooting:** [TROUBLESHOOTING_FIREWALL.md](TROUBLESHOOTING_FIREWALL.md)
