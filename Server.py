import tkinter as tk
import cv2
import socket
import threading
from UI import VideoChatUI

# 서버 IP 주소 및 포트 번호
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
class VideoChatServer:
    def __init__(self):
        self.ui = VideoChatUI(tk.Tk(), "화상 채팅 서버")
        self.ui.on_send_message = self.send_message_to_clients
        self.clients = []

        #웹캠 초기화
        self.cap = cv2.VideoCapture(0)

        #소켓 초기화
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(SERVER_IP, SERVER_PORT)
        self.server_socket.listen(5)

        #웹캠 영상 전송 스래드 시작
        self.webcam_thread = threading.Thread(target=self.send_webcam)
        self.webcam_thread.daemon = True
        self.webcam_thread.start()

        #클라이언트 연결을 처리하는 스레드 시작
        self.receive_thread = threading.Thread(target=self.receive_clients)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        # 라벨 위젯을 사용하여 영상 표시 (80%)
        self.label = tk.Label(self.window)
        self.label.grid(row=0, column=0, padx=10, pady=10, rowspan=2, sticky="nsew")

        # 채팅 창 (Text 위젯) 추가 (20%)
        self.chat_text = tk.Text(self.window, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_text.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # 메시지 입력 필드 (20%)
        self.entry = tk.Entry(self.window)
        self.entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # 메시지 보내기 버튼 (20%)
        self.send_button = tk.Button(self.window, text="보내기", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10, sticky="se")

        # 행 및 열 가중치 설정
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=4)  # 비디오 화면이 80% 차지
        self.window.grid_columnconfigure(1, weight=1)  # 채팅 창이 20% 차지

        # 갱신 함수 호출
        self.update()

        # GUI 초기화
        self.window = tk.Tk()
        self.window.title("화상 채팅")

        #서버 GUI 시작
        self.window.mainloop()

        # 웹캠 해제
        self.cap.release()

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = self.ImageTk.PhotoImage(image=self.Image.fromarray(frame))
            self.label.config(image=photo)
            self.label.image = photo
        self.window.after(10, self.update)

    def send_message(self):
        message = self.entry.get()
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, "나: " + message + "\n")
        self.chat_text.config(state=tk.DISABLED)
        self.entry.delete(0, tk.END)

    def show_frame(self, frame):
        self.ui.show_frame(frame)

    def send_message_to_clients(self, message):
        for client in self.clients:
            client.send(message.encode())
        #서버 UI에도 메시지 표시
        self.ui.receive_message("서버: "+message)

    def send_message_to_server(self, message):
        self.ui.receive_message(message)    #서버에서 받은 메시지를 UI에 표시
        self.send_message_to_clients(message)   #받은 메시지를 다른 클라이언트들에게 전송

    def send_webcam(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                continue
            _, encoded_frame = cv2.imencode('.jpg',frame, {int(cv2.IMWRITE_JPEG_QUALITY), 60})
            encoded_frame = encoded_frame.tobytes()
            for client in self.clients:
                try:
                    client.send(encoded_frame)
                except:
                    self.clients.remove(client)
            #서버 UI에도 비디오 화면 표시
            self.show_frame(frame)

if __name__ == "__main__":
    server = VideoChatServer()
