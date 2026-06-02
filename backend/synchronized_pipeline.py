import queue
import time
from backend.config import NUM_PRODUCTS, DEFECT_PATTERN
from backend.product import ProductPacket


def log_event(events, time_step, product_id, event, mode="safe", status="normal"):
    events.append({
        "time": round(time_step, 2),
        "product_id": product_id,
        "event": event,
        "mode": mode,
        "status": status
    })


def run_safe_simulation():
    events = []

    sensor_to_camera = queue.Queue()
    camera_to_ai = queue.Queue()
    ai_to_decision = queue.Queue()
    decision_to_actuator = queue.Queue()

    products = [
        ProductPacket(
            product_id=f"P{i:03d}",
            is_defective=i in DEFECT_PATTERN
        )
        for i in range(1, NUM_PRODUCTS + 1)
    ]

    time_step = 0

    for product in products:
        sensor_to_camera.put(product)
        log_event(events, time_step, product.product_id, "sensor_detected")
        time_step += 1

    while not sensor_to_camera.empty():
        product = sensor_to_camera.get()
        product.frame_id = f"FRAME_{product.product_id}"
        camera_to_ai.put(product)
        log_event(events, time_step, product.product_id, "camera_frame_attached")
        time_step += 1

    while not camera_to_ai.empty():
        product = camera_to_ai.get()
        product.ai_result = "defective" if product.is_defective else "normal"
        product.rule_result = "fail" if product.is_defective else "pass"
        ai_to_decision.put(product)
        log_event(events, time_step, product.product_id, "inspection_complete")
        time_step += 1

    while not ai_to_decision.empty():
        product = ai_to_decision.get()
        if product.ai_result == "defective" or product.rule_result == "fail":
            product.final_decision = "reject"
        else:
            product.final_decision = "pass"

        decision_to_actuator.put(product)
        log_event(events, time_step, product.product_id, "decision_fused")
        time_step += 1

    while not decision_to_actuator.empty():
        product = decision_to_actuator.get()

        if product.final_decision == "reject":
            product.rejected_product_id = product.product_id
            log_event(events, time_step, product.product_id, "actuator_reject")
        else:
            log_event(events, time_step, product.product_id, "actuator_pass")

        time_step += 1

    return {
        "mode": "safe",
        "products": [product.to_dict() for product in products],
        "events": events,
        "metrics": {
            "total_products": len(products),
            "race_conditions": 0,
            "defective_products": len(DEFECT_PATTERN)
        }
    }


if __name__ == "__main__":
    result = run_safe_simulation()
    print(result["metrics"])
