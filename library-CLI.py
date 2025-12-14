from system.library import Library as lib

from rich.panel import Panel
from rich.console import Console
from rich.prompt import Prompt

import os
import platform

console = Console()
prompt = Prompt()
lib = lib()
# add book
# lib.add_book("Terjadinya penebangan hutan di sumatra", "Reyhan Buztanil", "1/1/2001", "Berita")

# add member
# lib.add_member("reyhan", "banjar")


# borrow
# member = lib.find_member_by_id(1)
# lib.borrow(1, member)

# return
# lib.return_book(1, member)

# remove
# lib.remove_member(1)
# lib.remove_book(1)

# search
# lib.search_by_title("Hutan")
# lib.search_by_writer("Reyhan")

# lib.show_members()
# lib.show_books()

def clear() :
    os.system("cls" if platform.system() == "Windows" else "clear")

def help() :
    console.print(
        Panel.fit(
f"""
[green]'exit'[/] untuk keluar dari program.
[green]'add book'[/] untuk menambahkan sebuah buku keperpustakaan.
[green]'remove book'[/] untuk menghapus sebuah buku diperpustakaan.
[green]'search'[/] untuk mencari ID dari sebuah buku.
[green] - Penulis[/]
[green] - Judul[/]
[green]'membership'[/] untuk bergabung keperpustakaan dan agar bisa meminjam sebuah buku.
[green]'borrow book'[/] untuk meminjam sebuah buku diperpustakaan.
[green]'return book'[/] untuk mengembalikan buku yang sudah dipinjam.
""",
title="HELP",
border_style="cyan"
              )
        )
    console.input("Tekan enter untuk kembali...")

def perpustakaan() :

    player = True
    
    
    while (player) :
        clear()
    
        lib.show_members()    
        lib.show_books()
                
        command = console.input("Tekan [green]'help'[/] untuk melihat fitur.\n>> ")

                
        if command.lower() == 'help' :
            help()
            continue
        
        if command.lower() == 'exit' :
            console.rule("[green]Terimakasih telah menggunakan program ini.[/]")
            player = False
        
        elif command.lower() == 'add book' :
            lib.add_book(
                    input("Masukkan judul buku : "),
                    input("Masukkan nama penulis : "),
                    input("Masukkan tanggal/tahun/bulan : "),
                    input("Masukkan genre buku : ")
                    )
            console.input("Tekan enter untuk kembali...")
            
        
        elif command.lower() == 'remove book' :
            lib.remove_book(int(input("Masukkan ID buku : ")))
            console.input("Tekan enter untuk kembali...")
        
        elif command.lower() == 'search' :
            command = input("Kamu ingin mencari berdasarkan apa\n>> ")
            console.input("Tekan enter untuk kembali...")
            
            if command.lower() == 'help' :
                help()
                console.input("Tekan enter untuk kembali...")
            elif command.lower() == 'judul' :
                lib.search_by_title(input("Masukkan judul nya : "))
                console.input("Tekan enter untuk kembali...")
            elif command.lower() == 'penulis' :
                lib.search_by_writer(input("Masukkan penulisnya : "))
                console.input("Tekan enter untuk kembali...")

        elif command.lower() == 'membership' :
            lib.add_member(
                input("Masukkan nama : "),
                input("Masukkan alamat : ")
                )
            console.input("Tekan enter untuk kembali...")
            
        elif command.lower() == 'borrow book' :
            lib.borrow(
                int(input("Masukkan ID dari buku : ")),
                lib.find_member_by_id(int(input("Masukkan ID dari member : ")))
            )
            console.input("Tekan enter untuk kembali...")
            
        elif command.lower() == 'return book' :
            lib.return_book(
                int(input("Masukkan ID dari buku : ")),
                lib.find_member_by_id(int(input("Masukkan ID dari member : ")))
            )
            console.input("Tekan enter untuk kembali...")
        
        else : 
            console.print(Panel.fit(f"[red]'{command}'[/] tidak ada"))
            console.input("Tekan enter untuk kembali...")
        

console.rule("Sistem Manajemen Perpustakaan")
perpustakaan()
