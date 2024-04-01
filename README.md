# Dự báo doanh thu trong tương lai bằng mô hình ARIMA, phân tệp khách hàng dựa trên mô hình RFM và dự đoán doanh thu của từng khách hàng qua mô hình deep leanirng
Dựa trên tập dữ liệu của cuộc thi Data Got Talent 2023, chúng em thực hiện tiền xử lý dữ liệu và phân khúc khách hàng theo 12 nhóm dựa trên các chỉ số RFM, sử dụng mô hình ARIMA để thực hiện dự báo tổng doanh thu(Total Turnover) của các khách hàng theo từng tháng và sự đoán doanh thu của từng khách hàng bằng mô hình deep learning

## Nội dung
* [Giới thiệu](#gioithieu)
* [Thư viện sử dụng](#thuvien)
* [Mô tả các bước thực hiện](#motacacbuocthuchien)

## Giới thiệu
Thông tin của bộ dữ liệu được nhận bao gồm 1 file csv:
- Bảng dữ liệu bao gồm 12364101 giao dịch và 16 trường thông tin

## Thư viện
Sử dụng các thư viện thống kê, huấn luyện mô hình:
* python version: 3.7
* tabpy version: 2.9.0 là thư viện dùng để kết nối dữ python và tableau
* pandas version: 2.0.3, là thư viện phổ biến dùng để thao tác trên các dữ liệu dạng bảng.
* numpy version: 1.24.3, là một dùng để xử lý dữ liệu list, array
* seaborn version: 0.12.2, sử dụng để vẽ biểu đồ
* matplotlib version: 3.7.2, sử dụng để vẽ biểu đồ
* plotly version: 5.9.0, sử dụng để vẽ biểu đồ
* statsmodels version: 0.13.5 thư viện cung cấp về các mô hình thống kế
* scikit-learn version: 1.0.2 thư viện cung cấp về các kỹ thuật tiền xử lý dữ liệu, mô hình học máy và các độ đo
* tensorflow version: 2.10.0 thư viện dùng để huấn luyện các mô hình deep learning
* keras version: 2.10.0 thư viện dùng để huấn luyện các mô hình deep learning

## Mô tả các bước thực hiện
### Thực hiện kết nối với server tabpy lên tableau trên máy tính cá nhân
B1: Tải [anaconda](https://www.anaconda.com/download)

B2: Tìm kiếm trên máy và mở anaconda prompt

B3: Tạo enviroment trên anaconda và tải các thư viện cần dùng
![image](https://github.com/HaiYen-hp/Data-Got-Talent/assets/73486795/adf6f3a2-69e2-43c1-9cc0-ebf66ccc8dec)
![image](https://github.com/HaiYen-hp/Data-Got-Talent/assets/73486795/39c730cd-1300-4af9-888a-6e75fecbd4fb)
![image](https://github.com/HaiYen-hp/Data-Got-Talent/assets/73486795/e74cae6f-82e2-4d64-bd1c-941d5034a63e)

B4: Chạy server tabpy trên máy tính cá nhân
![image](https://github.com/HaiYen-hp/Data-Got-Talent/assets/73486795/62bbe80d-16c6-4daa-9a3b-4c4d37b3bb2a)

B5: Viết các function và script bằng python và deploy lên tableau

### Mô hình
- File thống kê phần tích dữ liệu: statictis_data.ipynb
- File tiền xử lý dữ liệu: clean_data.py
- File chia tập khách hàng qua RFM: Segmentation_Customers.ipynb
- File huấn luyện và dự đoán doanh thu từng khách hàng: turnover_prediction.ipynb, TurnoverPrediction.py
- Script dự báo doanh thu qua từ tháng: Forecast (parametric) được viêt trên file tableau workbook




