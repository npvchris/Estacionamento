import tkinter as tk
from tkinter import messagebox, Label, Entry, Button, Text
from datetime import datetime
import os

# Define a tarifa por hora
TARIFA_HORARIA = 15.00

# Informações sobre o estacionamento
INFO_ESTACIONAMENTO = """Estapar Estacionamento
End: Rua Gloria da Patria, 222, Sao Paulo
Telefone: 2020-5598
"""

# Função para registrar a entrada do veículo
def registrar_entrada():
    placa = entrada_placa.get().strip().upper()
    veiculo = entrada_veiculo.get().strip()
    cor = entrada_cor.get().strip()
    modelo = entrada_modelo.get().strip()
    avarias = entrada_avarias.get("1.0", tk.END).strip()
    
    if placa and veiculo and cor and modelo:
        hora_entrada = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        nome_arquivo = f"{placa}.txt"
        with open(nome_arquivo, "w") as arquivo:
            arquivo.write(INFO_ESTACIONAMENTO)
            arquivo.write(f"\nVeículo: {veiculo}")
            arquivo.write(f"\nCor: {cor}")
            arquivo.write(f"\nModelo: {modelo}")
            arquivo.write(f"\nAvarias: {avarias}")
            arquivo.write(f"\nPlaca: {placa}")
            arquivo.write(f"\nHora de Entrada: {hora_entrada}\n")
        
        messagebox.showinfo("Entrada Registrada", f"Veículo {placa} entrou às {hora_entrada}")
        limpar_campos_entrada()
    else:
        messagebox.showwarning("Entrada Inválida", "Por favor, preencha todas as informações do veículo.")

# Função para registrar a saída do veículo
def registrar_saida():
    placa = entrada_placa.get().strip().upper()
    nome_arquivo = f"{placa}.txt"
    
    if placa and os.path.exists(nome_arquivo):
        with open(nome_arquivo, "a") as arquivo:
            hora_entrada_str = None
            for linha in open(nome_arquivo):
                if linha.startswith("Hora de Entrada:"):
                    hora_entrada_str = linha.split(": ")[1].strip()
                    break
            if hora_entrada_str:
                hora_entrada = datetime.strptime(hora_entrada_str, '%Y-%m-%d %H:%M:%S')
                hora_saida = datetime.now()
                duracao_estacionado = hora_saida - hora_entrada
                horas_estacionadas = duracao_estacionado.total_seconds() / 3600
                custo_total = horas_estacionadas * TARIFA_HORARIA
                arquivo.write(f"Hora de Saída: {hora_saida.strftime('%Y-%m-%d %H:%M:%S')}\n")
                arquivo.write(f"Tempo Estacionado: {horas_estacionadas:.2f} horas\n")
                arquivo.write(f"Total a Pagar: R${custo_total:.2f}\n")
            
            messagebox.showinfo("Saída Registrada", f"Veículo {placa} ficou estacionado por {horas_estacionadas:.2f} horas.\nTotal a pagar: R${custo_total:.2f}")
            limpar_campos_entrada()
    else:
        messagebox.showwarning("Saída Inválida", "Placa não encontrada ou veículo não registrado.")

# Função para limpar os campos de entrada
def limpar_campos_entrada():
    entrada_placa.delete(0, tk.END)
    entrada_veiculo.delete(0, tk.END)
    entrada_cor.delete(0, tk.END)
    entrada_modelo.delete(0, tk.END)
    entrada_avarias.delete("1.0", tk.END)

# Configuração da janela principal do aplicativo
root = tk.Tk()
root.title("Sistema de Estacionamento")

# Carregar e exibir a imagem
caminho_imagem = "estacionamento.png"  # Certifique-se de que esta imagem está no mesmo diretório que o script
if os.path.exists(caminho_imagem):
    imagem = tk.PhotoImage(file=caminho_imagem)
    label_imagem = Label(root, image=imagem)
    label_imagem.pack()

# Criar widgets de entrada
Label(root, text="Placa do Veículo:").pack()
entrada_placa = Entry(root)
entrada_placa.pack()

Label(root, text="Veículo:").pack()
entrada_veiculo = Entry(root)
entrada_veiculo.pack()

Label(root, text="Cor:").pack()
entrada_cor = Entry(root)
entrada_cor.pack()

Label(root, text="Modelo:").pack()
entrada_modelo = Entry(root)
entrada_modelo.pack()

Label(root, text="Avarias:").pack()
entrada_avarias = Text(root, height=4, width=40)
entrada_avarias.pack()

# Criar botões
Button(root, text="Registrar Entrada", command=registrar_entrada).pack()
Button(root, text="Registrar Saída", command=registrar_saida).pack()

# Executar o aplicativo
root.mainloop()
