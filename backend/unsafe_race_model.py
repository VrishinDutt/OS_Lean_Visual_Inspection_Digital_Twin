import random
import time
import threading
from backend.config import NUM_PRODUCTS, DEFECT_PATTERN
from backend.product import ProductPacket


current_product_id = None
inspection_results = {}
events = []
lock_for_event_log_only = threading.Lock()


def log_event(time_step, product_id, event, mode="unsafe", status="normal"):
    with lock_for_event_log_only:
        events.append({
            "time": round(time_step, 2),
            "product_id": product_id,
            "event": event,
            "mode": mode,
            "status": status
        })


def sensor_task(products):
    global current_product_id

    for product in products:
        current_product_id = product.product_id
        log_event(time.time() % 1000, product.product_id, "sensor_detected")
        time.sleep(random.uniform(0.002, 0.008))


def ai_inspection_task(products):
    global current_product_id

    for product in products:
        original_product_id = product.product_id
        frame_id = f"FRAME_{original_product_id}"

        time.sleep(random.uniform(0.003, 0.012))

        ai_result = "defective" if product.is_defective else "normal"

        mapped_product_id = current_product_id

        inspection_results[mapped_product_id] = {
            "actual_product_id": original_product_id,
            "frame_id": frame_id,
            "ai_result": ai_result
        }

        if mapped_product_id != original_product_id:
            product.race_condition = True
            log_event(
                time.time() % 1000,
                original_product_id,
                f"race_condition_result_mapped_to_{mapped_product_id}",
                status="race"
            )
        else:
            log_event(time.time() % 1000, original_product_id, "ai_result_mapped_correctly")


def actuator_task(products):
    for product in products:
        time.sleep(random.uniform(0.004, 0.01))

        result = inspection_results.get(product.product_id)

        if result and result["ai_result"] == "defective":
            product.final_decision = "reject"
            product.rejected_product_id = product.product_id
            log_event(time.time() % 1000, product.product_id, "actuator_reject")
        else:
            product.final_decision = "pass"
            log_event(time.time() % 1000, product.product_id, "actuator_pass")


def run_unsafe_simulation():
    global current_product_id, inspection_results, events

    current_product_id = None
    inspection_results = {}
    events = []

    products = [
        ProductPacket(
            product_id=f"P{i:03d}",
            is_defective=i in DEFECT_PATTERN
        )
        for i in range(1, NUM_PRODUCTS + 1)
    ]

    threads = [
        threading.Thread(target=sensor_task, args=(products,)),
        threading.Thread(target=ai_inspection_task, args=(products,)),
        threading.Thread(target=actuator_task, args=(products,))
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    race_count = sum(1 for product in products if product.race_condition)

    return {
        "mode": "unsafe",
        "products": [product.to_dict() for product in products],
        "events": events,
        "metrics": {
            "total_products": len(products),
            "race_conditions": race_count,
            "defective_products": len(DEFECT_PATTERN)
        }
    }


if __name__ == "__main__":
    result = run_unsafe_simulation()
    print(result["metrics"])
