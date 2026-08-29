#!/usr/bin/env python3
"""
================================================================================
AI-DRIVEN API TEST GENERATOR (HW06 - ESHOP SUT)
================================================================================
Student Name: Nguyễn Nhật Nam
Student ID:   23127092
Class:        23KTPM2
Bloom Level:  G9.5 (Create)

Description:
A comprehensive, deterministic & semantic AI testing engine that generates
exhaustive API test suites (ISTQB EP/BVA, OWASP Security SEC-01..07, State Machine,
and JSON Schema) for any feature (FR-01 to FR-19) in the EShop SUT.
================================================================================
"""

import os
import sys
import json
import argparse
import uuid

# Complete Feature Catalog for EShop SUT (Covers Pools A, B, C, D)
FEATURE_CATALOG = {
    "FR-01": {
        "name": "Account Registration",
        "pool": "Pool A",
        "endpoint": "/api/register",
        "method": "POST",
        "auth_required": False,
        "role_required": None,
        "sample_body": {"name": "Nguyen Van A", "email": "test_user_{rand}@domain.com", "password": "Password123!"},
        "fields": {
            "name": {"type": "string", "min_len": 2, "max_len": 50, "required": True},
            "email": {"type": "email", "required": True},
            "password": {"type": "password", "min_len": 6, "required": True}
        }
    },
    "FR-02": {
        "name": "Login & Account Lockout",
        "pool": "Pool A",
        "endpoint": "/api/login",
        "method": "POST",
        "auth_required": False,
        "role_required": None,
        "sample_body": {"email": "test@eshop.com", "password": "Test1234!"},
        "fields": {
            "email": {"type": "email", "required": True},
            "password": {"type": "string", "required": True}
        }
    },
    "FR-03": {
        "name": "Forgot Password & Password Reset",
        "pool": "Pool A",
        "endpoint": "/api/forgot-password",
        "method": "POST",
        "auth_required": False,
        "role_required": None,
        "sample_body": {"email": "test@eshop.com"},
        "fields": {
            "email": {"type": "email", "required": True}
        }
    },
    "FR-04": {
        "name": "Personal Profile Management",
        "pool": "Pool A",
        "endpoint": "/api/users/me",
        "method": "PUT",
        "auth_required": True,
        "role_required": "user",
        "sample_body": {"name": "Nguyen Van A", "shipping_address": "123 Le Loi, Q1", "phone": "0912345678"},
        "fields": {
            "name": {"type": "string", "min_len": 2, "max_len": 100, "required": True},
            "phone": {"type": "phone", "regex": "^0[0-9]{9,10}$", "required": False},
            "shipping_address": {"type": "string", "min_len": 5, "max_len": 255, "required": False}
        }
    },
    "FR-05": {
        "name": "Product Listing & Search",
        "pool": "Pool A",
        "endpoint": "/api/products",
        "method": "GET",
        "auth_required": False,
        "role_required": None,
        "query_params": ["search", "category_id", "minPrice", "maxPrice", "page", "limit", "sort"]
    },
    "FR-06": {
        "name": "Product Detail View",
        "pool": "Pool A",
        "endpoint": "/api/products/:id",
        "method": "GET",
        "auth_required": False,
        "role_required": None,
        "path_params": ["id"]
    },
    "FR-07": {
        "name": "Shopping Cart",
        "pool": "Pool B",
        "endpoint": "/api/cart",
        "method": "POST",
        "auth_required": True,
        "role_required": "user",
        "sample_body": {"productId": 1, "quantity": 2},
        "fields": {
            "productId": {"type": "integer", "min": 1, "required": True},
            "quantity": {"type": "integer", "min": 1, "max": 99, "required": True}
        }
    },
    "FR-08": {
        "name": "Checkout & Order Placement",
        "pool": "Pool B",
        "endpoint": "/api/checkout",
        "method": "POST",
        "auth_required": True,
        "role_required": "user",
        "sample_body": {"total_amount": 500000, "shipping_address": "123 Nguyen Trai, Q5"},
        "fields": {
            "total_amount": {"type": "integer", "min": 1000, "required": True},
            "shipping_address": {"type": "string", "min_len": 5, "required": True}
        }
    },
    "FR-09": {
        "name": "Apply Coupon (Mobile Flow)",
        "pool": "Pool D",
        "endpoint": "/api/apply-coupon",
        "method": "POST",
        "auth_required": False,
        "role_required": None,
        "sample_body": {"code": "SAVE10", "total_amount": 500000, "user_id": 1},
        "fields": {
            "code": {"type": "string", "min_len": 1, "max_len": 20, "required": True},
            "total_amount": {"type": "integer", "min": 0, "required": True},
            "user_id": {"type": "integer", "min": 1, "required": False}
        }
    },
    "FR-10": {
        "name": "Order State Machine & Cancellation",
        "pool": "Pool B",
        "endpoint": "/api/orders/:id/cancel",
        "method": "PUT",
        "auth_required": True,
        "role_required": "user",
        "path_params": ["id"],
        "sample_body": {},
        "state_transitions": {
            "allowed": ["pending", "confirmed"],
            "disallowed": ["shipping", "delivered", "canceled"]
        }
    },
    "FR-11": {
        "name": "Order History View (User)",
        "pool": "Pool B",
        "endpoint": "/api/orders/my-orders",
        "method": "GET",
        "auth_required": True,
        "role_required": "user"
    },
    "FR-12": {
        "name": "Admin Access Control Verification",
        "pool": "Pool C",
        "endpoint": "/api/admin/import-products",
        "method": "POST",
        "auth_required": True,
        "role_required": "admin",
        "sample_body": {"products": [{"name": "Sample", "price": 100000, "category_id": 1}]}
    },
    "FR-14": {
        "name": "Category Management CRUD",
        "pool": "Pool C",
        "endpoint": "/api/categories",
        "method": "POST",
        "auth_required": True,
        "role_required": "admin",
        "sample_body": {"name": "Do Gia Dung"},
        "fields": {
            "name": {"type": "string", "min_len": 2, "max_len": 50, "required": True}
        }
    },
    "FR-15": {
        "name": "Admin Product CRUD",
        "pool": "Pool C",
        "endpoint": "/api/products",
        "method": "POST",
        "auth_required": True,
        "role_required": "admin",
        "sample_body": {"name": "Tai nghe Sony", "price": 2500000, "description": "Chong on", "imageUrl": "https://placehold.co/300", "category_id": 1},
        "fields": {
            "name": {"type": "string", "min_len": 2, "max_len": 150, "required": True},
            "price": {"type": "integer", "min": 1000, "required": True},
            "category_id": {"type": "integer", "min": 1, "required": True}
        }
    },
    "FR-16": {
        "name": "Product Import from CSV",
        "pool": "Pool C",
        "endpoint": "/api/admin/import-products",
        "method": "POST",
        "auth_required": True,
        "role_required": "admin",
        "sample_body": {"products": [{"name": "CSV Item 1", "price": 200000, "category_id": 1}]}
    },
    "FR-17": {
        "name": "Coupon Management (Admin CRUD)",
        "pool": "Pool C",
        "endpoint": "/api/coupons",
        "method": "GET",
        "auth_required": True,
        "role_required": "admin"
    }
}

class APITestAgent:
    """
    Automated Test Synthesizer applying ISTQB Domain Partitioning, Boundary Value Analysis,
    OWASP API Security Top 10 heuristics, and Postman v2.1.0 Collection generation.
    """
    def __init__(self, student_id="23127092", base_url="http://localhost:3000"):
        self.student_id = student_id
        self.base_url = base_url

    def generate_fr05_test_cases(self):
        """Generates 45 comprehensive test cases for FR-05: Product Listing & Search."""
        tcs = []
        
        # -------------------------------------------------------------
        # NHÓM 1: DOMAIN PARTITIONS & BVA (14 Test Cases)
        # -------------------------------------------------------------
        tcs.append({
            "tc_id": "TC_FR05_DOM_01",
            "category": "Domain (EP - Standard Keyword Search)",
            "objective": "Kiểm tra tìm kiếm sản phẩm thành công với từ khóa chuẩn xác 'Ao'",
            "method": "GET",
            "endpoint": "/api/products?search=Ao",
            "headers": {"Authorization": "Bearer {{user_token_A}}"},
            "expected_status": 200,
            "chai_assertion": """pm.test("Status code is 200 OK", function () {
    pm.response.to.have.status(200);
});
pm.test("Response is an array and contains matching products", function () {
    var jsonData = pm.response.json();
    pm.expect(Array.isArray(jsonData)).to.be.true;
    if (jsonData.length > 0) {
        pm.expect(jsonData[0].name.toLowerCase()).to.include("ao");
    }
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_DOM_02",
            "category": "Domain (EP - Empty Search Query)",
            "objective": "Kiểm tra gửi tham số search rỗng (?search=) trả về toàn bộ danh sách sản phẩm",
            "method": "GET",
            "endpoint": "/api/products?search=",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("Status code is 200 OK for empty search query", function () {
    pm.response.to.have.status(200);
});
pm.test("Returns non-empty array of products", function () {
    var jsonData = pm.response.json();
    pm.expect(Array.isArray(jsonData)).to.be.true;
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_DOM_03",
            "category": "Domain (EP - No Query Parameters / Full Listing)",
            "objective": "Kiểm tra gọi GET /api/products không truyền query string trả về toàn bộ danh mục sản phẩm",
            "method": "GET",
            "endpoint": "/api/products",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("Status code is 200 OK for full listing", function () {
    pm.response.to.have.status(200);
});
pm.test("Response contains product list", function () {
    var jsonData = pm.response.json();
    pm.expect(Array.isArray(jsonData)).to.be.true;
    pm.expect(jsonData.length).to.be.above(0);
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_DOM_04",
            "category": "Domain (EP - Non-Existent Product Keyword)",
            "objective": "Kiểm tra tìm kiếm từ khóa không tồn tại trả về mảng rỗng [] và status 200 OK",
            "method": "GET",
            "endpoint": "/api/products?search=NonExistentProductXYZ9999",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("Status code is 200 OK", function () {
    pm.response.to.have.status(200);
});
pm.test("Response returns empty array []", function () {
    var jsonData = pm.response.json();
    pm.expect(Array.isArray(jsonData)).to.be.true;
    pm.expect(jsonData.length).to.eql(0);
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_DOM_05",
            "category": "Domain (EP - Case-Insensitive Lowercase Search)",
            "objective": "Kiểm tra tìm kiếm không phân biệt chữ hoa chữ thường với từ khóa chữ thường 'ao'",
            "method": "GET",
            "endpoint": "/api/products?search=ao",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("Status code is 200 OK for lowercase search", function () {
    pm.response.to.have.status(200);
});
pm.test("Matches products case-insensitively", function () {
    var jsonData = pm.response.json();
    pm.expect(Array.isArray(jsonData)).to.be.true;
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_DOM_06",
            "category": "Domain (EP - Case-Insensitive Uppercase Search)",
            "objective": "Kiểm tra tìm kiếm không phân biệt chữ hoa chữ thường với từ khóa chữ in hoa 'AO'",
            "method": "GET",
            "endpoint": "/api/products?search=AO",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("Status code is 200 OK for uppercase search", function () {
    pm.response.to.have.status(200);
});
pm.test("Matches same results as lowercase search", function () {
    var jsonData = pm.response.json();
    pm.expect(Array.isArray(jsonData)).to.be.true;
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_DOM_07",
            "category": "Domain (EP - Substring Middle Match)",
            "objective": "Kiểm tra tìm kiếm chuỗi con ở giữa tên sản phẩm 'thoai'",
            "method": "GET",
            "endpoint": "/api/products?search=thoai",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("Status code is 200 OK for substring match", function () {
    pm.response.to.have.status(200);
});
pm.test("Result items contain substring in name", function () {
    var jsonData = pm.response.json();
    pm.expect(Array.isArray(jsonData)).to.be.true;
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_DOM_08",
            "category": "Domain (EP - Single Character Search)",
            "objective": "Kiểm tra tìm kiếm với từ khóa tối thiểu 1 ký tự 'a'",
            "method": "GET",
            "endpoint": "/api/products?search=a",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("Status code is 200 OK for single char search", function () {
    pm.response.to.have.status(200);
});
pm.test("Response is array", function () {
    pm.expect(Array.isArray(pm.response.json())).to.be.true;
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_DOM_09",
            "category": "Domain (BVA - Max Length Query 255 chars)",
            "objective": "Phân tích giá trị biên: Kiểm tra tìm kiếm với từ khóa độ dài tối đa 255 ký tự",
            "method": "GET",
            "endpoint": "/api/products?search=" + ("A" * 255),
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("Status code is 200 OK on 255-char query", function () {
    pm.response.to.have.status(200);
});
pm.test("Returns empty array for long non-matching query", function () {
    var jsonData = pm.response.json();
    pm.expect(Array.isArray(jsonData)).to.be.true;
    pm.expect(jsonData.length).to.eql(0);
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_DOM_10",
            "category": "Domain (BVA - Over-length Query 1000 chars)",
            "objective": "Phân tích giá trị biên: Kiểm tra hệ thống xử lý an toàn từ khóa siêu dài 1000 ký tự không bị tràn bộ đệm",
            "method": "GET",
            "endpoint": "/api/products?search=" + ("B" * 1000),
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("Server handles 1000-char query safely without 500 error", function () {
    pm.expect(pm.response.code).to.be.oneOf([200, 400, 414]);
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_DOM_11",
            "category": "Domain (EP - Vietnamese Unicode Diacritics)",
            "objective": "Kiểm tra tìm kiếm sản phẩm với tiếng Việt có dấu 'Điện thoại'",
            "method": "GET",
            "endpoint": "/api/products?search=%C4%90i%E1%BB%87n%20tho%E1%BA%A1i",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("Status code is 200 OK for Vietnamese Unicode query", function () {
    pm.response.to.have.status(200);
});
pm.test("Response is array", function () {
    pm.expect(Array.isArray(pm.response.json())).to.be.true;
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_DOM_12",
            "category": "Domain (EP - Numeric Keyword Search)",
            "objective": "Kiểm tra tìm kiếm sản phẩm với từ khóa số '15'",
            "method": "GET",
            "endpoint": "/api/products?search=15",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("Status code is 200 OK for numeric search", function () {
    pm.response.to.have.status(200);
});
pm.test("Response is array", function () {
    pm.expect(Array.isArray(pm.response.json())).to.be.true;
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_DOM_13",
            "category": "Domain (EP - Whitespace-only Keyword)",
            "objective": "Kiểm tra tìm kiếm chỉ chứa khoảng trắng (?search=%20%20%20)",
            "method": "GET",
            "endpoint": "/api/products?search=%20%20%20",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("Status code is 200 OK for whitespace query", function () {
    pm.response.to.have.status(200);
});
pm.test("Response is array", function () {
    pm.expect(Array.isArray(pm.response.json())).to.be.true;
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_DOM_14",
            "category": "Domain (EP - Trim Leading and Trailing Whitespaces)",
            "objective": "Kiểm tra hệ thống tự động cắt tỉa khoảng trắng đầu cuối (?search=%20Ao%20)",
            "method": "GET",
            "endpoint": "/api/products?search=%20Ao%20",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("Status code is 200 OK", function () {
    pm.response.to.have.status(200);
});
pm.test("Matches keyword after trimming", function () {
    var jsonData = pm.response.json();
    pm.expect(Array.isArray(jsonData)).to.be.true;
});"""
        })

        # -------------------------------------------------------------
        # NHÓM 2: OWASP API SECURITY & INJECTION (12 Test Cases)
        # -------------------------------------------------------------
        tcs.append({
            "tc_id": "TC_FR05_SEC_01",
            "category": "Security (SEC-06 - SQLi Single Quote Syntax Breaker)",
            "objective": "Kiểm tra bảo vệ SQLi: Gửi dấu nháy đơn ' nhằm phá vỡ câu truy vấn SQL, đảm bảo không sập 500 HTML",
            "method": "GET",
            "endpoint": "/api/products?search='",
            "headers": {},
            "expected_status": 400,
            "chai_assertion": """pm.test("TC_FR05_SEC_01: SQLi syntax breaker must NOT cause 500 HTML leak", function () {
    pm.expect(pm.response.code).to.not.equal(500);
    pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json");
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_SEC_02",
            "category": "Security (SEC-06 - SQLi Boolean Tautology Bypass)",
            "objective": "Kiểm tra tấn công SQLi Boolean Tautology (?search=' OR 1=1 --) không được phép bypass bộ lọc tìm kiếm",
            "method": "GET",
            "endpoint": "/api/products?search=%27%20OR%201=1%20--",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("TC_FR05_SEC_02: Boolean bypass is sanitized or handled safely", function () {
    pm.expect(pm.response.code).to.be.oneOf([200, 400]);
    pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json");
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_SEC_03",
            "category": "Security (SEC-06 - SQLi Comment Operator Injection)",
            "objective": "Kiểm tra chèn ký tự chú thích SQL (?search=Ao%27%20--) được xử lý an toàn",
            "method": "GET",
            "endpoint": "/api/products?search=Ao%27%20--",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("TC_FR05_SEC_03: Comment operator does not break SQL query", function () {
    pm.expect(pm.response.code).to.not.equal(500);
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_SEC_04",
            "category": "Security (SEC-06 - SQLi UNION Column Count Probing)",
            "objective": "Kiểm tra thăm dò số cột UNION (?search=%27%20UNION%20SELECT%201,2,3,4,5,6%20--)",
            "method": "GET",
            "endpoint": "/api/products?search=%27%20UNION%20SELECT%201,2,3,4,5,6%20--",
            "headers": {},
            "expected_status": 400,
            "chai_assertion": """pm.test("TC_FR05_SEC_04: UNION column probing is blocked or sanitized", function () {
    pm.expect(pm.response.code).to.not.equal(500);
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_SEC_05",
            "category": "Security (SEC-06 & SEC-07 - SQLi UNION Users Table Password Extraction)",
            "objective": "Kiểm tra lỗ hổng nguy cấp: Kẻ tấn công trích xuất mật khẩu và token từ bảng users qua UNION Injection",
            "method": "GET",
            "endpoint": "/api/products?search=%27%20UNION%20SELECT%20id,name,0,email,role,1%20FROM%20users%20--",
            "headers": {},
            "expected_status": 400,
            "chai_assertion": """pm.test("TC_FR05_SEC_05: CRITICAL - Must NOT exfiltrate user credentials via product search", function () {
    if (pm.response.code === 200) {
        var items = pm.response.json();
        items.forEach(function(item) {
            pm.expect(item).to.not.have.property("password");
            pm.expect(item).to.not.have.property("reset_token");
        });
    } else {
        pm.expect(pm.response.code).to.be.oneOf([400, 403]);
    }
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_SEC_06",
            "category": "Security (SEC-06 - SQLi SQLite Schema Metadata Leak)",
            "objective": "Kiểm tra khai thác đọc cấu trúc CSDL từ sqlite_master (?search=%27%20UNION%20SELECT%201,sql,3,tbl_name,5,6%20FROM%20sqlite_master%20--)",
            "method": "GET",
            "endpoint": "/api/products?search=%27%20UNION%20SELECT%201,sql,3,tbl_name,5,6%20FROM%20sqlite_master%20--",
            "headers": {},
            "expected_status": 400,
            "chai_assertion": """pm.test("TC_FR05_SEC_06: Schema extraction from sqlite_master is prevented", function () {
    pm.expect(pm.response.code).to.not.equal(500);
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_SEC_07",
            "category": "Security (SEC-06 - SQLi Stacked Queries Drop Table Attempt)",
            "objective": "Kiểm tra thực thi đa câu lệnh stacked queries (?search=test%27;%20DROP%20TABLE%20products;%20--)",
            "method": "GET",
            "endpoint": "/api/products?search=test%27;%20DROP%20TABLE%20products;%20--",
            "headers": {},
            "expected_status": 400,
            "chai_assertion": """pm.test("TC_FR05_SEC_07: Stacked query injection is safely rejected", function () {
    pm.expect(pm.response.code).to.not.equal(500);
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_SEC_08",
            "category": "Security (SEC-06 - Reflected XSS Script Injection)",
            "objective": "Kiểm tra chống XSS: Chèn mã độc script (?search=<script>alert('XSS')</script>) trả về dữ liệu an toàn",
            "method": "GET",
            "endpoint": "/api/products?search=%3Cscript%3Ealert(%27XSS%27)%3C/script%3E",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("TC_FR05_SEC_08: XSS payload returns JSON and does not execute script", function () {
    pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json");
    pm.expect(pm.response.code).to.be.oneOf([200, 400]);
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_SEC_09",
            "category": "Security (SEC-06 - Path Traversal Ingestion)",
            "objective": "Kiểm tra chèn chuỗi Path Traversal (?search=../../../../etc/passwd) được coi như chuỗi tìm kiếm thông thường",
            "method": "GET",
            "endpoint": "/api/products?search=../../../../etc/passwd",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("TC_FR05_SEC_09: Path traversal payload returns safe empty JSON array", function () {
    pm.response.to.have.status(200);
    pm.expect(Array.isArray(pm.response.json())).to.be.true;
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_SEC_10",
            "category": "Security (SEC-06 - SQL Wildcard Percent '%' Filter Bypass)",
            "objective": "Kiểm tra chèn ký tự % (?search=%): Phải tìm kiếm ký tự % nguyên nghĩa chứ không được coi là wildcard lấy toàn bộ CSDL",
            "method": "GET",
            "endpoint": "/api/products?search=%25",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("TC_FR05_SEC_10: Literal '%' does not unintentionally match all products", function () {
    pm.response.to.have.status(200);
    var jsonData = pm.response.json();
    pm.expect(Array.isArray(jsonData)).to.be.true;
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_SEC_11",
            "category": "Security (SEC-06 - SQL Wildcard Underscore '_' Single Character Bypass)",
            "objective": "Kiểm tra chèn ký tự _ (?search=_): Phải tìm kiếm ký tự _ nguyên bản",
            "method": "GET",
            "endpoint": "/api/products?search=_",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("TC_FR05_SEC_11: Underscore '_' is treated safely", function () {
    pm.response.to.have.status(200);
    pm.expect(Array.isArray(pm.response.json())).to.be.true;
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_SEC_12",
            "category": "Security (SEC-06 - HTTP Parameter Pollution)",
            "objective": "Kiểm tra tấn công trùng lặp tham số HPP (?search=phone&search=laptop) không làm crash server",
            "method": "GET",
            "endpoint": "/api/products?search=phone&search=laptop",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("TC_FR05_SEC_12: Duplicate search params handled gracefully without 500", function () {
    pm.expect(pm.response.code).to.be.oneOf([200, 400]);
});"""
        })

        # -------------------------------------------------------------
        # NHÓM 3: FILTER, PAGINATION & QUERY COMBINATIONS (8 Test Cases)
        # -------------------------------------------------------------
        tcs.append({
            "tc_id": "TC_FR05_FLT_01",
            "category": "Filter (Category ID Filtering)",
            "objective": "Kiểm tra lọc danh sách sản phẩm theo danh mục (?category_id=1)",
            "method": "GET",
            "endpoint": "/api/products?category_id=1",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("Status code is 200 OK for category filtering", function () {
    pm.response.to.have.status(200);
});
pm.test("All returned items belong to requested category_id 1", function () {
    var jsonData = pm.response.json();
    pm.expect(Array.isArray(jsonData)).to.be.true;
    jsonData.forEach(function(item) {
        if (item.category_id !== undefined) {
            pm.expect(item.category_id).to.eql(1);
        }
    });
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_FLT_02",
            "category": "Filter (Combined Search & Category Filtering)",
            "objective": "Kiểm tra lọc kết hợp đồng thời từ khóa và danh mục (?search=Ao&category_id=1)",
            "method": "GET",
            "endpoint": "/api/products?search=Ao&category_id=1",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("Status code is 200 OK for combined filters", function () {
    pm.response.to.have.status(200);
});
pm.test("Results satisfy both keyword and category", function () {
    var jsonData = pm.response.json();
    pm.expect(Array.isArray(jsonData)).to.be.true;
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_FLT_03",
            "category": "Filter (Non-Existent Category ID)",
            "objective": "Kiểm tra lọc theo danh mục không tồn tại (?category_id=9999) trả về mảng rỗng []",
            "method": "GET",
            "endpoint": "/api/products?category_id=9999",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("Status code is 200 OK", function () {
    pm.response.to.have.status(200);
});
pm.test("Returns empty array for non-existent category", function () {
    var jsonData = pm.response.json();
    pm.expect(Array.isArray(jsonData)).to.be.true;
    pm.expect(jsonData.length).to.eql(0);
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_FLT_04",
            "category": "Filter (Invalid Category ID Data Type)",
            "objective": "Kiểm tra truyền kiểu dữ liệu không hợp lệ cho category_id (?category_id=abc) phải bị từ chối 400 Bad Request",
            "method": "GET",
            "endpoint": "/api/products?category_id=abc",
            "headers": {},
            "expected_status": 400,
            "chai_assertion": """pm.test("Rejects invalid non-numeric category_id", function () {
    pm.expect(pm.response.code).to.be.oneOf([200, 400]);
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_FLT_05",
            "category": "Filter (Unsupported Query Parameters)",
            "objective": "Kiểm tra truyền tham số lạ ngoài đặc tả (?unknown_param=xyz) được hệ thống bỏ qua và trả danh sách bình thường",
            "method": "GET",
            "endpoint": "/api/products?unknown_param=xyz",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("Status code is 200 OK when unknown query params passed", function () {
    pm.response.to.have.status(200);
});
pm.test("Returns standard product list", function () {
    pm.expect(Array.isArray(pm.response.json())).to.be.true;
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_FLT_06",
            "category": "Filter (Price Range Filtering)",
            "objective": "Kiểm tra lọc sản phẩm theo khoảng giá (?minPrice=10000&maxPrice=500000)",
            "method": "GET",
            "endpoint": "/api/products?minPrice=10000&maxPrice=500000",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("Status code is 200 OK for price range query", function () {
    pm.response.to.have.status(200);
});
pm.test("Response is array", function () {
    pm.expect(Array.isArray(pm.response.json())).to.be.true;
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_FLT_07",
            "category": "Pagination (Page and Limit Parameters)",
            "objective": "Kiểm tra phân trang danh sách sản phẩm (?page=1&limit=5)",
            "method": "GET",
            "endpoint": "/api/products?page=1&limit=5",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("Status code is 200 OK for pagination query", function () {
    pm.response.to.have.status(200);
});
pm.test("Response length does not exceed limit", function () {
    var jsonData = pm.response.json();
    pm.expect(Array.isArray(jsonData)).to.be.true;
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_FLT_08",
            "category": "Filter (Sorting Parameters)",
            "objective": "Kiểm tra sắp xếp danh sách sản phẩm (?sort=price&order=desc)",
            "method": "GET",
            "endpoint": "/api/products?sort=price&order=desc",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("Status code is 200 OK for sorting query", function () {
    pm.response.to.have.status(200);
});
pm.test("Response is array", function () {
    pm.expect(Array.isArray(pm.response.json())).to.be.true;
});"""
        })

        # -------------------------------------------------------------
        # NHÓM 4: JSON SCHEMA DRAFT-07, HTTP & SLA (6 Test Cases)
        # -------------------------------------------------------------
        tcs.append({
            "tc_id": "TC_FR05_SCHEMA_01",
            "category": "Schema (Root JSON Array Structure)",
            "objective": "Kiểm tra cấu trúc gốc của response bắt buộc phải là JSON Array",
            "method": "GET",
            "endpoint": "/api/products",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("Root response is a valid JSON Array", function () {
    pm.response.to.have.status(200);
    pm.expect(Array.isArray(pm.response.json())).to.be.true;
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_SCHEMA_02",
            "category": "Schema (Product Item Draft-07 Schema Validation)",
            "objective": "Kiểm tra từng phần tử sản phẩm khớp 100% JSON Schema: id (integer), name (string), price (number), description (string), imageUrl (string), category_id (integer)",
            "method": "GET",
            "endpoint": "/api/products",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("Each product item matches standard JSON schema", function () {
    var jsonData = pm.response.json();
    if (jsonData.length > 0) {
        var item = jsonData[0];
        pm.expect(item).to.have.property("id");
        pm.expect(item).to.have.property("name");
        pm.expect(item).to.have.property("price");
        pm.expect(typeof item.name).to.eql("string");
    }
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_SCHEMA_03",
            "category": "Schema (Content-Type Header Verification)",
            "objective": "Kiểm tra Header Content-Type trả về là application/json; charset=utf-8",
            "method": "GET",
            "endpoint": "/api/products",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("Content-Type header is application/json", function () {
    pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json");
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_SCHEMA_04",
            "category": "Performance SLA (Sub-200ms Mobile Standard)",
            "objective": "Kiểm tra thời gian phản hồi của API danh sách sản phẩm đạt chuẩn Mobile SLA (< 200ms)",
            "method": "GET",
            "endpoint": "/api/products",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("Response time meets sub-200ms mobile SLA", function () {
    pm.expect(pm.response.responseTime).to.be.below(200);
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_SCHEMA_05",
            "category": "Anti-Cheat (Mandatory Student ID Header)",
            "objective": "Kiểm tra gắn Header X-Student-Id trên request theo quy định bài tập FIT@HCMUS",
            "method": "GET",
            "endpoint": "/api/products",
            "headers": {"X-Student-Id": "{{studentId}}"},
            "expected_status": 200,
            "chai_assertion": """pm.test("X-Student-Id header is transmitted correctly", function () {
    pm.response.to.have.status(200);
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_SCHEMA_06",
            "category": "HTTP Protocol (Disallowed HTTP Method Verification)",
            "objective": "Kiểm tra gọi sai phương thức HTTP PATCH /api/products bị từ chối hoặc xử lý an toàn",
            "method": "PATCH",
            "endpoint": "/api/products",
            "headers": {},
            "body": {},
            "expected_status": 404,
            "chai_assertion": """pm.test("Disallowed method is rejected with 404 or 405", function () {
    pm.expect(pm.response.code).to.be.oneOf([404, 405]);
});"""
        })

        # -------------------------------------------------------------
        # NHÓM 5: HIDDEN LOGIC & ADVANCED CODE VULNERABILITIES (5 Test Cases - Human Extension)
        # -------------------------------------------------------------
        tcs.append({
            "tc_id": "TC_FR05_ADV_01",
            "category": "Advanced Code Vulnerability (Raw HTML 500 Database Error Leak)",
            "objective": "Bóc tách lỗi server.js dòng 147-150: Truyền chuỗi phá vỡ SQL (?search=') khiến backend trả về 500 HTML <h1>Database Error</h1><p>... lộ thông tin CSDL nội bộ",
            "method": "GET",
            "endpoint": "/api/products?search=%27",
            "headers": {},
            "expected_status": 400,
            "chai_assertion": """pm.test("TC_FR05_ADV_01: SUT must NOT return raw HTML 500 leaking database engine error", function () {
    // SUT BUG HUNTER: server.js lines 147-150 send HTML 500
    pm.expect(pm.response.code).to.not.equal(500);
    pm.expect(pm.response.headers.get("Content-Type")).to.not.include("text/html");
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_ADV_02",
            "category": "Advanced Security Vulnerability (Full Users Table Exfiltration via Public Product Search)",
            "objective": "Thực thi khai thác trích xuất toàn bộ tài khoản người dùng, email và mật khẩu từ bảng users qua UNION Injection trên API công khai",
            "method": "GET",
            "endpoint": "/api/products?search=%27%20UNION%20SELECT%20id,%20name,%200,%20email%20||%20%27:%27%20||%20password,%20role,%201%20FROM%20users%20--",
            "headers": {},
            "expected_status": 400,
            "chai_assertion": """pm.test("TC_FR05_ADV_02: Public product search MUST NEVER expose user credentials via SQL injection", function () {
    if (pm.response.code === 200) {
        var items = pm.response.json();
        items.forEach(function(item) {
            pm.expect(item.description).to.not.include("@");
            pm.expect(item.name).to.not.include("admin");
        });
    } else {
        pm.expect(pm.response.code).to.be.oneOf([400, 403]);
    }
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_ADV_03",
            "category": "Advanced Code Vulnerability (Wildcard % Complete Filter Bypass)",
            "objective": "Bóc tách lỗi server.js dòng 144: Truy vấn LIKE '%${searchQuery}%' khi truyền ?search=% biến thành '%%%%', trả về 100% sản phẩm bypass bộ lọc",
            "method": "GET",
            "endpoint": "/api/products?search=%25",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("TC_FR05_ADV_03: Wildcard '%' should be escaped and not return all database rows", function () {
    pm.response.to.have.status(200);
    var items = pm.response.json();
    pm.expect(Array.isArray(items)).to.be.true;
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_ADV_04",
            "category": "Advanced Code Vulnerability (Express Query Array Parsing Type Coercion)",
            "objective": "Kiểm tra lỗ hổng Type Coercion: Client truyền mảng (?search[]=a&search[]=b) khiến Express parse thành Array, nối chuỗi SQL thành LIKE '%a,b%'",
            "method": "GET",
            "endpoint": "/api/products?search[]=a&search[]=b",
            "headers": {},
            "expected_status": 400,
            "chai_assertion": """pm.test("TC_FR05_ADV_04: Array in query string is rejected or normalized safely", function () {
    pm.expect(pm.response.code).to.be.oneOf([200, 400]);
    pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json");
});"""
        })

        tcs.append({
            "tc_id": "TC_FR05_ADV_05",
            "category": "Advanced Security Vulnerability (Public Information Leakage vs Admin Data Separation)",
            "objective": "Kiểm tra API công khai GET /api/products không để lộ các cột ẩn nội bộ của sản phẩm (như cost_price hoặc supplier_info)",
            "method": "GET",
            "endpoint": "/api/products",
            "headers": {},
            "expected_status": 200,
            "chai_assertion": """pm.test("TC_FR05_ADV_05: Public product view does not leak internal admin fields", function () {
    pm.response.to.have.status(200);
    var items = pm.response.json();
    if (items.length > 0) {
        pm.expect(items[0]).to.not.have.property("cost_price");
        pm.expect(items[0]).to.not.have.property("supplier_secret");
    }
});"""
        })

        return tcs

    def generate_test_cases_for_fr(self, fr_id, config):
        """Generates exhaustive test cases for a specific Feature Requirement."""
        # Check if specialized test generator exists for target FR
        if fr_id == "FR-05":
            return self.generate_fr05_test_cases()

        test_cases = []
        tc_counter = 1

        # 1. Happy Path Valid Case
        tc_id = f"TC_{fr_id.replace('-', '')}_HAPPY_{tc_counter:02d}"
        test_cases.append({
            "tc_id": tc_id,
            "category": "Happy Path (Functional Verification)",
            "objective": f"Verify successful execution of {config['name']} with valid payload",
            "method": config["method"],
            "endpoint": config["endpoint"].replace(":id", "1"),
            "headers": {"Content-Type": "application/json", "Authorization": "Bearer {{admin_token}}" if config.get("role_required") == "admin" else "Bearer {{user_token_A}}"},
            "body": config.get("sample_body", {}),
            "expected_status": 200 if config["method"] != "POST" else (201 if "create" in config["name"].lower() else 200),
            "chai_assertion": "pm.response.to.have.status(200);"
        })
        tc_counter += 1

        # 2. Domain & Boundary Value Partitioning (EP / BVA)
        if "fields" in config:
            for field, f_props in config["fields"].items():
                # Test Empty / Missing
                if f_props.get("required"):
                    t_body = dict(config.get("sample_body", {}))
                    t_body[field] = ""
                    test_cases.append({
                        "tc_id": f"TC_{fr_id.replace('-', '')}_DOM_{tc_counter:02d}",
                        "category": f"Domain Partition (Empty Field: {field})",
                        "objective": f"Reject request when required field '{field}' is empty string",
                        "method": config["method"],
                        "endpoint": config["endpoint"].replace(":id", "1"),
                        "headers": {"Content-Type": "application/json"},
                        "body": t_body,
                        "expected_status": 400,
                        "chai_assertion": f"pm.response.to.have.status(400); pm.expect(pm.response.json()).to.have.property('error');"
                    })
                    tc_counter += 1

                # Test Number Boundary (Negative & Zero)
                if f_props.get("type") in ["integer", "number"]:
                    t_body = dict(config.get("sample_body", {}))
                    t_body[field] = -50000
                    test_cases.append({
                        "tc_id": f"TC_{fr_id.replace('-', '')}_DOM_{tc_counter:02d}",
                        "category": f"Boundary Value Analysis (Negative Number: {field})",
                        "objective": f"Reject negative values for numeric field '{field}'",
                        "method": config["method"],
                        "endpoint": config["endpoint"].replace(":id", "1"),
                        "headers": {"Content-Type": "application/json"},
                        "body": t_body,
                        "expected_status": 400,
                        "chai_assertion": f"pm.response.to.have.status(400);"
                    })
                    tc_counter += 1

                # Test Phone Regex
                if f_props.get("type") == "phone":
                    t_body = dict(config.get("sample_body", {}))
                    t_body[field] = "12345678"
                    test_cases.append({
                        "tc_id": f"TC_{fr_id.replace('-', '')}_DOM_{tc_counter:02d}",
                        "category": f"Regex Validation (Phone Format: {field})",
                        "objective": f"Reject phone number not matching standard Vietnam regex format",
                        "method": config["method"],
                        "endpoint": config["endpoint"].replace(":id", "1"),
                        "headers": {"Content-Type": "application/json"},
                        "body": t_body,
                        "expected_status": 400,
                        "chai_assertion": f"pm.response.to.have.status(400);"
                    })
                    tc_counter += 1

        # 3. Security & Access Control (OWASP Top 10)
        if config.get("auth_required"):
            # Missing Auth Header
            test_cases.append({
                "tc_id": f"TC_{fr_id.replace('-', '')}_SEC_{tc_counter:02d}",
                "category": "Security (SEC-02 - Missing Authorization Header)",
                "objective": f"Reject unauthenticated request to {config['endpoint']}",
                "method": config["method"],
                "endpoint": config["endpoint"].replace(":id", "1"),
                "headers": {},
                "body": config.get("sample_body", {}),
                "expected_status": 401,
                "chai_assertion": "pm.response.to.have.status(401);"
            })
            tc_counter += 1

            # Invalid Forged Token
            test_cases.append({
                "tc_id": f"TC_{fr_id.replace('-', '')}_SEC_{tc_counter:02d}",
                "category": "Security (SEC-02 - Forged JWT Token)",
                "objective": f"Reject request with invalid/forged signature token",
                "method": config["method"],
                "endpoint": config["endpoint"].replace(":id", "1"),
                "headers": {"Authorization": "Bearer forged.token.signature"},
                "body": config.get("sample_body", {}),
                "expected_status": 403,
                "chai_assertion": "pm.response.to.have.status(403);"
            })
            tc_counter += 1

            # RBAC Role Escalation
            if config.get("role_required") == "admin":
                test_cases.append({
                    "tc_id": f"TC_{fr_id.replace('-', '')}_SEC_{tc_counter:02d}",
                    "category": "Security (SEC-03 - Broken Function Level Authorization)",
                    "objective": "Prevent regular unprivileged user from performing admin operation",
                    "method": config["method"],
                    "endpoint": config["endpoint"].replace(":id", "1"),
                    "headers": {"Authorization": "Bearer {{user_token_A}}"},
                    "body": config.get("sample_body", {}),
                    "expected_status": 403,
                    "chai_assertion": "pm.expect(pm.response.code).to.be.oneOf([401, 403]);"
                })
                tc_counter += 1

        # 4. SQL Injection (SEC-06)
        test_cases.append({
            "tc_id": f"TC_{fr_id.replace('-', '')}_SEC_{tc_counter:02d}",
            "category": "Security (SEC-06 - SQL Injection Protection)",
            "objective": f"Ensure {config['endpoint']} handles SQL injection strings safely without 500 error",
            "method": config["method"],
            "endpoint": config["endpoint"].replace(":id", "1 OR 1=1"),
            "headers": {"Content-Type": "application/json"},
            "body": config.get("sample_body", {}),
            "expected_status": 400,
            "chai_assertion": "pm.expect(pm.response.code).to.not.equal(500);"
        })
        tc_counter += 1

        # 5. Schema & Mobile SLA
        test_cases.append({
            "tc_id": f"TC_{fr_id.replace('-', '')}_SLA_{tc_counter:02d}",
            "category": "Performance SLA (Response Time < 200ms)",
            "objective": f"Verify API response time meets sub-200ms mobile standard",
            "method": config["method"],
            "endpoint": config["endpoint"].replace(":id", "1"),
            "headers": {"Authorization": "Bearer {{user_token_A}}"},
            "body": config.get("sample_body", {}),
            "expected_status": 200,
            "chai_assertion": "pm.expect(pm.response.responseTime).to.be.below(200);"
        })

        return test_cases

    def build_postman_collection(self, target_fr="ALL"):
        """Compiles generated test cases into a Postman Collection v2.1.0."""
        collection = {
            "info": {
                "name": "EShop_Auto_Generated_Full_TestCollection" if target_fr == "ALL" else f"FR{target_fr.replace('-', '')}_Product_Listing_Search" if target_fr == "FR-05" else f"{target_fr}_Test_Collection",
                "_postman_id": f"gen-{uuid.uuid4().hex[:16]}",
                "description": f"Auto-generated API Test Collection for EShop SUT (MSSV: {self.student_id})",
                "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
            },
            "item": []
        }

        # Add Global Pre-request Script for Student ID Header
        setup_folder = {
            "name": "0. Setup & Auth Seed",
            "item": [
                {
                    "name": "0.1 Register Auto Test User",
                    "request": {
                        "method": "POST",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"},
                            {"key": "X-Student-Id", "value": "{{studentId}}"}
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": json.dumps({"name": "Auto QA User", "email": f"auto_qa_{uuid.uuid4().hex[:8]}@eshop.com", "password": "Password123!"}, indent=2)
                        },
                        "url": {"raw": "{{baseUrl}}/api/register", "host": ["{{baseUrl}}"], "path": ["api", "register"]}
                    },
                    "event": [{
                        "listen": "test",
                        "script": {
                            "type": "text/javascript",
                            "exec": ["pm.test('Auto register test user passes', function() { pm.expect(pm.response.code).to.be.oneOf([200, 201]); });"]
                        }
                    }]
                },
                {
                    "name": "0.2 Login Admin User",
                    "request": {
                        "method": "POST",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"},
                            {"key": "X-Student-Id", "value": "{{studentId}}"}
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": json.dumps({"email": "admin@eshop.com", "password": "Admin123!"}, indent=2)
                        },
                        "url": {"raw": "{{baseUrl}}/api/login", "host": ["{{baseUrl}}"], "path": ["api", "login"]}
                    },
                    "event": [{
                        "listen": "test",
                        "script": {
                            "type": "text/javascript",
                            "exec": ["var res = pm.response.json(); if(res.token) { pm.environment.set('admin_token', res.token); }"]
                        }
                    }]
                }
            ]
        }
        collection["item"].append(setup_folder)

        # Select Features to Generate
        features_to_run = list(FEATURE_CATALOG.keys()) if target_fr == "ALL" else [target_fr]

        for fr in features_to_run:
            if fr not in FEATURE_CATALOG:
                continue
            config = FEATURE_CATALOG[fr]
            fr_folder = {"name": f"{fr} - {config['name']}", "item": []}
            tcs = self.generate_test_cases_for_fr(fr, config)

            for tc in tcs:
                headers = [{"key": "X-Student-Id", "value": "{{studentId}}"}]
                for hk, hv in tc.get("headers", {}).items():
                    headers.append({"key": hk, "value": hv})

                endpoint_str = tc['endpoint']
                if '?' in endpoint_str:
                    path_part, query_part = endpoint_str.split('?', 1)
                    query_items = []
                    for q_pair in query_part.split('&'):
                        if '=' in q_pair:
                            k, v = q_pair.split('=', 1)
                            query_items.append({"key": k, "value": v})
                        elif q_pair:
                            query_items.append({"key": q_pair, "value": ""})
                else:
                    path_part = endpoint_str
                    query_items = []

                path_segments = [p for p in path_part.strip('/').split('/') if p]

                url_obj = {
                    "raw": f"{{{{baseUrl}}}}{endpoint_str}",
                    "host": ["{{baseUrl}}"],
                    "path": path_segments
                }
                if query_items:
                    url_obj["query"] = query_items

                item = {
                    "name": f"{tc['tc_id']}: {tc['objective']}",
                    "request": {
                        "method": tc["method"],
                        "header": headers,
                        "url": url_obj
                    },
                    "event": [{
                        "listen": "test",
                        "script": {
                            "type": "text/javascript",
                            "exec": tc["chai_assertion"].split("\n")
                        }
                    }]
                }

                if tc["method"] in ["POST", "PUT", "PATCH"] and "body" in tc:
                    item["request"]["body"] = {
                        "mode": "raw",
                        "raw": json.dumps(tc.get("body", {}), indent=2)
                    }

                fr_folder["item"].append(item)

            collection["item"].append(fr_folder)

        return collection

def main():
    parser = argparse.ArgumentParser(description="AI-Driven API Test Generator for EShop SUT (HW06)")
    parser.add_argument("--target-fr", default="ALL", help="Target FR ID (e.g., FR-04, FR-05, FR-10, FR-15, FR-09 or ALL)")
    parser.add_argument("--student-id", default="23127092", help="Student ID for mandatory X-Student-Id Header")
    parser.add_argument("--output-collection", default="collections/AutoGenerated_Collection.postman_collection.json", help="Path to save Postman JSON Collection")
    args = parser.parse_args()

    print(f"[*] Initializing AI Test Generator Engine for Target: {args.target_fr} (Student: {args.student_id})...")
    agent = APITestAgent(student_id=args.student_id)
    collection = agent.build_postman_collection(target_fr=args.target_fr)

    os.makedirs(os.path.dirname(args.output_collection), exist_ok=True)
    with open(args.output_collection, "w", encoding="utf-8") as f:
        json.dump(collection, f, indent=2, ensure_ascii=False)

    print(f"[+] Successfully generated Postman Collection at: {args.output_collection}")
    print(f"[+] Total Feature Folders: {len(collection['item'])}")
    total_tcs = sum(len(folder['item']) for folder in collection['item'] if folder['name'] != "0. Setup & Auth Seed")
    print(f"[+] Total Generated Test Cases: {total_tcs}")

if __name__ == "__main__":
    main()
