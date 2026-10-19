import tkinter as tk
from tkinter import messagebox
import json
from web3 import Web3

# Подключаемся к локальному блокчейну (Remix VM или Ganache/Hardhat)
NODE_URL = "http://127.0.0.1:8545"
w3 = Web3(Web3.HTTPProvider(NODE_URL))

# ABI контракта Auction
AUCTION_ABI = json.loads(
    '[{"inputs":[{"internalType":"uint256","name":"_durationInSeconds","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"bid","stateMutability":"payable","type":"function"},{"inputs":[],"name":"endAuction","stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"highestBid","stateMutability":"view","type":"uint256"},{"inputs":[],"name":"highestBidder","stateMutability":"view","type":"address"}]')

# Адрес контракта (вставим тот, что выдаст Remix при деплое)
CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"

try:
    auction_contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=AUCTION_ABI)
except Exception:
    pass


def get_account():
    pk = pk_entry.get().strip()
    if not pk:
        messagebox.showerror("Помилка", "Введіть приватний ключ кошелька!")
        return None
    try:
        return w3.eth.account.from_key(pk)
    except Exception:
        messagebox.showerror("Помилка", "Невірний формат приватного ключа!")
        return None


def place_bid():
    account = get_account()
    if not account: return
    try:
        eth_amount = float(bid_entry.get())
        nonce = w3.eth.get_transaction_count(account.address)

        tx = auction_contract.functions.bid().build_transaction({
            'from': account.address,
            'value': w3.to_wei(eth_amount, 'ether'),
            'nonce': nonce,
            'gas': 300000,
            'gasPrice': w3.eth.gas_price
        })

        signed_tx = w3.eth.account.sign_transaction(tx, private_key=account.key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        w3.eth.wait_for_transaction_receipt(tx_hash)

        messagebox.showinfo("Успіх", "Ставка успішно прийнята аукціоном!")
        update_status()
    except Exception as e:
        messagebox.showerror("Помилка транзакції", str(e))


def update_status():
    try:
        leader = auction_contract.functions.highestBidder().call()
        max_bid = auction_contract.functions.highestBid().call()
        status_label.config(text=f"Лідер: {leader}\nСтавка: {w3.from_wei(max_bid, 'ether')} ETH")
    except Exception:
        status_label.config(text="Не вдалося оновити статус (Перевірте підключення)")


root = tk.Tk()
root.title("Аукціон з поверненням ставок (Варіант 11)")
root.geometry("450x400")

tk.Label(root, text="Введіть ваш приватний ключ (Приховано):", font=("Arial", 10, "bold")).pack(pady=10)
pk_entry = tk.Entry(root, show="*", width=50)
pk_entry.pack(pady=5)

tk.Label(root, text="--------------------------------------------------").pack()

tk.Label(root, text="Сума вашої ставки (в ETH):").pack(pady=5)
bid_entry = tk.Entry(root, width=20)
bid_entry.pack(pady=5)

btn_bid = tk.Button(root, text="Зробити ставку (Payable)", command=place_bid, bg="darkblue", fg="white",
                    font=("Arial", 11))
btn_bid.pack(pady=15)

status_label = tk.Label(root, text="Лідер: 0x00... \nСтавка: 0 ETH", fg="green", font=("Arial", 10))
status_label.pack(pady=10)

tk.Button(root, text="Оновити дані", command=update_status).pack()

root.mainloop()
