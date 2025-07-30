# 🛠️ ETL Pipeline với Apache Airflow

## 🚀 Giới thiệu 
Dự án này sử dụng **Apache Airflow** để triển khai các pipeline xử lý dữ liệu (ETL) một cách tự động, dễ quản lý và dễ mở rộng.

Mỗi pipeline được định nghĩa dưới dạng một **DAG** (Directed Acyclic Graph) trong thư mục `dags/`, với khả năng lập lịch, theo dõi trạng thái, kiểm soát lỗi, và ghi log chi tiết.

---

### 🧩 ETL Pipeline Basic

Pipeline này gồm 3 bước chính:

1. **Extract**  
   - Gọi API `http://universities.hipolabs.com/search?country=United+States`  
2. **Transform**  
   - Lọc ra các trường có chứa từ khóa `"California"`  
   - Làm sạch dữ liệu: nối `domains` và `web_pages` thành chuỗi  
3. **Load**  
   - Ghi kết quả vào bảng `cal_uni` trong PostgreSQL thông qua SQLAlchemy

Pipeline này chạy tự động mỗi ngày với lịch `@daily` và có thể mở rộng cho các use case ETL thực tế.

---

## ⚙️ Cách sử dụng

### 🔹 Bước 1: Tạo và kích hoạt môi trường ảo (venv)

```bash
# Tạo môi trường ảo Python
python -m venv venv

# Kích hoạt môi trường (tùy hệ điều hành)

# Windows:
venv\Scripts\activate

# macOS / Linux:
source venv/bin/activate
```

---

### 🔹 Bước 2: Cài đặt các thư viện cần thiết

```bash
pip install -r requirements.txt
```

---

### 🔹 Bước 3: Tạo file `.env` để cấu hình kết nối cơ sở dữ liệu

Tạo file `.env` ở thư mục gốc với nội dung:

```
DB_USER=airflow
DB_PASSWORD=airflow
DB_HOST=postgres
DB_PORT=5432
DB_DATABASE=airflow
```

---

### 🔹 Bước 4: Khởi động hệ thống bằng Docker Compose

```bash
docker compose up --build -d
```

Lệnh này sẽ khởi chạy các container:
- PostgreSQL
- Redis
- Airflow Webserver
- Airflow Scheduler

---

### 🔹 Bước 5: Truy cập giao diện Airflow

- Truy cập: http://localhost:8080
- Tài khoản mặc định:
  - **Username**: `airflow`
  - **Password**: `airflow`

---

### 🔹 Bước 6: Bật và chạy DAG `ETL_Basic`

1. Vào giao diện Airflow
2. Bật DAG `ETL_Basic` (gạt công tắc bên trái)
3. Nhấn nút ▶ để chạy DAG thủ công hoặc đợi chạy tự động mỗi ngày

---

## ✅ Kiểm tra kết quả

### Dùng dòng lệnh:

```bash
docker exec -it <container_id_postgres> psql -U airflow airflow
```

```sql
SELECT * FROM cal_uni LIMIT 10;
```

### Hoặc dùng DBeaver  để xem bảng `cal_uni` trong PostgreSQL.

#### Bước 1: Để dùng DBeaver kết nối với Container Postgres cần tắt Postgres ở local.
```bash
Search -> Services -> postgresql-x64 -> Right Click -> Stop.
```

#### Bước 2: Sau khi đăng nhập vào Web UI Airflow tiếp tục:
```bash 
Admin -> Connection -> Add Connection.
Conn_id = postgres_host
Conn_type = postgres
host = postgres
login = airflow
password = airflow
database = airflow
port = 5432
-> Save
```

#### Bước 3: Vào DBeaver 
```bash
New Database Connection (Ctrl + Shift + N) -> PostgreSQL
Host=localhost
Database=airflow
Port=5432
Username=airflow
Password=airflow
-> Finish -> New SQL Script (Ctrl + ])
```
```sql
SELECT * FROM cal_uni;
```

---

