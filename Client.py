import tkinter as tk
import threading
import cv2
import socket
import numpy as np
from PIL import Image, ImageTk
from UI import VideoChatUI

# 서버 IP 주소 및 포트 번호
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345

class VideoChatClient:
    def __init__(self):
        self.ui = VideoChatUI(tk.Tk(), "Video Streaming Client")
        self.ui.on_send_message = self.send_message_to_server

        #웹캠 초기화
        self.cap = cv2.VideoCapture(0)

        # 클라이언트 소켓 설정
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((SERVER_IP, SERVER_PORT))

        # 웹캠 영상 전송 스래드 시작
        self.webcam_thread = threading.Thread(target=self.send_webcam)
        self.webcam_thread.daemon = True
        self.webcam_thread.start()

        # 서버 연결을 처리하는 스레드 시작
        self.receive_thread = threading.Thread(target=self.receive_clients)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        # 비디오 수신 스레드 시작
        self.video_thread = threading.Thread(target=self.receive_video_stream)
        self.video_thread.daemon = True
        self.video_thread.start()

        # GUI 시작
        self.client_socket.mainloop()

        # 연결 종료 시 스레드 및 소켓 닫기
        self.client_socket.close()

    # 서버로부터 비디오 스트리밍을 받아 화면에 표시하는 함수
    def receive_video_stream(self):
        while True:
            try:
                img_bytes = self.client_socket.recv(1024)
                img_encoded = np.frombuffer(img_bytes, dtype=np.uint8)
                frame = cv2.imdecode(img_encoded, cv2.IMREAD_COLOR)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.label.config(image=photo)
                self.label.image = photo
            except Exception as e:
                print(e)
                break

    def show_frame(self):
        received_frame_data = self.client_socket.recv(65536)
        received_frame_array = np.frombuffer(received_frame_data,dtype=np.unit8)
        received_frame = cv2.imdecode(received_frame_array, cv2.IMREAD_COLOR)
        if received_frame is not None:
            self.ui.show_frame(received_frame)
        self.ui.window.after(100, self.show_frame())


    def send_message_to_server(self, message):
        self.client_socket.send(message.encode())

    def send_message_to_clients(self, message):
        self.ui.receive_message(message)            #클라이언트에서 받은 메시지를 UI에 표시

    def receive_message(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if not message:
                    break
                self.send_message_to_clients(message) #서버에거 받은 메시지를 UI에 표시
            except:
                pass
