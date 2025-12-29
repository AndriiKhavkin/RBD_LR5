# Лабораторна робота №5  
## Моніторинг BESS (Battery Energy Storage System) через Prometheus Exporter

**Дисципліна:** Проєктування систем з розподіленими базами даних в енергетиці  
**Тема ЛР5:** Метрики/моніторинг DER/BESS, Prometheus (та опційно Grafana)

---

## Що робить ця лабораторна
Скрипт `lr5.py` симулює флот з 3 акумуляторних систем (BESS_01..BESS_03) і експортує метрики у форматі Prometheus на HTTP.

Особливість симуляції:
- стартує **нормальний режим** (SOC ~ 50–60%, SOH ~ 97–99%)
- через ~15 секунд **імітується аварійний стан**: низький SOC (10–25%), деградація SOH (~83–84.5%) і різко більша швидкість деградації

---

## Метрики (Prometheus)
Експортуються такі метрики (label: `battery_id`):

- `der_battery_soc` — State of Charge (%), **Gauge**
- `der_battery_soh` — State of Health (%), **Gauge**
- `der_battery_power_kw` — потужність (+ заряд / − розряд), **Gauge**
- `der_battery_cycles_total` — лічильник “циклів” (умовно), **Counter**

---

## Структура проєкту (рекомендовано)
```
RBD_LAB5/
├── lr5.py
├── requirements.txt
├── docker-compose.yml          # (опційно) Prometheus + Grafana
├── prometheus.yml              # (опційно) конфіг Prometheus
├── README.md
├── REPORT_LR5.md
└── .gitignore
```

---

## Швидкий старт (тільки Python exporter)

### 1) Створити venv і встановити залежності
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -r requirements.txt
```

### 2) Запустити exporter
```powershell
python lr5.py
```

### 3) Перевірити метрики в браузері
Відкрий:
- `http://localhost:8000/metrics`

---

## Запуск з Prometheus + Grafana (docker compose)
> Це зручно, щоб мати історію та графіки (а не просто /metrics).

### 1) Підняти сервіси
```powershell
docker compose up -d
docker compose ps
```

### 2) Запустити exporter (окремо)
```powershell
python lr5.py
```

### 3) Prometheus
- UI: `http://localhost:9090`
- Targets → має бути target `lr5_exporter` у стані **UP**

### 4) Grafana
- UI: `http://localhost:3000`
- логін/пароль: `admin / admin` (попросить змінити)

Потім:
1) **Add data source** → Prometheus  
2) URL: `http://prometheus:9090`  
3) Save & test

---

## Приклади PromQL для графіків/перевірок

### SOC по кожній батареї
```promql
der_battery_soc
```

### SOH по кожній батареї
```promql
der_battery_soh
```

### Потужність (заряд/розряд)
```promql
der_battery_power_kw
```

### “Цикли” (швидкість росту)
```promql
rate(der_battery_cycles_total[5m])
```

### Аварійний стан (приклад умов)
Низький SOC (< 25%):
```promql
der_battery_soc < 25
```

Низький SOH (< 85%):
```promql
der_battery_soh < 85
```

---

## Висновки (коротко)
- Prometheus exporter дозволяє стандартизовано знімати стан DER/BESS у реальному часі.
- Метрики SOC/SOH/Power/Цикли дають базу для виявлення аварійних ситуацій (низький заряд, деградація, пікові режими).
- З Prometheus+Grafana з’являється історія, тренди, алерти та зручні дашборди.
