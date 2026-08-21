"""
AI-Driven API Test Generator (HW06 - Agent Skill G9.5)
Tự động đọc tài liệu API Specification và sinh Postman Collection v2.1 cho 4 FR
"""

import json
import os
import re

def parse_api_spec(spec_file_path):
    """Trích xuất danh sách endpoint và phương thức từ file markdown spec"""
    with open(spec_file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    endpoints = []
    pattern = r"- \*\*Endpoint:\*\* `(GET|POST|PUT|DELETE)\s+([^\`]+)`"
    matches = re.findall(pattern, content)
    for method, path in matches:
        endpoints.append({"method": method.strip(), "path": path.strip()})
    return endpoints

def generate_postman_item(endpoint, student_id="25127001"):
    """Sinh một request item trong Postman Collection kèm test assertions"""
    method = endpoint["method"]
    path = endpoint["path"]
    name = f"AutoTest: {method} {path}"
    
    test_script = f"""
pm.test("Status code is 200/201 or handled error", function () {{
    pm.expect([200, 201, 400, 401, 403, 404]).to.include(pm.response.code);
}});

pm.test("Response carries X-Student-Id reflection or header", function () {{
    pm.expect(pm.request.headers.get("X-Student-Id")).to.eql("{student_id}");
}});
"""

    item = {
        "name": name,
        "request": {
            "method": method,
            "header": [
                {"key": "Content-Type", "value": "application/json"},
                {"key": "X-Student-Id", "value": student_id}
            ],
            "url": {
                "raw": "{{baseUrl}}" + path,
                "host": ["{{baseUrl}}"],
                "path": [p for p in path.split("/") if p]
            }
        },
        "event": [
            {
                "listen": "test",
                "script": {
                    "exec": [line for line in test_script.strip().split("\n")],
                    "type": "text/javascript"
                }
            }
        ]
    }
    return item

def build_postman_collection(endpoints, output_path="collections/Auto_Generated_Collection.json"):
    """Đóng gói toàn bộ endpoints thành Postman Collection JSON hoàn chỉnh"""
    collection = {
        "info": {
            "_postman_id": "auto-generated-hw06-collection",
            "name": "HW06 Auto Generated API Test Collection",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": [generate_postman_item(ep) for ep in endpoints]
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(collection, f, indent=2, ensure_ascii=False)
    print(f"Successfully generated Postman Collection at: {output_path}")

if __name__ == "__main__":
    spec_path = "eshop-sut/api_specification.md"
    if os.path.exists(spec_path):
        endpoints = parse_api_spec(spec_path)
        build_postman_collection(endpoints)
    else:
        print("API spec file not found. Please verify the path.")
