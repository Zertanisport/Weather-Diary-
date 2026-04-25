import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
import json
import os
from datetime import datetime
import re

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Дневник погоды")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        self.root.minsize(800, 600)
        
        # Файл для хранения данных
        self.data_file = "weather_data.json"
        
        # Загрузка данных
        self.weather_records = self.load_data()
        
        # Настройка цветовой схемы
        self.setup_colors()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Заполнение таблицы
        self.refresh_table()
        
        # Обработчик закрытия
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_colors(self):
        """Настройка цветовой схемы приложения"""
        self.colors = {
            'bg_main': '#f0f4f8',
            'bg_secondary': '#ffffff',
            'primary': '#2196F3',
            'success': '#4CAF50',
            'warning': '#FF9800',
            'danger': '#f44336',
            'text_primary': '#212121',
            'text_secondary': '#757575',
            'border': '#e0e0e0',
            'row_even': '#f8f9fa',
            'row_odd': '#ffffff',
            'hover': '#e3f2fd'
        }
        self.root.configure(bg=self.colors['bg_main'])
        
    def create_widgets(self):
        """Создание всех элементов интерфейса"""
        
        # Главный контейнер
        main_frame = tk.Frame(self.root, bg=self.colors['bg_main'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Заголовок приложения
        self.create_header(main_frame)
        
        # Панель ввода данных
        self.create_input_panel(main_frame)
        
        # Панель фильтрации
        self.create_filter_panel(main_frame)
        
        # Таблица записей
        self.create_table(main_frame)
        
        # Панель статистики
        self.create_stats_panel(main_frame)
        
    def create_header(self, parent):
        """Создание заголовка"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_main'])
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_font = tkfont.Font(family="Arial", size=20, weight="bold")
        title_label = tk.Label(
            header_frame,
            text="Дневник погоды",
            font=title_font,
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary']
        )
        title_label.pack(side=tk.LEFT)
        
        # Информация о количестве записей
        self.record_count_label = tk.Label(
            header_frame,
            text=f"Записей: {len(self.weather_records)}",
            font=("Arial", 11),
            bg=self.colors['bg_main'],
            fg=self.colors['text_secondary']
        )
        self.record_count_label.pack(side=tk.RIGHT)
        
    def create_input_panel(self, parent):
        """Создание панели ввода данных"""
        input_frame = tk.LabelFrame(
            parent,
            text="Добавить новую запись",
            font=("Arial", 12, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            relief=tk.RAISED,
            bd=1
        )
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Контейнер для полей ввода
        fields_container = tk.Frame(input_frame, bg=self.colors['bg_secondary'])
        fields_container.pack(fill=tk.X, padx=15, pady=15)
        
        # Поле "Дата"
        tk.Label(
            fields_container,
            text="Дата (ДД.ММ.ГГГГ):",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            font=("Arial", 10)
        ).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.date_entry = tk.Entry(
            fields_container,
            font=("Arial", 11),
            width=20,
            relief=tk.FLAT,
            bd=1,
            bg='white'
        )
        self.date_entry.grid(row=1, column=0, padx=(0, 20), sticky=tk.W)
        self.date_entry.insert(0, datetime.now().strftime("%d.%m.%Y"))
        
        # Поле "Температура"
        tk.Label(
            fields_container,
            text="Температура (°C):",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            font=("Arial", 10)
        ).grid(row=0, column=1, sticky=tk.W, pady=(0, 5))
        
        self.temp_entry = tk.Entry(
            fields_container,
            font=("Arial", 11),
            width=15,
            relief=tk.FLAT,
            bd=1,
            bg='white'
        )
        self.temp_entry.grid(row=1, column=1, padx=(0, 20), sticky=tk.W)
        self.temp_entry.insert(0, "20")
        
        # Поле "Описание погоды"
        tk.Label(
            fields_container,
            text="Описание погоды:",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            font=("Arial", 10)
        ).grid(row=0, column=2, sticky=tk.W, pady=(0, 5))
        
        self.weather_desc_entry = tk.Entry(
            fields_container,
            font=("Arial", 11),
            width=30,
            relief=tk.FLAT,
            bd=1,
            bg='white'
        )
        self.weather_desc_entry.grid(row=1, column=2, padx=(0, 20), sticky=tk.W)
        
        # Поле "Осадки"
        tk.Label(
            fields_container,
            text="Осадки:",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            font=("Arial", 10)
        ).grid(row=0, column=3, sticky=tk.W, pady=(0, 5))
        
        self.precipitation_var = tk.BooleanVar()
        self.precipitation_check = tk.Checkbutton(
            fields_container,
            text="Да",
            variable=self.precipitation_var,
            bg=self.colors['bg_secondary'],
            font=("Arial", 11)
        )
        self.precipitation_check.grid(row=1, column=3, sticky=tk.W)
        
        # Кнопка добавления
        add_button = tk.Button(
            fields_container,
            text="Добавить запись",
            command=self.add_record,
            bg=self.colors['success'],
            fg='white',
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        add_button.grid(row=1, column=4, padx=(20, 0))
        
    def create_filter_panel(self, parent):
        """Создание панели фильтрации"""
        filter_frame = tk.LabelFrame(
            parent,
            text="Фильтрация записей",
            font=("Arial", 12, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            relief=tk.RAISED,
            bd=1
        )
        filter_frame.pack(fill=tk.X, pady=(0, 15))
        
        filter_container = tk.Frame(filter_frame, bg=self.colors['bg_secondary'])
        filter_container.pack(fill=tk.X, padx=15, pady=15)
        
        # Фильтр по дате
        tk.Label(
            filter_container,
            text="Фильтр по дате:",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            font=("Arial", 10)
        ).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.filter_date_entry = tk.Entry(
            filter_container,
            font=("Arial", 11),
            width=20,
            relief=tk.FLAT,
            bd=1,
            bg='white'
        )
        self.filter_date_entry.grid(row=1, column=0, padx=(0, 20), sticky=tk.W)
        
        # Кнопка фильтрации по дате
        filter_date_btn = tk.Button(
            filter_container,
            text="Фильтровать",
            command=self.filter_by_date,
            bg=self.colors['primary'],
            fg='white',
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=9,
            pady=1,
            cursor="hand2"
        )
        filter_date_btn.grid(row=1, column=1, padx=(0, 30))
        
        # Фильтр по температуре
        tk.Label(
            filter_container,
            text="Температура выше (°C):",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            font=("Arial", 10)
        ).grid(row=0, column=2, sticky=tk.W, pady=(0, 5))
        
        self.filter_temp_entry = tk.Entry(
            filter_container,
            font=("Arial", 11),
            width=15,
            relief=tk.FLAT,
            bd=1,
            bg='white'
        )
        self.filter_temp_entry.grid(row=1, column=2, padx=(0, 20), sticky=tk.W)
        
        # Кнопка фильтрации по температуре
        filter_temp_btn = tk.Button(
            filter_container,
            text="Фильтровать",
            command=self.filter_by_temperature,
            bg=self.colors['primary'],
            fg='white',
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=9,
            pady=1,
            cursor="hand2"
        )
        filter_temp_btn.grid(row=1, column=3, padx=(0, 30))
        
        # Кнопка сброса фильтров
        reset_filter_btn = tk.Button(
            filter_container,
            text="Сбросить фильтры",
            command=self.reset_filters,
            bg=self.colors['warning'],
            fg='white',
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=9,
            pady=1,
            cursor="hand2"
        )
        reset_filter_btn.grid(row=1, column=4)
        
    def create_table(self, parent):
        """Создание таблицы записей"""
        table_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Создаем Treeview для таблицы
        columns = ('date', 'temperature', 'description', 'precipitation', 'time')
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            height=15
        )
        
        # Определяем заголовки
        self.tree.heading('date', text='Дата')
        self.tree.heading('temperature', text='Температура')
        self.tree.heading('description', text='Описание')
        self.tree.heading('precipitation', text='Осадки')
        self.tree.heading('time', text='🕐 Время добавления')
        
        # Настройка ширины колонок
        self.tree.column('date', width=120)
        self.tree.column('temperature', width=120)
        self.tree.column('description', width=250)
        self.tree.column('precipitation', width=100)
        self.tree.column('time', width=180)
        
        # Добавляем скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещение таблицы и скроллбара
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Привязываем двойной клик для удаления
        self.tree.bind('<Double-1>', self.on_double_click)
        
        # Настройка стилей для Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="white",
            foreground=self.colors['text_primary'],
            rowheight=30,
            fieldbackground="white",
            font=("Arial", 10)
        )
        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold"),
            background=self.colors['bg_main']
        )
        style.map(
            "Treeview",
            background=[('selected', self.colors['hover'])],
            foreground=[('selected', self.colors['text_primary'])]
        )
        
    def create_stats_panel(self, parent):
        """Создание панели статистики"""
        stats_frame = tk.Frame(parent, bg=self.colors['bg_main'])
        stats_frame.pack(fill=tk.X)
        
        # Кнопки управления
        button_frame = tk.Frame(stats_frame, bg=self.colors['bg_main'])
        button_frame.pack(side=tk.LEFT)
        
        delete_btn = tk.Button(
            button_frame,
            text="Удалить выбранное",
            command=self.delete_selected,
            bg=self.colors['danger'],
            fg='white',
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2"
        )
        delete_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        save_btn = tk.Button(
            button_frame,
            text="Сохранить",
            command=self.save_data,
            bg=self.colors['success'],
            fg='white',
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2"
        )
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        export_btn = tk.Button(
            button_frame,
            text="📁 Экспорт",
            command=self.export_data,
            bg=self.colors['primary'],
            fg='white',
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2"
        )
        export_btn.pack(side=tk.LEFT)
        
        # Статистика
        self.stats_label = tk.Label(
            stats_frame,
            text="",
            bg=self.colors['bg_main'],
            fg=self.colors['text_secondary'],
            font=("Arial", 10)
        )
        self.stats_label.pack(side=tk.RIGHT)
        self.update_stats()
        
    def add_record(self):
        """Добавление новой записи о погоде"""
        date = self.date_entry.get().strip()
        temp = self.temp_entry.get().strip()
        desc = self.weather_desc_entry.get().strip()
        precipitation = self.precipitation_var.get()
        
        # Валидация данных
        if not self.validate_date(date):
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ДД.ММ.ГГГГ")
            return
            
        if not self.validate_temperature(temp):
            messagebox.showerror("Ошибка", "Температура должна быть числом!")
            return
            
        if not desc:
            messagebox.showerror("Ошибка", "Описание погоды не может быть пустым!")
            return
            
        # Создание записи
        record = {
            "date": date,
            "temperature": float(temp),
            "description": desc,
            "precipitation": "Да" if precipitation else "Нет",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Добавление в список
        self.weather_records.append(record)
        
        # Сохранение данных
        self.save_data()
        
        # Обновление интерфейса
        self.refresh_table()
        self.update_stats()
        self.record_count_label.config(text=f"Записей: {len(self.weather_records)}")
        
        # Очистка полей
        self.weather_desc_entry.delete(0, tk.END)
        self.weather_desc_entry.focus()
        
        messagebox.showinfo("Успех", "Запись успешно добавлена!")
        
    def validate_date(self, date_str):
        """Проверка формата даты"""
        pattern = r'^\d{2}\.\d{2}\.\d{4}$'
        if not re.match(pattern, date_str):
            return False
            
        try:
            day, month, year = map(int, date_str.split('.'))
            datetime(year, month, day)
            return True
        except:
            return False
            
    def validate_temperature(self, temp_str):
        """Проверка температуры"""
        try:
            float(temp_str)
            return True
        except:
            return False
            
    def filter_by_date(self):
        """Фильтрация записей по дате"""
        filter_date = self.filter_date_entry.get().strip()
        
        if not filter_date:
            messagebox.showwarning("Предупреждение", "Введите дату для фильтрации!")
            return
            
        if not self.validate_date(filter_date):
            messagebox.showerror("Ошибка", "Неверный формат даты!")
            return
            
        # Фильтрация записей
        filtered_records = [
            record for record in self.weather_records 
            if record['date'] == filter_date
        ]
        
        self.refresh_table(filtered_records)
        self.update_stats(filtered_records)
        
    def filter_by_temperature(self):
        """Фильтрация записей по температуре"""
        temp_str = self.filter_temp_entry.get().strip()
        
        if not temp_str:
            messagebox.showwarning("Предупреждение", "Введите температуру для фильтрации!")
            return
            
        if not self.validate_temperature(temp_str):
            messagebox.showerror("Ошибка", "Температура должна быть числом!")
            return
            
        threshold = float(temp_str)
        
        # Фильтрация записей
        filtered_records = [
            record for record in self.weather_records 
            if record['temperature'] > threshold
        ]
        
        self.refresh_table(filtered_records)
        self.update_stats(filtered_records)
        
    def reset_filters(self):
        """Сброс фильтров"""
        self.filter_date_entry.delete(0, tk.END)
        self.filter_temp_entry.delete(0, tk.END)
        self.refresh_table()
        self.update_stats()
        
    def refresh_table(self, records=None):
        """Обновление таблицы записей"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if records is None:
            records = self.weather_records
            
        # Заполнение таблицы
        for record in records:
            values = (
                record['date'],
                f"{record['temperature']}°C",
                record['description'],
                record['precipitation'],
                record.get('timestamp', '')
            )
            
            # Определяем тег для строки в зависимости от температуры
            if record['temperature'] < 0:
                tag = 'cold'
            elif record['temperature'] > 25:
                tag = 'hot'
            else:
                tag = 'normal'
                
            self.tree.insert('', tk.END, values=values, tags=(tag,))
            
        # Настройка цветов для тегов
        self.tree.tag_configure('cold', background='#e3f2fd')
        self.tree.tag_configure('hot', background='#ffebee')
        self.tree.tag_configure('normal', background='white')
        
    def update_stats(self, records=None):
        """Обновление статистики"""
        if records is None:
            records = self.weather_records
            
        if records:
            temperatures = [r['temperature'] for r in records]
            avg_temp = sum(temperatures) / len(temperatures)
            min_temp = min(temperatures)
            max_temp = max(temperatures)
            rain_days = sum(1 for r in records if r['precipitation'] == 'Да')
            
            stats_text = f"Средняя t: {avg_temp:.1f}°C | Мин: {min_temp}°C | Макс: {max_temp}°C | Дней с осадками: {rain_days}"
        else:
            stats_text = "Нет данных для отображения статистики"
            
        self.stats_label.config(text=stats_text)
        
    def delete_selected(self):
        """Удаление выбранной записи"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите запись для удаления!")
            return
            
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранную запись?"):
            # Получаем индекс выбранной записи
            item = selected[0]
            values = self.tree.item(item, 'values')
            
            # Находим и удаляем запись из списка
            for i, record in enumerate(self.weather_records):
                if (record['date'] == values[0] and 
                    f"{record['temperature']}°C" == values[1] and 
                    record['description'] == values[2]):
                    del self.weather_records[i]
                    break
                    
            self.save_data()
            self.refresh_table()
            self.update_stats()
            self.record_count_label.config(text=f"Записей: {len(self.weather_records)}")
            messagebox.showinfo("Успех", "Запись удалена!")
            
    def on_double_click(self, event):
        """Обработчик двойного клика по записи"""
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            values = self.tree.item(item, 'values')
            
            info_text = f"Дата: {values[0]}\n"
            info_text += f"Температура: {values[1]}\n"
            info_text += f"Описание: {values[2]}\n"
            info_text += f"Осадки: {values[3]}\n"
            info_text += f"Добавлено: {values[4]}"
            
            messagebox.showinfo("Информация о записи", info_text)
            
    def load_data(self):
        """Загрузка данных из файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except:
                return []
        return []
        
    def save_data(self):
        """Сохранение данных в файл"""
        with open(self.data_file, 'w', encoding='utf-8') as file:
            json.dump(self.weather_records, file, ensure_ascii=False, indent=2)
            
    def export_data(self):
        """Экспорт данных в текстовый файл"""
        export_file = f"weather_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(export_file, 'w', encoding='utf-8') as file:
            file.write("ДНЕВНИК ПОГОДЫ\n")
            file.write("=" * 80 + "\n\n")
            
            for record in self.weather_records:
                file.write(f"Дата: {record['date']}\n")
                file.write(f"Температура: {record['temperature']}°C\n")
                file.write(f"Описание: {record['description']}\n")
                file.write(f"Осадки: {record['precipitation']}\n")
                file.write(f"Добавлено: {record.get('timestamp', '')}\n")
                file.write("-" * 40 + "\n")
                
        messagebox.showinfo("Успех", f"Данные экспортированы в файл {export_file}")
        
    def on_closing(self):
        """Обработчик закрытия приложения"""
        self.save_data()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = WeatherDiary(root)
    
    # Центрирование окна
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()
