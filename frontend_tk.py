import time
import random
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont

import question_bank
import exam_generator


def get_subjects(questions):
    subjects = sorted({q.subject for q in questions})
    return subjects


def generate_from_dataset(subject: str, num_questions: int, diff_mode: str):
    # Map difficulty mode to ratios
    if diff_mode == 'easy':
        er, mr, hr = 1.0, 0.0, 0.0
    elif diff_mode == 'medium':
        er, mr, hr = 0.0, 1.0, 0.0
    elif diff_mode == 'hard':
        er, mr, hr = 0.0, 0.0, 1.0
    else:  # mixed
        er, mr, hr = 0.3, 0.5, 0.2
    exam = exam_generator.generate_exam(
        'questions_vi.csv', subject, num_questions,
        easy_ratio=er, medium_ratio=mr, hard_ratio=hr,
    )
    return exam


def generate_from_llm(subject: str, num_questions: int, diff_mode: str):
    """Placeholder cho sinh câu hỏi từ LLM.

    Hiện tại để demo, hàm này tái sử dụng bộ sinh đề từ dataset.
    Khi tích hợp LLM thực, bạn có thể thay thân hàm này bằng lời gọi API
    sinh câu hỏi mới và ánh xạ về cấu trúc Question tương tự question_bank.Question.
    """
    return generate_from_dataset(subject, num_questions, diff_mode)


class QuizApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title('Quiz Demo - Python & DSA')

        # Thử phóng to toàn màn hình (zoomed); nếu không được thì đặt kích thước lớn
        try:
            self.root.state('zoomed')  # Windows
        except tk.TclError:
            self.root.geometry('1200x800')

        # Fonts & style (phóng to chữ toàn app)
        self.base_font = tkfont.Font(family='Segoe UI', size=13)
        self.title_font = tkfont.Font(family='Segoe UI', size=14, weight='bold')
        self.code_font = tkfont.Font(family='Consolas', size=12)

        style = ttk.Style(self.root)
        try:
            style.theme_use('clam')
        except tk.TclError:
            pass
        style.configure('TLabel', font=self.base_font)
        style.configure('TButton', font=self.base_font)
        style.configure('TRadiobutton', font=self.base_font)
        style.configure('TCheckbutton', font=self.base_font)
        style.configure('TLabelframe.Label', font=self.title_font)

        # Load full question bank once
        self.all_questions = question_bank.load_questions('questions_vi.csv')
        self.subjects = get_subjects(self.all_questions)

        # State
        self.current_exam = []
        self.answer_vars = []  # list of (question, tk.StringVar, frame)
        self.start_time = None
        self.timer_running = False

        self.build_ui()

        # Không cho copy nội dung trong app bằng Ctrl+C
        self.root.bind_all('<Control-c>', lambda e: 'break')

    def build_ui(self):
        self.root.configure(bg='#f5f5f5')

        # Top configuration frame (không chiếm hết, để phần ĐỀ THI bên dưới full)
        cfg_frame = ttk.LabelFrame(self.root, text='Cấu hình đề thi')
        cfg_frame.pack(fill='x', padx=10, pady=10)

        ttk.Label(cfg_frame, text='Môn học:').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.subject_var = tk.StringVar()
        self.subject_cb = ttk.Combobox(cfg_frame, textvariable=self.subject_var, state='readonly', font=self.base_font, width=22)
        self.subject_cb['values'] = self.subjects
        if self.subjects:
            self.subject_cb.current(0)
        self.subject_cb.grid(row=0, column=1, sticky='w', padx=5, pady=5)

        ttk.Label(cfg_frame, text='Độ khó:').grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.diff_var = tk.StringVar(value='xáo trộn')
        self.diff_cb = ttk.Combobox(cfg_frame, textvariable=self.diff_var, state='readonly', font=self.base_font, width=10)
        self.diff_cb['values'] = ['dễ', 'trung bình', 'khó', 'xáo trộn']
        self.diff_cb.current(3)
        self.diff_cb.grid(row=0, column=3, sticky='w', padx=5, pady=5)

        ttk.Label(cfg_frame, text='Nguồn:').grid(row=0, column=4, sticky='w', padx=5, pady=5)
        self.source_var = tk.StringVar(value='dataset')
        ttk.Radiobutton(cfg_frame, text='Dataset', variable=self.source_var, value='dataset').grid(
            row=0, column=5, sticky='w', padx=(0, 2), pady=5
        )
        ttk.Radiobutton(cfg_frame, text='LLM', variable=self.source_var, value='llm').grid(
            row=0, column=6, sticky='w', padx=(0, 5), pady=5
        )

        ttk.Label(cfg_frame, text='Số câu hỏi:').grid(row=0, column=7, sticky='w', padx=5, pady=5)
        self.num_var = tk.IntVar(value=10)
        self.num_spin = ttk.Spinbox(cfg_frame, from_=1, to=50, textvariable=self.num_var, width=5, font=self.base_font)
        self.num_spin.grid(row=0, column=8, sticky='w', padx=5, pady=5)


        self.start_btn = ttk.Button(cfg_frame, text='Tạo đề và bắt đầu làm bài', command=self.on_start)
        self.start_btn.grid(row=1, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

        self.timer_label = ttk.Label(cfg_frame, text='Thời gian: 00:00', font=self.title_font)
        self.timer_label.grid(row=1, column=2, columnspan=4, sticky='ew', padx=5, pady=5)

        self.submit_btn = ttk.Button(cfg_frame, text='Nộp bài và chấm điểm', command=self.on_submit)
        self.submit_btn.grid(row=1, column=5, columnspan=4, sticky='ew', padx=5, pady=5)

        # Khung ĐỀ THI chiếm toàn bộ phần còn lại
        exam_outer = ttk.LabelFrame(self.root, text='ĐỀ THI')
        exam_outer.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        q_container = ttk.Frame(exam_outer)
        q_container.pack(fill='both', expand=True, padx=5, pady=5)

        canvas = tk.Canvas(q_container, borderwidth=0, highlightthickness=0, bg='#f5f5f5')
        scrollbar = ttk.Scrollbar(q_container, orient='vertical', command=canvas.yview)
        self.questions_frame = ttk.Frame(canvas)

        # Gắn window và ép cho questions_frame luôn full width của canvas
        self.canvas_window = canvas.create_window((0, 0), window=self.questions_frame, anchor='nw')

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox('all'))

        self.questions_frame.bind('<Configure>', on_frame_configure)

        def on_canvas_configure(event):
            canvas.itemconfig(self.canvas_window, width=event.width)

        canvas.bind('<Configure>', on_canvas_configure)

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.canvas = canvas

        # Enable mouse wheel scrolling
        self.canvas.bind_all('<MouseWheel>', self.on_mousewheel)
        # For Linux systems
        self.canvas.bind_all('<Button-4>', lambda e: self.canvas.yview_scroll(-1, 'units'))
        self.canvas.bind_all('<Button-5>', lambda e: self.canvas.yview_scroll(1, 'units'))

        # Result label dưới khung ĐỀ THI
        self.result_label = ttk.Label(self.root, text='Kết quả sẽ hiển thị ở đây.', foreground='blue', font=self.title_font)
        self.result_label.pack(fill='x', padx=10, pady=(0, 8))

    def on_mousewheel(self, event):
        # Windows / macOS scroll
        delta = int(-1 * (event.delta / 120))
        self.canvas.yview_scroll(delta, 'units')

    def on_start(self):
        subject = self.subject_var.get()
        diff_mode = self.diff_var.get()
        num_q = self.num_var.get()
        source = self.source_var.get()

        if not subject:
            messagebox.showwarning('Thiếu thông tin', 'Vui lòng chọn môn học.')
            return

        if num_q <= 0:
            messagebox.showwarning('Số câu không hợp lệ', 'Số câu hỏi phải lớn hơn 0.')
            return

        # Generate exam
        try:
            if source == 'dataset':
                exam = generate_from_dataset(subject, num_q, diff_mode)
            else:
                exam = generate_from_llm(subject, num_q, diff_mode)
        except Exception as e:
            messagebox.showerror('Lỗi sinh đề', f'Không thể sinh đề: {e}')
            return

        if not exam:
            messagebox.showwarning('Không có câu hỏi', 'Không tìm thấy câu hỏi phù hợp trong ngân hàng.')
            return

        self.current_exam = exam
        self.answer_vars = []
        # Clear previous questions
        for child in self.questions_frame.winfo_children():
            child.destroy()

        # Render questions
        for idx, q in enumerate(self.current_exam, start=1):
            q_frame = ttk.LabelFrame(self.questions_frame, text=f'Câu {idx}')
            q_frame.pack(fill='x', expand=True, padx=5, pady=7)

            # Tách phần mô tả và phần code (nếu có) với ký tự trong dữ liệu
            text = q.text or ''
            text = text.replace('\\n', '\n')

            if '\n' in text:
                parts = text.split('\n')
                prompt = parts[0]
                code = '\n'.join(parts[1:]).strip()
            else:
                prompt = text
                code = ''

            prompt_lbl = ttk.Label(q_frame, text=prompt, wraplength=1100, justify='left', font=self.base_font)
            prompt_lbl.pack(anchor='w', padx=5, pady=3)

            if code:
                code_box = tk.Text(
                    q_frame,
                    height=min(8, max(2, code.count('\n') + 1)),
                    width=110,
                    font=self.code_font,
                    bg='#f0f0f0',
                    relief='flat',
                    wrap='none',
                )
                code_box.insert('1.0', code)
                code_box.config(state='disabled')  # chỉ đọc
                code_box.pack(anchor='w', padx=25, pady=3)

            var = tk.StringVar()
            self.answer_vars.append((q, var, q_frame))

            opt_items = list(q.options.items())        # [(key, text), ...]
            random.shuffle(opt_items)                  # xáo trộn vị trí

            labels = ['A', 'B', 'C', 'D']
            for (key, opt_text), label in zip(opt_items, labels):
                rb = ttk.Radiobutton(
                    q_frame,
                    text=f'{label}. {opt_text}',
                    variable=var,
                    value=key,      
                )
                rb.pack(anchor='w', padx=25, pady=2)

        # Reset timer
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()
        self.result_label.config(text='Đề thi đã được tạo. Hãy bắt đầu làm bài.', foreground='blue')

    def update_timer(self):
        if not self.timer_running or self.start_time is None:
            return
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        self.timer_label.config(text=f'Thời gian: {minutes:02d}:{seconds:02d}')
        self.root.after(1000, self.update_timer)

    def on_submit(self):
        if not self.current_exam or not self.answer_vars:
            messagebox.showwarning('Chưa có đề', 'Bạn chưa bấm "Bắt đầu làm bài".')
            return

        for q, var, frame in self.answer_vars:
            if not var.get():
                messagebox.showwarning('Chưa làm đầy đủ', 'Vui lòng trả lời tất cả các câu hỏi trước khi nộp.')
                return

        self.timer_running = False
        if self.start_time is not None:
            elapsed = int(time.time() - self.start_time)
        else:
            elapsed = 0

        correct = 0
        total = len(self.answer_vars)

        for q, var, frame in self.answer_vars:
            chosen = var.get()
            is_correct = chosen == q.correct_option
            if is_correct:
                correct += 1

            feedback_text = 'Đúng' if is_correct else 'Sai'
            correct_label = q.options[q.correct_option]
            fb_lbl = ttk.Label(
                frame,
                text=f'Kết quả: {feedback_text}. Đáp án đúng: {correct_label}',
                foreground='green' if is_correct else 'red',
            )
            fb_lbl.pack(anchor='w', padx=5, pady=2)

            for child in frame.winfo_children():
                if isinstance(child, ttk.Radiobutton):
                    child.state(['disabled'])

        score_10 = 10 * correct / total if total > 0 else 0.0
        minutes = elapsed // 60
        seconds = elapsed % 60

        summary = (
            f'Điểm: {score_10:.2f}/10 | Đúng {correct}/{total} câu | '
            f'Thời gian: {minutes:02d}:{seconds:02d}'
        )
        self.result_label.config(text=summary, foreground='purple')


if __name__ == '__main__':
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
