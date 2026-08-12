# E3/E4 — rolling-window and ACI step-size sensitivity

Generated 2026-08-12T16:48:06.150104+00:00 | nominal 0.80 | eval 2015-01-01..2026-02-27 (Hormuz window excluded)

Cells evaluated: 270 (model x series x horizon); missing: 0.
Post-hoc robustness analysis. The pre-registered configuration is window 250, gamma 0.02.

## Median PICP across models and series (nominal 0.80)

### h = 1

| method | window | gamma | calm | covid | ukraine |
|---|---|---|---|---|---|
| ACI | 250 | 0.005 | 0.803 | 0.741 | 0.779 |
| ACI | 250 | 0.01 | 0.800 | 0.763 | 0.798 |
| ACI **(pre-registered)** | 250 | 0.02 | 0.798 | 0.770 | 0.809 |
| ACI | 250 | 0.05 | 0.799 | 0.793 | 0.809 |
| Rolling-SC | 50 | — | 0.822 | 0.800 | 0.813 |
| Rolling-SC | 100 | — | 0.807 | 0.770 | 0.771 |
| Rolling-SC **(pre-registered)** | 250 | — | 0.802 | 0.733 | 0.656 |
| Rolling-SC | 500 | — | 0.804 | 0.733 | 0.565 |

### h = 5

| method | window | gamma | calm | covid | ukraine |
|---|---|---|---|---|---|
| ACI | 250 | 0.005 | 0.805 | 0.733 | 0.763 |
| ACI | 250 | 0.01 | 0.803 | 0.763 | 0.779 |
| ACI **(pre-registered)** | 250 | 0.02 | 0.798 | 0.774 | 0.794 |
| ACI | 250 | 0.05 | 0.798 | 0.793 | 0.798 |
| Rolling-SC | 50 | — | 0.813 | 0.785 | 0.790 |
| Rolling-SC | 100 | — | 0.803 | 0.756 | 0.741 |
| Rolling-SC **(pre-registered)** | 250 | — | 0.799 | 0.704 | 0.699 |
| Rolling-SC | 500 | — | 0.799 | 0.715 | 0.618 |

### h = 22

| method | window | gamma | calm | covid | ukraine |
|---|---|---|---|---|---|
| ACI | 250 | 0.005 | 0.803 | 0.748 | 0.737 |
| ACI | 250 | 0.01 | 0.804 | 0.748 | 0.741 |
| ACI **(pre-registered)** | 250 | 0.02 | 0.800 | 0.756 | 0.763 |
| ACI | 250 | 0.05 | 0.798 | 0.770 | 0.763 |
| Rolling-SC | 50 | — | 0.771 | 0.733 | 0.679 |
| Rolling-SC | 100 | — | 0.788 | 0.711 | 0.664 |
| Rolling-SC **(pre-registered)** | 250 | — | 0.793 | 0.637 | 0.599 |
| Rolling-SC | 500 | — | 0.791 | 0.593 | 0.573 |

## Decisive comparison

- **h = 1**: best rolling window is 50 at PICP 0.813 (ukraine); pre-registered ACI (gamma 0.02) reaches 0.809 at its best crisis regime and 0.770 at its worst.
- **h = 5**: best rolling window is 50 at PICP 0.790 (ukraine); pre-registered ACI (gamma 0.02) reaches 0.794 at its best crisis regime and 0.774 at its worst.
- **h = 22**: best rolling window is 50 at PICP 0.733 (covid); pre-registered ACI (gamma 0.02) reaches 0.763 at its best crisis regime and 0.756 at its worst.
