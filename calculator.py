from tkinter import *
from tkinter import ttk, filedialog, messagebox
import csv
from pathlib import Path
import math
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
expr = ""  # Global expression string

def press(key):
    global expr
    expr += str(key)
    display.set(expr)

def equal():
    global expr
    calculation = display.get().strip()    #read the typed expression
    try:
        result = str(eval(calculation))
        display.set(result)
        history_box.insert(END, f"{calculation}={result}")
        expr = result
    except Exception:
        display.set("Error")
        expr = " "

def clear():
    global expr
    expr = ""
    display.set("")

def backspace():
    global expr
    expr = expr[:-1]
    display.set(expr)

def keyboard_input(event):
    global expr
    if event.keysym in ("Return", "KP_Enter"):
        expr = display.get()
        equal()
        return "break"
    if event.keysym == "BackSpace":
        return              #Entry handle Backspace
    if event.keysym == "Escape":
        clear()
        return "break"    #Entry handle all other keys, including letters and symbols.

def advanced_press(value):
    advanced_display.set(advanced_display.get() + str(value))

def advanced_clear():
    advanced_display.set("")
    degree_button.config(bg="light blue", fg="black")
    radian_button.config(bg="light blue", fg="black")

def advanced_backspace():
    advanced_display.set(advanced_display.get()[:-1])

def set_degrees():
    degree_mode = True
    degree_button.config(bg='blue', fg='white')
    radian_button.config(bg='light blue', fg='black')

def set_radians():
    degree_mode = False
    radian_button.config(bg='blue', fg='white')
    degree_button.config(bg='light blue', fg='black')

def advanced_calculate(function):
    try:
        original_value = advanced_display.get().strip()
        value = float(original_value)

        if function == "square":
            result = value ** 2
        elif function == "sqrt":
            result = math.sqrt(value)
        elif function == "reciprocal":
            result = 1 / value
        elif function == "factorial":
            if value < 0 or not value.is_integer():
                raise ValueError
            result = math.factorial(int(value))
        elif function == "percent":
            result = value / 100
        elif function == "log":
            result = math.log10(value)
        elif function == "ln":
            result = math.log(value)
        elif function in ("sin", "cos", "tan"):
            angle = math.radians(value) if angle_mode.get() == "DEG" else value

            if function == "sin":
                result = math.sin(angle)
            elif function == "cos":
                result = math.cos(angle)
            else:
                result = math.tan(angle)

        advanced_display.set(str(result))
        ad_history_box.insert(END, f"{function}{original_value}={result}")

    except (ValueError, ZeroDivisionError, OverflowError):
        advanced_display.set("Error")

def convert_units():
    try:
        value = float(conversion_input.get())
        category = conversion_category.get()
        from_unit = from_unit_choice.get()
        to_unit = to_unit_choice.get()

        # Convert the input to a base unit, then from the base unit
        if category == "Length":
            factors = {"Millimeter": 0.001,
                "Centimeter": 0.01,
                "Meter": 1,
                "Kilometer": 1000,
                "Inch": 0.0254,
                "Foot": 0.3048,
                "Mile": 1609.344,}
            result = value * factors[from_unit] / factors[to_unit]

        elif category == "Weight":
            factors = {"Milligram": 0.000001,
                "Gram": 0.001,
                "Kilogram": 1,
                "Ounce": 0.028349523125,
                "Pound": 0.45359237,}
            result = value * factors[from_unit] / factors[to_unit]

        elif category == "Temperature":
            if from_unit == "Celsius":      # Convert to Celsius first
                celsius = value
            elif from_unit == "Fahrenheit":
                celsius = (value - 32) * 5 / 9
            else:                          
                celsius = value - 273.15            # Kelvin
            # Convert from Celsius to the selected unit
            if to_unit == "Celsius":
                result = celsius
            elif to_unit == "Fahrenheit":
                result = celsius * 9 / 5 + 32
            else:  # Kelvin
                result = celsius + 273.15

        conversion_result.config(text=f"Result: {result:.6g} {to_unit}")

    except (ValueError, KeyError):
        conversion_result.config(text="Enter a valid number and select units")

def calculate_bmi():
    try:
        weight = float(bmi_weight.get())
        height_cm = float(bmi_height.get())
        if weight <= 0 or height_cm <= 0:
            raise ValueError
        height_m = height_cm / 100
        bmi = weight / (height_m ** 2)
        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal range"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obesity range"
        bmi_result.config(text=f"BMI: {bmi:.1f} — {category}")
    except ValueError:
        bmi_result.config(text="Enter valid positive height and weight values")

def clear_bmi():
    bmi_weight.set("")
    bmi_height.set("")
    bmi_result.config(text="Enter your height and weight.")

def calculate_gst():
    try:
        amount_text = gst_amount.get().strip().replace(",","")
        rate_text = gst_rate.get().strip().replace("%","")
        amount = float(amount_text)
        rate = float(rate_text)
        if not math.isfinite(amount) or not math.isfinite(rate) or amount < 0 or rate <0:
            raise ValueError
        if gst_mode.get() == "Inclusive of GST":
            base_amount = amount / (1 + rate / 100)
            tax = amount - base_amount
            total = amount
        else:
            base_amount = amount
            tax = base_amount * rate / 100
            total = base_amount + tax
        gst_result.config(text=f"Base amount: {base_amount:.2f}\nGST ({rate:g}%): {tax:.2f}\nTotal: {total:.2f}")
    except (ValueError, OverflowError):
        gst_result.config(text="Enter valid non-negative amount and GST rate values")

def clear_gst():
    gst_amount.set("")
    gst_rate.set("18")
    gst_mode.set("Exclusive of GST")
    gst_result.config(text="Enter an amount and GST rate.")

if __name__ == "__main__":
    root = Tk()
    angle_mode = StringVar(value="DEG")
    root.configure(bg='dark blue')
    root.title("Smart Calculator", )
    root.geometry("400x500")
    style = ttk.Style(root)
    style.theme_use("clam")  # allows custom tab colors
    style.configure("TNotebook.Tab",
    background="#d9eaf7",  # unselected tab
    foreground="#222222",
    padding=[12, 6])

    style.map("TNotebook.Tab",
    background=[("selected", "#2563eb"), ("active", "#93c5fd")],
    foreground=[("selected", "white"), ("active", "#111827")])
    tabs = ttk.Notebook(root)
    tabs.pack(fill="both", expand=True)     #Notebook is managed in root with pack

    basic_tab = Frame(tabs)
    advanced_tab = Frame(tabs)
    conversion_tab = Frame(tabs)
    graph_tab = Frame(tabs)

    basic_tab = ttk.Frame(tabs, style="Calculator.TFrame")
    advanced_tab = ttk.Frame(tabs, style="Calculator.TFrame")
    conversion_tab = ttk.Frame(tabs, style="Calculator.TFrame")
    graph_tab = ttk.Frame(tabs, style="Calculator.TFrame")
    bmi_tab = ttk.Frame(tabs, style="Calculator.TFrame")
    gst_tab = ttk.Frame(tabs, style="Calculator.TFrame")

    style.configure("Calculator.TFrame", background="#1e1e2e")

    tabs.add(basic_tab, text="Basic")
    tabs.add(advanced_tab, text="Advanced")
    tabs.add(conversion_tab, text="UnitConversion")
    tabs.add(graph_tab, text="Graph")
    tabs.add(bmi_tab, text="BMI")
    tabs.add(gst_tab, text="GST")
   
    display = StringVar()
    entry = Entry(basic_tab, textvariable=display, width=30, font=("Arial",10) )
    entry.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="ew", ipady=10)
    entry.bind("<Key>", keyboard_input)
    entry.focus_set()

        #Basic tab
    # Number buttons
    btn1 = Button(basic_tab, text='1', fg='black', bg='light blue', command=lambda: press(1), height=2, width=12)
    btn1.grid(row=2, column=0, padx=3, pady=3)
    btn2 = Button(basic_tab, text='2', fg='black', bg='light blue', command=lambda: press(2), height=2, width=12)
    btn2.grid(row=2, column=1, padx=3, pady=3)
    btn3 = Button(basic_tab, text='3', fg='black', bg='light blue', command=lambda: press(3), height=2, width=12)
    btn3.grid(row=2, column=2, padx=3, pady=3)
    btn4 = Button(basic_tab, text='4', fg='black', bg='light blue', command=lambda: press(4), height=2, width=12)
    btn4.grid(row=3, column=0, padx=3, pady=3)
    btn5 = Button(basic_tab, text='5', fg='black', bg='light blue', command=lambda: press(5), height=2, width=12)
    btn5.grid(row=3, column=1, padx=3, pady=3)
    btn6 = Button(basic_tab, text='6', fg='black', bg='light blue', command=lambda: press(6), height=2, width=12)
    btn6.grid(row=3, column=2, padx=3, pady=3)
    btn7 = Button(basic_tab, text='7', fg='black', bg='light blue', command=lambda: press(7), height=2, width=12)
    btn7.grid(row=4, column=0, padx=3, pady=3)
    btn8 = Button(basic_tab, text='8', fg='black', bg='light blue', command=lambda: press(8), height=2, width=12)
    btn8.grid(row=4, column=1, padx=3, pady=3)
    btn9 = Button(basic_tab, text='9', fg='black', bg='light blue', command=lambda: press(9), height=2, width=12)
    btn9.grid(row=4, column=2, padx=3, pady=3)
    btn0 = Button(basic_tab, text='0', fg='black', bg='light blue', command=lambda: press(0), height=2, width=12)
    btn0.grid(row=5, column=0, padx=3, pady=3)

    # Operator buttons
    plus = Button(basic_tab, text='+', fg='black', bg='light blue', command=lambda: press('+'), height=2, width=12)
    plus.grid(row=2, column=3, padx=3, pady=3)
    minus = Button(basic_tab, text='-', fg='black', bg='light blue', command=lambda: press('-'), height=2, width=12)
    minus.grid(row=3, column=3, padx=3, pady=3)
    mult = Button(basic_tab, text='*', fg='black', bg='light blue', command=lambda: press('*'), height=2, width=12)
    mult.grid(row=4, column=3, padx=3, pady=3)
    div = Button(basic_tab, text='/', fg='black', bg='light blue', command=lambda: press('/'), height=2, width=12)
    div.grid(row=5, column=3, padx=3, pady=3)

    # Other buttons
    eq = Button(basic_tab, text='=', fg='black', bg='light blue', command=equal, height=2, width=12)
    eq.grid(row=6, column=2, padx=3, pady=3)
    clr = Button(basic_tab, text='Clear', fg='black', bg='light blue', command=clear, height=2, width=12)
    clr.grid(row=6, column=1, padx=3, pady=3)
    dot = Button(basic_tab, text='.', fg='black', bg='light blue', command=lambda: press('.'), height=2, width=12)
    dot.grid(row=6, column=0, padx=3, pady=3)
    opprnts = Button(basic_tab, text="(", fg='black', bg='light blue', command=lambda: press('('), height=2, width=12) 
    opprnts.grid(row=5, column=1, padx=3, pady=3) 
    clprnts = Button(basic_tab, text=")", fg='black', bg='light blue', command=lambda: press(')'), height=2, width=12) 
    clprnts.grid(row=5, column=2, padx=3, pady=3)
    backspc = Button(basic_tab, text="⌫", fg='black', bg='light blue', command=backspace, height=2, width=12)
    backspc.grid(row=6, column=3, padx=3, pady=3)
    history_box = Listbox(basic_tab, height=10, width=35)
    history_box.grid(row=7, column=0, columnspan=4, rowspan=2, padx=5, pady=5, sticky="ew")
    history_box.insert(END, " History")

    ##Advance tab
    advanced_display = StringVar()
    advanced_entry = Entry(advanced_tab, textvariable=advanced_display)
    advanced_entry.grid(row=0, column=0, columnspan=4,  ipady=8, sticky="ew")


    #numbers, decimal and backspace buttons
    buttons = [
    ("1", 2, 0), ("2", 2, 1), ("3", 2, 2),
    ("4", 3, 0), ("5", 3, 1), ("6", 3, 2),
    ("7", 4, 0), ("8", 4, 1), ("9", 4, 2),
    ("0", 5, 0), (".", 5, 1),]

    for text, row, col in buttons:
       button = Button(advanced_tab, text=text, fg='black', bg='light blue',height=2, width=12, command=lambda value=text: advanced_press(value))
       button.grid(row=row, column=col, padx=3, pady=3, sticky='nsew')
    bckspc_button = Button(advanced_tab, text="⌫", fg='black', bg='light blue', height=2, width=12, command=advanced_backspace)
    bckspc_button.grid(row=5, column=2, padx=3, pady=3, sticky='nsew')

    #scientific function and clear buttons
    functions = [
    ("x²", "square", 2, 3),
    ("√x", "sqrt", 3, 3),
    ("1/x", "reciprocal", 4, 3),
    ("n!", "factorial", 5, 3),
    ("% ", "percent", 6, 0),
    ("sin", "sin", 6, 1),
    ("cos", "cos", 6, 2),
    ("tan", "tan", 6, 3),
    ("log", "log", 7, 0),
    ("ln", "ln", 7, 1),]

    for label, function, row, col in functions:
       button = Button(advanced_tab, text=label, fg='black', bg='light blue',height=2, width=12, command=lambda f=function: advanced_calculate(f))
       button.grid(row=row, column=col, padx=3, pady=3, sticky='nsew')
    clr_button = Button(advanced_tab, text="Clear", fg='black', bg='light blue',height=2, width=12, command=advanced_clear)
    clr_button.grid(row=7, column=2, columnspan=2, padx=3, pady=3, sticky="nsew")
    degree_button = Button(advanced_tab, text="DEG", fg='black', bg='light blue',height=2, width=12, command=set_degrees)
    degree_button.grid(row=8, column=0, columnspan=2, padx=3, pady=3, sticky='nsew')
    radian_button = Button(advanced_tab, text="RAD", fg='black',bg='light blue', height=2, width=12, command=set_radians)
    radian_button.grid(row=8, column=2, columnspan=2, padx=3, pady=3, sticky='nsew' )
    ad_history_box = Listbox(advanced_tab, height=5, width=35)
    ad_history_box.grid(row=9, column=0, columnspan=4, padx=5, pady=5, sticky='nsew')
    ad_history_box.insert(END, "History")
    ad_history_box.grid_rowconfigure(9, weight=1)

        # Unit Conversion tab
    conversion_category = StringVar(value="Length")
    from_unit_choice = StringVar(value="Meter")
    to_unit_choice = StringVar(value="Kilometer")
    conversion_input = StringVar()

    label1 = Label(conversion_tab, text="Choose a conversion type:", font=("Arial",15,"bold"), fg='white', bg="#1e1e2e", anchor='w')
    label1.grid(row=0, column=0, columnspan=2, padx=16, pady=(18, 12), sticky='ew')

    category_menu = ttk.Combobox(conversion_tab, textvariable=conversion_category,
        values=["Length", "Weight", "Temperature"], state="readonly")
    category_menu.grid(row=1, column=0, columnspan=4, padx=16, pady=(0, 14), sticky='ew')

    label2 = Label(conversion_tab, text="Value:", fg='white', bg='#1e1e2e', anchor='e')
    label2.grid(row=2, column=0, padx=(16, 10), pady=7, sticky='e')
    conversion_entry = Entry(conversion_tab, textvariable=conversion_input)
    conversion_entry.grid(row=2, column=1, padx=(0, 16), pady=7, sticky='ew')

    label3 = Label(conversion_tab, text="From:", fg='white', bg='#1e1e2e', anchor='e')
    label3.grid(row=3, column=0, padx=(16, 10), pady=7, sticky='e')
    from_menu = ttk.Combobox(conversion_tab, textvariable=from_unit_choice, state="readonly")
    from_menu.grid(row=3, column=1, padx=(0, 16), pady=7, sticky='ew')

    label4 = Label(conversion_tab, text="To:", fg='white', bg='#1e1e2e', anchor='e')
    label4.grid(row=4, column=0, padx=(16, 10), pady=7, sticky='e')
    to_menu = ttk.Combobox(conversion_tab, textvariable=to_unit_choice, state="readonly")
    to_menu.grid(row=4, column=1, padx=(0, 16), pady=7, sticky='ew')

    conversion_tab.grid_columnconfigure(0, weight=0, minsize=82)
    conversion_tab.grid_columnconfigure(1, weight=1)
    convert_button = Button(conversion_tab, text="Convert",fg='black', bg='light blue', command=convert_units)
    convert_button.grid(row=5, column=0, columnspan=2, padx=16, pady=(14, 8), sticky='ew')

    clear_button = Button(conversion_tab, text="Clear", fg='black', bg='light blue', command=lambda: (conversion_input.set(""),conversion_result.config(text="Result:")))
    clear_button.grid(row=7, column=0, columnspan=2, padx=16, pady=(8, 14), sticky='ew')

    conversion_result = Label(conversion_tab, text="Enter value to convert into other unit.", fg='white', bg='#1e1e2e', anchor="center")
    conversion_result.grid(row=6, column=0, columnspan=2, padx=16, pady=8, sticky='ew')

    # Update available units when the category changes
    unit_options = {
        "Length": ["Millimeter", "Centimeter", "Meter", "Kilometer", "Inch", "Foot", "Mile"],
        "Weight": ["Milligram", "Gram", "Kilogram", "Ounce", "Pound"],
        "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],}

    def update_unit_choices(event=None):
        units = unit_options[conversion_category.get()]
        from_menu["values"] = units
        to_menu["values"] = units
        from_unit_choice.set(units[0])
        to_unit_choice.set(units[1])

    category_menu.bind("<<ComboboxSelected>>", update_unit_choices)
    update_unit_choices()

    # Graph tab: enter values manually or load columns from CSV/Excel
    x_values_input = StringVar(value="")
    y_values_input = StringVar(value="")
    chart_type = StringVar(value="Line")
    graph_file_path = StringVar(value="")
    graph_headers = []
    graph_rows = []

    def load_graph_file():
        path = filedialog.askopenfilename(title="Choose data file",
            filetypes=[("CSV and Excel files", "*.csv *.xlsx *.xlsm"),
                      ("CSV files", "*.csv"),
                      ("Excel workbooks", "*.xlsx *.xlsm")])
        if not path:
            return
        try:
            suffix = Path(path).suffix.lower()
            if suffix == ".csv":
                with open(path, "r", newline="", encoding="utf-8-sig") as data_file:
                    rows = list(csv.reader(data_file))
            elif suffix in (".xlsx", ".xlsm"):
                try:
                    from openpyxl import load_workbook
                except ImportError as error:
                    raise ValueError("Excel support needs openpyxl. Install it with: pip install openpyxl") from error
                workbook = load_workbook(path, read_only=True, data_only=True)
                sheet = workbook.active
                rows = list(sheet.iter_rows(values_only=True))
                workbook.close()
            else:
                raise ValueError("Choose a .csv, .xlsx, or .xlsm file.")

            if len(rows) < 2:
                raise ValueError("The file needs a header row and at least one data row.")
            graph_headers[:] = [str(value).strip() if value is not None and str(value).strip()
                                else f"Column {index + 1}" for index, value in enumerate(rows[0])]
            graph_rows[:] = [list(row) for row in rows[1:] if row and any(value is not None and str(value).strip() for value in row)]
            if not graph_rows:
                raise ValueError("No data rows were found below the header.")
            x_column_menu["values"] = graph_headers
            y_column_menu["values"] = graph_headers
            x_column.set(graph_headers[0])
            y_column.set(graph_headers[1] if len(graph_headers) > 1 else graph_headers[0])
            graph_file_path.set(Path(path).name)
            graph_status.config(text=f"Loaded {len(graph_rows)} rows from {Path(path).name}")
        except (OSError, ValueError, csv.Error) as error:
            messagebox.showerror("Could not load data", str(error), parent=root)

    def get_selected_column_values(column_name):
        column_index = graph_headers.index(column_name)
        values = []
        for row in graph_rows:
            if column_index >= len(row) or row[column_index] is None or not str(row[column_index]).strip():
                continue
            values.append(row[column_index])
        return values

    x_label = Label(graph_tab, text="X values (comma-separated):", fg='white', bg='#1e1e2e')
    x_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    x_input = Entry(graph_tab, textvariable=x_values_input, width=35)
    x_input.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    y_label = Label(graph_tab, text="Y values (comma-separated):", fg='white', bg='#1e1e2e')
    y_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    y_input = Entry(graph_tab, textvariable=y_values_input, width=35)
    y_input.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    file_button = Button(graph_tab, text="Load CSV / Excel File", command=load_graph_file, fg='black', bg='light blue')
    file_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
    file_label = Label(graph_tab, textvariable=graph_file_path, fg='white', bg='#1e1e2e', anchor="w")
    file_label.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    x_column = StringVar()
    y_column = StringVar()
    x_input_label = Label(graph_tab, text="X column:", fg='white', bg='#1e1e2e')
    x_input_label.grid(row=3, column=0, padx=5, pady=3, sticky="w")
    x_column_menu = ttk.Combobox(graph_tab, textvariable=x_column, state="readonly")
    x_column_menu.grid(row=3, column=1, padx=5, pady=3, sticky="ew")
    y_input_label = Label(graph_tab, text="Y column:", fg='white', bg='#1e1e2e')
    y_input_label.grid(row=4, column=0, padx=5, pady=3, sticky="w")
    y_column_menu = ttk.Combobox(graph_tab, textvariable=y_column, state="readonly")
    y_column_menu.grid(row=4, column=1, padx=5, pady=3, sticky="ew")

    chrt_typ = Label(graph_tab, text="Chart type:", fg='black', bg='light blue')
    chrt_typ.grid(row=5, column=0, padx=5, pady=5, sticky="ew")
    chart_menu = ttk.Combobox(graph_tab, textvariable=chart_type,
        values=["Line", "Bar", "Horizontal Bar", "Scatter", "Pie"], state="readonly", width=16)
    chart_menu.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

    figure = Figure(figsize=(5, 3.5), dpi=100)
    axes = figure.add_subplot(111)
    canvas = FigureCanvasTkAgg(figure, master=graph_tab)
    canvas.get_tk_widget().grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

    graph_status = Label(graph_tab, text="Enter matching X and Y values or load a data file.", fg='white', bg='#1e1e2e')
    graph_status.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

    def draw_chart():
        try:
            if graph_rows and x_column.get() and y_column.get():
                x_index = graph_headers.index(x_column.get())
                y_index = graph_headers.index(y_column.get())
                pairs = []
                for row in graph_rows:
                    if x_index >= len(row) or y_index >= len(row):
                        continue
                    xv, yv = row[x_index], row[y_index]
                    if xv is None or yv is None or not str(xv).strip() or not str(yv).strip:
                        continue
                    try:
                        pairs.append((float(xv), float(yv), str(xv)))
                    except(TypeError, ValueError):
                        continue
                if not pairs:
                    raise ValueError("Selected columnmust containnumeric X and Y values")    
                x_values = [item[0] for item in pairs]
                y_values = [item[1] for item in pairs]
                pie_labels = [item[2] for item in pairs]
            else:
                x_values = [float(value.strip()) for value in x_values_input.get().split(",") if value.strip()]
                y_values = [float(value.strip()) for value in y_values_input.get().split(",") if value.strip()]
                pie_labels = [str(value) for value in x_values]

            if not x_values or len(x_values) != len(y_values):
                raise ValueError("Enter the same number of X and Y values.")

            axes.clear()
            selected_chart = chart_type.get()
            if selected_chart == "Line":
                axes.plot(x_values, y_values, marker="o")
            elif selected_chart == "Bar":
                axes.bar(x_values, y_values)
            elif selected_chart == "Horizontal Bar":
                axes.barh(x_values, y_values)
            elif selected_chart == "Scatter":
                axes.scatter(x_values, y_values)
            elif selected_chart == "Pie":
                if any(value < 0 for value in y_values) or sum(y_values) <= 0:
                    raise ValueError("Pie chart needs non-negative Y values with a positive total.")
                axes.pie(y_values, labels=pie_labels, autopct="%1.1f%%")
            if selected_chart != "pie":
                axes.set_xlabel(x_column.get() or "X")
                axes.set_ylabel(y_column.get() or "Y")
                axes.grid(True)
            axes.set_title(f"{selected_chart} Chart")
            figure.tight_layout()
            canvas.draw()
            graph_status.config(text=f"{selected_chart} chart drawn with {len(x_values)} points.")
        except(ValueError, OverflowError) as error:
            graph_status.config(text=f"Check your data: {error}")
            
    def clear_chart():
        x_values_input.set("")
        y_values_input.set("")
        graph_file_path.set("")
        graph_headers.clear()
        graph_rows.clear()
        x_column_menu["values"] = []
        y_column_menu["values"] = []
        x_column.set("")
        y_column.set("")
        axes.clear()
        canvas.draw()
        graph_status.config(text="Enter matching X and Y values or load a data file.")

    chart_button = Button(graph_tab, text="Draw Chart", command=draw_chart, fg='black', bg='light blue')
    chart_button.grid(row=6, column=0, padx=5, pady=5, sticky="ew")
    clr_button1 = Button(graph_tab, text="Clear", command=clear_chart, fg='black', bg='light blue')
    clr_button1.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

    graph_tab.grid_rowconfigure(7, weight=1)
    graph_tab.grid_columnconfigure(1, weight=1)

     # BMI calculator tab (weight in kilograms, height in centimeters)
    bmi = Label(bmi_tab, text="BMI Calculator", font=("Arial", 16, "bold"), fg="white", bg="#1e1e2e")
    bmi.grid(row=0, column=0, columnspan=2, padx=12, pady=14)

    weight = Label(bmi_tab, text="Weight (kg):", fg="white", bg="#1e1e2e")
    weight.grid(row=1, column=0, padx=12, pady=8, sticky="e")
    bmi_weight = StringVar()
    enter_weight = Entry(bmi_tab, textvariable=bmi_weight)
    enter_weight.grid(row=1, column=1, padx=12, pady=8, sticky="ew")

    height = Label(bmi_tab, text="Height (cm):", fg="white", bg="#1e1e2e")
    height.grid(row=2, column=0, padx=12, pady=8, sticky="e")
    bmi_height = StringVar()
    enter_height = Entry(bmi_tab, textvariable=bmi_height)
    enter_height.grid(row=2, column=1, padx=12, pady=8, sticky="ew")

    bmi_button = Button(bmi_tab, text="Calculate BMI", command=calculate_bmi, fg="black", bg="light blue")
    bmi_button.grid(row=3, column=0, columnspan=2, padx=12, pady=12, sticky="ew")
    bmi_result = Label(bmi_tab, text="Enter your height and weight.", fg="white", bg="#1e1e2e", anchor='center')
    bmi_result.grid(row=4, column=0, columnspan=2, padx=12, pady=10, sticky="ew")
    bmi_tab.grid_columnconfigure(1, weight=1)

    clr_bmi = Button(bmi_tab, text="Clear", command=clear_bmi, fg="black", bg="light blue")
    clr_bmi.grid(row=5, column=0,columnspan=2, padx=12, pady=12, sticky="ew")

    msg_label = Label(bmi_tab, text="The BMI category is based on the calculated BMI.", fg='white', bg='#1e1e2e')
    msg_label.grid(row=6, column=0, columnspan=2, sticky='ew')
    msg_lebel1 = Label(bmi_tab, text="Underweight: BMI below 18.5", fg='white', bg='#1e1e2e')
    msg_lebel1.grid(row=7, column=0, columnspan=2)
    msg_label2 = Label(bmi_tab, text="Normal range: BMI from 18.5 to 25", fg='white', bg='#1e1e2e')
    msg_label2.grid(row=8, column=0, columnspan=2)
    msg_label3 = Label(bmi_tab, text="Overweight: BMI from 25 to 35", fg='white', bg='#1e1e2e')
    msg_label3.grid(row=9, column=0, columnspan=2)
    msg_label4 = Label(bmi_tab, text="Obesity range: BMI 30 or higher", fg='white', bg='#1e1e2e')
    msg_label4.grid(row=10, column=0, columnspan=2)

    # GST calculator tab
    gst_label = Label(gst_tab, text="GST Calculator", font=("Arial", 16, "bold"), fg="white", bg="#1e1e2e")
    gst_label.grid(row=0, column=0, columnspan=2, padx=12, pady=14)
    amt_label = Label(gst_tab, text="Amount:", fg="white", bg="#1e1e2e")
    amt_label.grid(row=1, column=0, padx=12, pady=8, sticky="e")
    gst_amount = StringVar()
    gst = Entry(gst_tab, textvariable=gst_amount)
    gst.grid(row=1, column=1, padx=12, pady=8, sticky="ew")

    rate_label = Label(gst_tab, text="GST rate (%):", fg="white", bg="#1e1e2e")
    rate_label.grid(row=2, column=0, padx=12, pady=8, sticky="e")
    gst_rate = StringVar(value="18")
    rate = ttk.Combobox(gst_tab, textvariable=gst_rate, values=["0.25%", "1.5%", "3%","5%","18%","40%"])
    rate.grid(row=2, column=1, padx=12, pady=8, sticky="ew")

    amt_type = Label(gst_tab, text="Amount type:", fg="white", bg="#1e1e2e")
    amt_type.grid(row=3, column=0, padx=12, pady=8, sticky="e")
    gst_mode = StringVar(value="Exclusive of GST")
    gst_combobox = ttk.Combobox(gst_tab, textvariable=gst_mode,
        values=["Exclusive of GST", "Inclusive of GST"], state="readonly")
    gst_combobox.grid(row=3, column=1, padx=12, pady=8, sticky="ew")

    calc_button = Button(gst_tab, text="Calculate GST", command=calculate_gst, fg="black", bg="light blue")
    calc_button.grid(row=4, column=0, columnspan=2, padx=12, pady=12, sticky="ew")
    gst_result = Label(gst_tab, text="Enter an Amount and select GST rate.", fg="white", bg="#1e1e2e")
    gst_result.grid(row=5, column=0, columnspan=2, padx=12, pady=10, sticky="ew")
    gst_tab.grid_columnconfigure(1, weight=1)

    clr_gst = Button(gst_tab, text="Clear", command=clear_gst, fg="black", bg="light blue")
    clr_gst.grid(row=6, column=0,columnspan=2, padx=12, pady=12, sticky="ew")

    note_label1 = Label(gst_tab, text="There are special rates of 0.25%, 1.5% & 3% for precious stones & metals. " , fg='white', bg='#1e1e2e')
    note_label1.grid(row=8, column=0, columnspan=2)
    note_label2 = Label(gst_tab, text="The 40% GST rate applies to selected luxury goods and services.", fg='white', bg='#1e1e2e')
    note_label2.grid(row=9, column=0, columnspan=2)
    note_label = Label(gst_tab, text="", bg='#1e1e2e')
    note_label.grid(row=10, column=0, columnspan=2)
    note_label3 = Label(gst_tab, text="Here the GST includes 50% CGST and 50% SGST.", fg='white', bg='#1e1e2e')
    note_label3.grid(row=11, column=0, columnspan=2)
    note_label4 = Label(gst_tab, text="In 18% GST - 9% CGST and 9% SGST.", fg='white', bg='#1e1e2e')
    note_label4.grid(row=12, column=0, columnspan=2)

    root.mainloop()