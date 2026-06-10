# F.R.I.D.A.Y - Trợ Lý Cá Nhân AI Toàn Năng

**F.R.I.D.A.Y** (Female Replacement Intelligent Digital Assistant Youth) là một trợ lý ảo cá nhân được xây dựng trên ngôn ngữ Python, hỗ trợ tương tác giọng nói, thực thi các lệnh hệ thống và truy cập mô hình ngôn ngữ lớn (LLM) cục bộ thông qua Ollama. Dự án đã được tối ưu hóa theo thiết kế Modular hướng đối tượng và cơ chế Dependency Injection.

---

## 🤖 Tính năng nổi bật
- **Trí tuệ nhân tạo cục bộ (Local AI):** Tích hợp Ollama để gọi LLM ngoại tuyến (mặc định sử dụng `phi3:mini`).
- **Quản lý bộ nhớ:** Bộ nhớ lịch sử trò chuyện dài hạn được lưu trữ dưới dạng JSON, tự động tối ưu hóa số lượng tin nhắn (`max_history`).
- **Giao diện dòng lệnh trực quan:** Hỗ trợ điều khiển bằng văn bản tiếng Việt và tích hợp kiểm soát an toàn bảo mật.
- **Hệ thống công cụ (Agent Tools):** Khả năng tự động đọc/ghi file hệ thống, tìm kiếm web qua DuckDuckGo và thực thi các lệnh shell (yêu cầu Boss phê duyệt).
- **Hạ tầng âm thanh (Sắp hoạt động lại):** Quản lý micro và tổng hợp giọng nói ngoại tuyến qua Vosk và TTS.

---

## ⚡ Hướng dẫn cài đặt và khởi chạy nhanh

### 1. Cài đặt môi trường
Yêu cầu Python 3.12+ và Ollama đã được cài đặt trên máy của bạn.

```bash
# Clone repository
git clone <repository-url>
cd friday

# Khởi tạo và kích hoạt môi trường ảo (Windows)
python -m venv venv
venv\Scripts\Activate.ps1

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# Copy tệp cấu hình môi trường
copy .env.example .env
```
*(Hãy cấu hình lại các thông số như `AI_NAME`, `BOSS_NAME` trong tệp `.env` nếu cần)*

### 2. Khởi động AI
```bash
# Terminal 1: Chạy dịch vụ Ollama
ollama serve

# Terminal 2: Tải mô hình mặc định (chỉ chạy lần đầu)
ollama pull phi3:mini

# Terminal 3: Chạy ứng dụng trợ lý ảo
$env:PYTHONIOENCODING="utf-8"
python main.py
```

---

## 🛠️ Danh sách lệnh đặc biệt trên CLI

Các lệnh đặc biệt bắt đầu bằng dấu `/`. Hệ thống sẽ chặn và xử lý trực tiếp thay vì chuyển qua cho AI:

| Lệnh | Chức năng | Ví dụ |
| :--- | :--- | :--- |
| `/help` | Hiển thị tất cả hướng dẫn lệnh đặc biệt | `/help` |
| `/status` | Xem trạng thái hệ thống (Boss, Mode, bộ nhớ, TODO) | `/status` |
| `/clear` | Xóa sạch lịch sử hội thoại đã lưu | `/clear` |
| `/check-files` | Liệt kê các tệp đang lưu trữ trong thư mục dữ liệu (`DATA_DIR`) | `/check-files` |
| `/search <keyword>`| Tìm kiếm nhanh thông tin trên Internet | `/search xu hướng AI` |
| `/mode <name>` | Đọc hoặc thay đổi chế độ hoạt động | `/mode think` |
| `/todo [list]` | Xem danh sách việc cần làm (TODO) | `/todo list` |
| `/todo add <txt>`| Thêm một công việc mới vào danh sách TODO | `/todo add mua sữa` |
| `/voice on/off` | Bật hoặc tắt thiết bị nhận diện giọng nói | `/voice off` |
| `/bye` (hoặc `/exit`) | Thoát khỏi chương trình trợ lý ảo | `/exit` |

---

## 💻 Hướng dẫn phát triển và kiểm thử
Xem chi tiết tại [DEVELOPMENT.md](docs/DEVELOPMENT.md) để hiểu về:
- Sơ đồ kiến trúc thiết kế Dependency Injection & Composition Root.
- Cách chạy bộ kiểm thử tự động `unittest` cô lập (16 test case).
- Cách viết và đăng ký thêm công cụ (tool) mới bằng decorator `@register_tool`.

---

## 📄 Bản quyền
Dự án được phân phối dưới giấy phép MIT. Xem chi tiết tại tệp `LICENSE`.
