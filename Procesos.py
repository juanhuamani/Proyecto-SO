import psutil
import tkinter as tk
from tkinter import ttk
from queue import Queue
import threading
import time

class MonitorProcesos:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Monitor de Procesos")

        self.procesos_impresos = set()
        self.procesos_a_excluir = ["unattended-upgr", "apt-check"]
        self.cola_procesos = Queue()
        self.tiempo_actual = 2

        self.inicializar_interfaz()

        self.hilo_interfaz = threading.Thread(target=self.actualizar_interfaz, daemon=True)
        self.hilo_interfaz.start()

        self.contador_inicio = time.time()
        self.iniciar_bucle_impresion()

        self.lista_fcfs_en_ejecucion.pack_forget()
        self.lista_fcfs_cola.pack_forget()
        self.lista_round_robin_en_ejecucion.pack_forget()
        self.lista_round_robin_cola.pack_forget()
        self.lista_prioridad_en_ejecucion.pack_forget()
        self.lista_prioridad_cola.pack_forget()

    def inicializar_interfaz(self):
        # Estilo para los widgets
        estilo = ttk.Style()
        estilo.configure("TButton", padding=6, relief="flat", background="#4CAF50", foreground="white")
        estilo.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        estilo.configure("Treeview", fieldbackground="#E3E3E3", background="#E3E3E3", foreground="black")

        self.crear_marco_cpu()
        self.crear_marco_procesos()
        self.crear_marco_fcfs()
        self.crear_marco_round_robin()
        self.crear_marco_prioridad()

    def crear_marco_cpu(self):
        marco_cpu = ttk.Frame(self.ventana)
        marco_cpu.pack(side=tk.TOP, padx=10, pady=10)
        etiqueta_cpu = ttk.Label(marco_cpu, text="Información de CPU", font=('Helvetica', 12, 'bold'))
        etiqueta_cpu.pack()

    def crear_marco_procesos(self):
        marco_procesos = ttk.Frame(self.ventana)
        marco_procesos.pack(side=tk.LEFT, padx=10, pady=10)
        etiqueta_procesos = ttk.Label(marco_procesos, text="Cola de Procesos", font=('Helvetica', 12, 'bold'))
        etiqueta_procesos.pack()

        columnas_procesos = ("PID", "Nombre", "Tiempo de CPU", "Tiempo de Llegada", "Prioridad")
        self.lista_procesos = ttk.Treeview(marco_procesos, columns=columnas_procesos, show="headings")
        for col in columnas_procesos:
            self.lista_procesos.heading(col, text=col)

        self.lista_procesos.column("PID", width=50)
        self.lista_procesos.column("Nombre", width=100)
        self.lista_procesos.column("Tiempo de CPU", width=80)
        self.lista_procesos.column("Tiempo de Llegada", width=100)
        self.lista_procesos.column("Prioridad", width=80)

        self.lista_procesos.config(height=20)
        self.lista_procesos.pack()

    def crear_marco_fcfs(self):
        marco_fcfs = ttk.Frame(self.ventana)
        marco_fcfs.pack(side=tk.RIGHT, padx=10, pady=10)
        etiqueta_fcfs = ttk.Label(marco_fcfs, text="Algoritmo FCFS", font=('Helvetica', 12, 'bold'))
        etiqueta_fcfs.pack()

        columnas_fcfs_en_ejecucion = ("Información")
        self.lista_fcfs_en_ejecucion = ttk.Treeview(marco_fcfs, columns=columnas_fcfs_en_ejecucion, show="headings")
        self.lista_fcfs_en_ejecucion.heading("Información", text="Procesos en Ejecución")
        self.lista_fcfs_en_ejecucion.column("Información", width=300)
        self.lista_fcfs_en_ejecucion.config(height=10)
        self.lista_fcfs_en_ejecucion.pack()

        columnas_fcfs_cola = ("Información")
        self.lista_fcfs_cola = ttk.Treeview(marco_fcfs, columns=columnas_fcfs_cola, show="headings")
        self.lista_fcfs_cola.heading("Información", text="Cola de Procesos")
        self.lista_fcfs_cola.column("Información", width=300)
        self.lista_fcfs_cola.config(height=10)
        self.lista_fcfs_cola.pack()

        self.boton_mostrar_fcfs = ttk.Button(marco_fcfs, text="Mostrar FCFS", command=self.alternar_fcfs)
        self.boton_mostrar_fcfs.pack()

    def crear_marco_round_robin(self):
        marco_round_robin = ttk.Frame(self.ventana)
        marco_round_robin.pack(side=tk.RIGHT, padx=10, pady=10)
        etiqueta_round_robin = ttk.Label(marco_round_robin, text="Algoritmo Round Robin", font=('Helvetica', 12, 'bold'))
        etiqueta_round_robin.pack()

        columnas_round_robin_en_ejecucion = ("Información")
        self.lista_round_robin_en_ejecucion = ttk.Treeview(marco_round_robin, columns=columnas_round_robin_en_ejecucion, show="headings")
        self.lista_round_robin_en_ejecucion.heading("Información", text="Procesos en Ejecución")
        self.lista_round_robin_en_ejecucion.column("Información", width=300)
        self.lista_round_robin_en_ejecucion.config(height=10)
        self.lista_round_robin_en_ejecucion.pack()

        columnas_round_robin_cola = ("Información")
        self.lista_round_robin_cola = ttk.Treeview(marco_round_robin, columns=columnas_round_robin_cola, show="headings")
        self.lista_round_robin_cola.heading("Información", text="Cola de Procesos")
        self.lista_round_robin_cola.column("Información", width=300)
        self.lista_round_robin_cola.config(height=10)
        self.lista_round_robin_cola.pack()

        self.boton_mostrar_round_robin = ttk.Button(marco_round_robin, text="Mostrar Round Robin", command=self.alternar_round_robin)
        self.boton_mostrar_round_robin.pack()

    def crear_marco_prioridad(self):
        marco_prioridad = ttk.Frame(self.ventana)
        marco_prioridad.pack(side=tk.RIGHT, padx=10, pady=10)
        etiqueta_prioridad = ttk.Label(marco_prioridad, text="Algoritmo de Prioridad", font=('Helvetica', 12, 'bold'))
        etiqueta_prioridad.pack()

        columnas_prioridad_en_ejecucion = ("Información")
        self.lista_prioridad_en_ejecucion = ttk.Treeview(marco_prioridad, columns=columnas_prioridad_en_ejecucion, show="headings")
        self.lista_prioridad_en_ejecucion.heading("Información", text="Procesos en Ejecución")
        self.lista_prioridad_en_ejecucion.column("Información", width=300)
        self.lista_prioridad_en_ejecucion.config(height=10)
        self.lista_prioridad_en_ejecucion.pack()

        columnas_prioridad_cola = ("Información")
        self.lista_prioridad_cola = ttk.Treeview(marco_prioridad, columns=columnas_prioridad_cola, show="headings")
        self.lista_prioridad_cola.heading("Información", text="Cola de Procesos")
        self.lista_prioridad_cola.column("Información", width=300)
        self.lista_prioridad_cola.config(height=10)
        self.lista_prioridad_cola.pack()

        self.boton_mostrar_prioridad = ttk.Button(marco_prioridad, text="Mostrar Prioridad", command=self.alternar_prioridad)
        self.boton_mostrar_prioridad.pack()

    def imprimir_nuevos_procesos(self):
        procesos = [p.info for p in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'create_time', 'nice'])]
        procesos_importantes = [p for p in procesos if p['cpu_percent'] > 5]
        procesos_nuevos = [p for p in procesos_importantes if p['pid'] not in self.procesos_impresos and p['name'] not in self.procesos_a_excluir]
        tiempo_transcurrido = int(time.time() - self.contador_inicio)

        for proceso in procesos_nuevos:
            pid = proceso['pid']
            nombre = proceso['name']
            usuario = proceso['username']
            cpu_percent = proceso['cpu_percent']
            tiempo_entrada = int(proceso['create_time'] - self.contador_inicio)
            tiempo_cpu = int(cpu_percent * tiempo_transcurrido / 100)

            if tiempo_entrada >= self.tiempo_actual:
                self.tiempo_actual = tiempo_entrada
                prioridad = proceso['nice']
                self.procesos_impresos.add(pid)
                self.cola_procesos.put((pid, nombre, tiempo_cpu, tiempo_entrada, prioridad))

        self.ventana.after(1000, self.imprimir_nuevos_procesos)

    def actualizar_interfaz(self):
        while True:
            try:
                info_proceso = self.cola_procesos.get_nowait()
                self.lista_procesos.insert("", "end", values=info_proceso)
            except:
                pass

    def iniciar_bucle_impresion(self):
        self.ventana.after(1000, self.imprimir_nuevos_procesos)

    def alternar_fcfs(self):
        if self.boton_mostrar_fcfs.cget("text") == "Mostrar FCFS":
            self.ocultar_algoritmos()
            self.lista_fcfs_en_ejecucion.pack()
            self.lista_fcfs_cola.pack()
            self.boton_mostrar_fcfs.config(text="Ocultar FCFS")
        else:
            self.lista_fcfs_en_ejecucion.pack_forget()
            self.lista_fcfs_cola.pack_forget()
            self.boton_mostrar_fcfs.config(text="Mostrar FCFS")

    def alternar_round_robin(self):
        if self.boton_mostrar_round_robin.cget("text") == "Mostrar Round Robin":
            self.ocultar_algoritmos()
            self.lista_round_robin_en_ejecucion.pack()
            self.lista_round_robin_cola.pack()
            self.boton_mostrar_round_robin.config(text="Ocultar Round Robin")
        else:
            self.lista_round_robin_en_ejecucion.pack_forget()
            self.lista_round_robin_cola.pack_forget()
            self.boton_mostrar_round_robin.config(text="Mostrar Round Robin")

    def alternar_prioridad(self):
        if self.boton_mostrar_prioridad.cget("text") == "Mostrar Prioridad":
            self.ocultar_algoritmos()
            self.lista_prioridad_en_ejecucion.pack()
            self.lista_prioridad_cola.pack()
            self.boton_mostrar_prioridad.config(text="Ocultar Prioridad")
        else:
            self.lista_prioridad_en_ejecucion.pack_forget()
            self.lista_prioridad_cola.pack_forget()
            self.boton_mostrar_prioridad.config(text="Mostrar Prioridad")

    def ocultar_algoritmos(self):
        self.lista_fcfs_en_ejecucion.pack_forget()
        self.lista_fcfs_cola.pack_forget()
        self.lista_round_robin_en_ejecucion.pack_forget()
        self.lista_round_robin_cola.pack_forget()
        self.lista_prioridad_en_ejecucion.pack_forget()
        self.lista_prioridad_cola.pack_forget()

# Crear la interfaz gráfica y la instancia de la clase MonitorProcesos
ventana = tk.Tk()
monitor = MonitorProcesos(ventana)

# Iniciar el bucle de la interfaz gráfica
ventana.mainloop()