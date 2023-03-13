import tkinter as tk
from tkinter import messagebox
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas


class NewtonRaphsonGUI:
    global master
    def __init__(self, master):
        self.master = master
        master.title("Método de Newton-Raphson")
        
        
        self.result_label = tk.Label(self.master, text="")
        self.result_label.grid(row=7, columnspan=2)
        
        self.iteration_label = tk.Label(self.master, text="")
        self.iteration_label.grid(row=3, columnspan=2)
        
        # Crear etiqueta para mostrar el valor de x en la iteración actual
        
        self.x_label = tk.Label(master, text="")
        self.x_label.grid(row=4, column=2)
        # Crear widgets para ingresar la función y los parámetros
        tk.Label(master, text="Función:").grid(row=0)
        self.function_entry = tk.Entry(master, width=50)
        self.function_entry.grid(row=0, column=1)
        
        tk.Label(master, text="Tolerancia:").grid(row=1)
        self.tol_entry = tk.Entry(master, width=20)
        self.tol_entry.grid(row=1, column=1)
        
        tk.Label(master, text="Número máximo de iteraciones:").grid(row=2)
        self.n_entry = tk.Entry(master, width=20)
        self.n_entry.grid(row=2, column=1)
        
        tk.Label(master, text="Valor inicial:").grid(row=3)
        self.x0_entry = tk.Entry(master, width=20)
        self.x0_entry.grid(row=3, column=1)
        
        # Crear botón para ejecutar el método de Newton-Raphson
        self.newton_button = tk.Button(master, text="Calcular", command=self.newton_raphson)
        self.newton_button.grid(row=4, column=0)
        
        # Crear botón para graficar la función
        self.plot_button = tk.Button(master, text="Graficar", command=self.plot_function)
        self.plot_button.grid(row=5, column=0)
        
        # Crear figura y lienzo para graficar la función
        self.fig = plt.figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.canvas = FigureCanvas(self.fig, master=master)

        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=6, columnspan=2)
        
    def newton_raphson(self):
        iterations = ""
        # Obtener el valor de tolerancia y el número máximo de iteraciones ingresado por el usuario
        tol = float(self.tol_entry.get())
        n = int(self.n_entry.get())

        # Permitir al usuario ingresar un valor inicial por consola
        while True:
            try:
                x0 = float(self.x0_entry.get())
                break
            except ValueError:
                #messagebox.showerror("Error", "Ingrese un número válido para x0.").grid(row=7, columnspan=2)
                
                self.master.update()
        # Obtener la función ingresada por el usuario y crear una función sympy y lambdify
        x = sp.symbols('x')
        f = sp.sympify(self.function_entry.get())
        df = f.diff(x)
        f = sp.lambdify(x, f)
        df = sp.lambdify(x, df)

        # Realizar el método de Newton-Raphson
        x_iter = ''

        for k in range(n):
            x1 = x0 - (f(x0) / df(x0))
            iterations += "Iteración {}: x{} = {}\n".format(k+1, k+1, x1)
          
            
                # Graficar la iteración
            self.ax.plot([x0, x1], [f(x0), 0], color='blue', linestyle='--')
            self.ax.scatter(x1, f(x1), color='blue')
            self.canvas.draw()

            if abs(x1 - x0) < tol:
                self.result_label.configure(text="x{} = {} es la raíz aproximada".format(k+1, x1))
                # Marcar la raíz en la gráfica
                
                self.ax.scatter(x1, f(x1), color='green')
                self.canvas.draw()
                break

            x0 = x1
        self.x_label.configure(text=iterations)

    def plot_function(self):
        
        # Obtener la función ingresada por el usuario y crear una función sympy y lambdify
        x = sp.symbols('x')
        f = sp.sympify(self.function_entry.get())
        f = sp.lambdify(x, f)

        # Graficar la función
        x_vals = np.linspace(-10, 10, 1000)
        y_vals = f(x_vals)
        self.ax.clear()
        self.ax.plot(x_vals, y_vals)
        self.ax.set(xlabel='x', ylabel='y', title='Función')
        self.ax.grid()
        self.canvas.draw()

    def newton_raphson_with_plot(self):
        self.plot_button = tk.Button(master, text="Graficar", command=self.newton_raphson_with_plot)

        # Realizar la gráfica de la función
        self.plot_function()

        # Realizar el método de Newton-Raphson
        self.newton_raphson()
        
if __name__=='__main__':
    root=tk.Tk()
    nr_gui=NewtonRaphsonGUI(root)
    root.mainloop()
