import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector
import random
import datetime


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Snigdh@0610",  
    database="banking"
)
cursor = conn.cursor()


class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Snigdha Online Banking System")
        self.root.geometry("400x550")
        self.root.config(bg="#e0f7fa")  
        self.current_user = None
        self.login_screen()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_screen(self):
        self.clear()

        tk.Label(self.root, text="Login", font=("Arial", 18), bg="#e0f7fa", fg="#00796b").pack(pady=20)

        tk.Label(self.root, text="Account Number or Name", bg="#e0f7fa", fg="#00796b").pack()
        self.acc_entry = tk.Entry(self.root, width=30)
        self.acc_entry.pack()

        tk.Label(self.root, text="PIN", bg="#e0f7fa", fg="#00796b").pack()
        self.pin_entry = tk.Entry(self.root, show="*", width=30)
        self.pin_entry.pack()

        tk.Button(self.root, text="Login", command=self.login, width=20, bg="#00796b", fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Sign Up", command=self.signup_screen, width=20, bg="#ff7043", fg="white", font=("Arial", 12)).pack()
        tk.Button(self.root, text="Exit", command=self.root.quit, width=20, bg="#d32f2f", fg="white", font=("Arial", 12)).pack(pady=10)

    def signup_screen(self):
        self.clear()
        tk.Label(self.root, text="Create New Account", font=("Arial", 16), bg="#e0f7fa", fg="#00796b").pack(pady=20)

        tk.Label(self.root, text="Full Name", bg="#e0f7fa", fg="#00796b").pack()
        self.name_entry = tk.Entry(self.root, width=30)
        self.name_entry.pack()

        tk.Label(self.root, text="Choose PIN", bg="#e0f7fa", fg="#00796b").pack()
        self.pin_entry = tk.Entry(self.root, show='*', width=30)
        self.pin_entry.pack()

        tk.Button(self.root, text="Register", command=self.create_account, width=20, bg="#00796b", fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Back to Login", command=self.login_screen, width=20, bg="#ff7043", fg="white", font=("Arial", 12)).pack()

    def create_account(self):
        name = self.name_entry.get().strip()
        pin = self.pin_entry.get().strip()

        if not name or not pin or len(pin) < 4:
            messagebox.showerror("Error", "Enter a name and 4-digit PIN.")
            return

        while True:
            acc_no = str(random.randint(1000, 9999))
            cursor.execute("SELECT * FROM users WHERE acc_no=%s", (acc_no,))
            if not cursor.fetchone():
                break

        cursor.execute("INSERT INTO users (acc_no, name, pin, balance) VALUES (%s, %s, %s, 0)",
                       (acc_no, name, pin))
        conn.commit()
        messagebox.showinfo("Success", f"Account created!\nYour account number is {acc_no}")
        self.login_screen()

    def login(self):
        login_input = self.acc_entry.get().strip()
        pin = self.pin_entry.get().strip()

        cursor.execute(
            "SELECT acc_no FROM users WHERE (acc_no=%s OR name=%s) AND pin=%s",
            (login_input, login_input, pin)
        )
        result = cursor.fetchone()
        if result:
            self.current_user = result[0]
            self.dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid account number/name or PIN")

    def dashboard(self):
        self.clear()
        tk.Label(self.root, text="Dashboard", font=("Arial", 14), bg="#e0f7fa", fg="#00796b").pack(pady=10)

        tk.Button(self.root, text="Check Balance", width=30, bg="#00796b", fg="white", font=("Arial", 12), command=self.check_balance).pack(pady=5)
        tk.Button(self.root, text="Deposit Money", width=30, bg="#388e3c", fg="white", font=("Arial", 12), command=self.deposit_money).pack(pady=5)
        tk.Button(self.root, text="Withdraw Money", width=30, bg="#d32f2f", fg="white", font=("Arial", 12), command=self.withdraw_money).pack(pady=5)
        tk.Button(self.root, text="Transfer Funds", width=30, bg="#1976d2", fg="white", font=("Arial", 12), command=self.transfer_funds).pack(pady=5)
        tk.Button(self.root, text="Recent Transactions", width=30, bg="#8e24aa", fg="white", font=("Arial", 12), command=self.show_transactions).pack(pady=5)
        tk.Button(self.root, text="View Account Number", width=30, bg="#0288d1", fg="white", font=("Arial", 12), command=self.show_account_number).pack(pady=5)
        tk.Button(self.root, text="Logout", width=30, bg="#fbc02d", fg="white", font=("Arial", 12), command=self.logout).pack(pady=10)

    def logout(self):
        self.current_user = None
        self.login_screen()

    def check_balance(self):
        cursor.execute("SELECT balance FROM users WHERE acc_no=%s", (self.current_user,))
        balance = cursor.fetchone()[0]
        messagebox.showinfo("Balance", f"Your current balance is ₹{balance:.2f}")

    def deposit_money(self):
        amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:")
        if amount and amount > 0:
            cursor.execute("UPDATE users SET balance = balance + %s WHERE acc_no=%s", (amount, self.current_user))
            cursor.execute("INSERT INTO transactions (acc_no, type, amount) VALUES (%s, 'Deposit', %s)", (self.current_user, amount))
            conn.commit()
            messagebox.showinfo("Success", f"₹{amount:.2f} deposited successfully.")
        else:
            messagebox.showerror("Error", "Invalid amount.")

    def withdraw_money(self):
        amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")
        if amount and amount > 0:
            cursor.execute("SELECT balance FROM users WHERE acc_no=%s", (self.current_user,))
            balance = cursor.fetchone()[0]
            if balance >= amount:
                cursor.execute("UPDATE users SET balance = balance - %s WHERE acc_no=%s", (amount, self.current_user))
                cursor.execute("INSERT INTO transactions (acc_no, type, amount) VALUES (%s, 'Withdraw', %s)", (self.current_user, amount))
                conn.commit()
                messagebox.showinfo("Success", f"₹{amount:.2f} withdrawn successfully.")
            else:
                messagebox.showwarning("Insufficient Funds", "Not enough balance.")
        else:
            messagebox.showerror("Error", "Invalid amount.")

    def transfer_funds(self):
        to_acc = simpledialog.askstring("Transfer", "Enter recipient account number:")
        amount = simpledialog.askfloat("Transfer", "Enter amount to transfer:")
        if not to_acc or not amount or amount <= 0:
            messagebox.showerror("Error", "Invalid input.")
            return

        if to_acc == self.current_user:
            messagebox.showerror("Error", "Cannot transfer to your own account.")
            return

        cursor.execute("SELECT * FROM users WHERE acc_no=%s", (to_acc,))
        if not cursor.fetchone():
            messagebox.showerror("Error", "Recipient account not found.")
            return

        cursor.execute("SELECT balance FROM users WHERE acc_no=%s", (self.current_user,))
        current_balance = cursor.fetchone()[0]
        if current_balance < amount:
            messagebox.showerror("Error", "Insufficient balance.")
            return

        cursor.execute("UPDATE users SET balance = balance - %s WHERE acc_no=%s", (amount, self.current_user))
        cursor.execute("UPDATE users SET balance = balance + %s WHERE acc_no=%s", (amount, to_acc))
        cursor.execute("INSERT INTO transactions (acc_no, type, amount) VALUES (%s, 'Transfer to %s', %s)", (self.current_user, to_acc, amount))
        cursor.execute("INSERT INTO transactions (acc_no, type, amount) VALUES (%s, 'Transfer from %s', %s)", (to_acc, self.current_user, amount))
        conn.commit()
        messagebox.showinfo("Success", f"₹{amount:.2f} transferred to {to_acc}.")

    def show_transactions(self):
        cursor.execute("SELECT type, amount, timestamp FROM transactions WHERE acc_no=%s ORDER BY timestamp DESC LIMIT 5", (self.current_user,))
        records = cursor.fetchall()
        if not records:
            messagebox.showinfo("Transactions", "No recent transactions.")
            return
        msg = "\n".join([f"{t[2].strftime('%Y-%m-%d %H:%M')} | {t[0]}: ₹{t[1]:.2f}" for t in records])
        messagebox.showinfo("Recent Transactions", msg)

    def show_account_number(self):
        messagebox.showinfo("Account Info", f"Your account number is: {self.current_user}")


if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()
