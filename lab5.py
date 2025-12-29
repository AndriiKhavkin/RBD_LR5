import random
import time
from prometheus_client import start_http_server, Gauge, Counter

soc_gauge = Gauge('der_battery_soc', 'State of Charge (%)', ['battery_id'])
soh_gauge = Gauge('der_battery_soh', 'State of Health (%)', ['battery_id'])
power_gauge = Gauge('der_battery_power_kw', 'Net power (+charge/-discharge)', ['battery_id'])
cycles_counter = Counter('der_battery_cycles_total', 'Total charge/discharge cycles', ['battery_id'])

def simulate_battery_fleet():
    batteries = ['BESS_01', 'BESS_02', 'BESS_03']
    
    battery_data = {
        b: {
            'soh': random.uniform(97.0, 99.0),
            'soc': random.uniform(50.0, 60.0),
            'deg_rate': 0.01
        } for b in batteries
    }

    start_time = time.time()
    emergency_triggered = False

    print("=== ЗАПУСК МОНІТОРИНГУ: СТАН НОРМАЛЬНИЙ ===")

    while True:

        if not emergency_triggered and (time.time() - start_time) > 15:
            print("\n!!! УВАГА: СИМУЛЯЦІЯ АВАРІЙНОГО СТАНУ (НИЗЬКИЙ ЗАРЯД ТА ДЕГРАДАЦІЯ) !!!\n")
            for b_id in batteries:
                battery_data[b_id]['soc'] = random.uniform(10.0, 25.0) 
                battery_data[b_id]['soh'] = random.uniform(83.0, 84.5) 
                battery_data[b_id]['deg_rate'] = 0.5 
            emergency_triggered = True

        for b_id in batteries:
       
            if not emergency_triggered:
                battery_data[b_id]['soc'] += random.uniform(-1.0, 1.0)
            

            battery_data[b_id]['soc'] = max(0, min(100, battery_data[b_id]['soc']))
            soc_gauge.labels(battery_id=b_id).set(battery_data[b_id]['soc'])

   
            power = random.uniform(-50, 50)
            power_gauge.labels(battery_id=b_id).set(power)


            battery_data[b_id]['soh'] -= battery_data[b_id]['deg_rate']
            noise = random.uniform(-0.02, 0.02)
            soh_gauge.labels(battery_id=b_id).set(battery_data[b_id]['soh'] + noise)

 
            if abs(power) > 45:
                cycles_counter.labels(battery_id=b_id).inc(0.1)

        print(f"Поточний статус - BESS_01: SOC={battery_data['BESS_01']['soc']:.1f}%, SOH={battery_data['BESS_01']['soh']:.2f}%")
        time.sleep(5)

if __name__ == '__main__':
    start_http_server(8000)
    simulate_battery_fleet()