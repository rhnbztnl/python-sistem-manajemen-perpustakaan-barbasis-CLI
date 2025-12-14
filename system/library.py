import json
from datetime import date, timedelta 

from system.book import Book
from system.lib.member import Member
from system.lib.borrowing import Borrowing

from rich.console import Console
from rich.table import Table
from rich.panel import Panel


console = Console()

class Library :
    
    def __init__(self, file_path="system/lib/database/storage.json") :
        self.file_path = file_path
        self.books = []
        self.member = []
        self.borrows = []
        self.load()
    
    # Load and Save
    def load(self) :
        try :
            with open(self.file_path, "r") as f :
                data = json.load(f)
                
            self.books = [Book.from_dict(b) for b in data.get("books", [])]
            self.member = [Member.from_dict(m) for m in data.get("members", [])]
            self.borrows = [Borrowing.from_dict(br) for br in data.get("borrows", [])]
            
        except FileNotFoundError :
            self.books = []
            self.member = []
            self.borrows = []
            self.save()
            
    def save(self) :
        data = {
            "books": [b.info() for b in self.books],
            "members": [m.into_dict() for m in self.member],
            "borrows": [br.into_dict() for br in self.borrows]
        }
        
        with open(self.file_path, "w") as f :
            json.dump(data, f , indent=4)
            
    # Utility
    def find_book_by_id(self, book_id) :
        for b in self.books :
            if b.id == book_id :
                return b
            
        return None
    
    def find_member_by_id(self, id_member) :
        for m in self.member :
            if m.id_member == id_member :
                return m
            
        return None
    
    # Add member
    def add_member(self, name, alamat) :
        if any(m.name == name for m in self.member) :
            console.print(Panel.fit(f"[red]'{name}' sudah terdaftar dalam member![/]"))
            return
        
        new_id = 1 if not self.member else max(m.id_member for m in self.member) + 1
        member = Member(new_id, name, alamat)
        
        self.member.append(member)
        self.save()
        
        console.print(Panel.fit(f"[green]'{name}' berhasil mendaftar dengan ID = {new_id}[/]"))
    
    # remove member
    def remove_member(self, id_member) :
        member = self.find_member_by_id(id_member)
        
        if not member:
            console.print(Panel.fit("[red]Member tidak ditemukan[/]"))
            return
        
        self.member.remove(member)
        self.save()
        console.print(Panel.fit(f"[green]Member dengan ID {id_member} telah dihapus.[/]"))

    # Add book
    def add_book(self, judul, penulis, tanggal, kategori) :
        if any(b.judul == judul for b in self.books) :
            console.print(Panel.fit(f"[red]Buku '{judul}' sudah ada didalam dafar![/]"))
            return
        
        new_id = 1 if not self.books else max(b.id for b in self.books) + 1
        book = Book(new_id, judul, penulis, tanggal, kategori)
        
        self.books.append(book)
        self.save()
        
        console.print(Panel.fit(f"[green]Buku '{judul}' berhasil ditambahkan dengan ID = {new_id}[/]"))
        
    # remove book
    def remove_book(self, book_id) :
        book = self.find_book_by_id(book_id)
        
        if not book:
            console.print(Panel.fit("[red]Buku tidak ditemukan[/]"))
            return
        
        self.books.remove(book)
        self.save()
        console.print(Panel.fit(f"[green]Buku ID {book_id} telah dihapus.[/]"))
    
    # Borrow book
    def borrow(self, book_id, member: Member) :
        book = self.find_book_by_id(book_id)
        
        if not book :
            console.print(Panel.fit("[red]Buku tidak ada![/]"))
            return
        
        member = self.find_member_by_id(member.id_member)
        if not member :
            console.print(Panel.fit("[red]Member tidak ada[/]"))
            return
        
        if not member.can_borrow_a_book() :
            console.print(Panel.fit(f"[red]Batas pinjaman member telah tercapai!.[/]"))
            return
        
        if not book.borrow() :
            console.print(Panel.fit("[red]Buku sedang dipinjam.[/]"))
            return
        
        transaction_id = len(self.borrows) + 1
        date_borrowed = date.today()
        due_date = date.today() + timedelta(days=7)
        borrows = Borrowing(
            transaction_id = transaction_id,
            book_id = book_id,
            member_id = member.id_member,
            date_borrowed = date_borrowed, 
            due_date = due_date,
        )
        
        self.borrows.append(borrows)
        member.borrow_a_book(book_id)
        self.save()
        
        console.print(Panel.fit(f"[green]Buku '{book.judul}' berhasil dipinjam oleh {member.name}[/]"))
                   
    # return book
    def return_book(self, book_id, member: Member) :
        book = self.find_book_by_id(book_id)
        
        if not book :
            console.print(Panel.fir("[red]Buku tidak ada![/]"))
            return
                        
        if not book.status :
            console.print(Panel.fit("[red]Buku ini belum dipinjam[/]"))
            return

        member = self.find_member_by_id(member.id_member)
        if not member :
            console.print(Panel.fit("[red]Member tidak terdaftar![/]"))
            return
    
        borrows = next(
            (br for br in self.borrows
            if br.book_id == book_id and br.member_id == member.id_member and br.return_date is None),
            None
        )
        
        if not borrows :
            console.print(Panel.fit("[red]Transaksi tidak ditemukan[/]"))
            return
        
        borrows.return_book()
        member.return_a_book(book_id)            
        book.return_book()
        
        fine = borrows.calculate_fine()
        if fine > 0 :
            console.print(
                Panel.fit(
                    f"""[red]Buku '{book.judul}' terlambat dikembalikan.
                    Denda: Rp{fine}[/]
                    """)
                )
        else :
            console.print(Panel.fit(f"[green]buku '{book.judul}' Berhasil dikembalikan tepat waktu[/]."))
                
        self.save()
            
    # search
    def search_by_writer(self, writer) :
        result = [b for b in self.books if writer.lower() in b.penulis.lower()]
        
        if not result :
            console.print(Panel.fit("[red]Tidak ada buku dengan nama penulis itu[/]"))
        else :
            console.print("[green]Buku ditemukan : [/]")
            for b in result :
                console.print(Panel.fit(f"[cyan]-{b.id}.[/] [greeb]'{b.judul}'[/]"))
                
    def search_by_title(self, judul) :
        result = [b for b in self.books if judul.lower() in b.judul.lower()]
        
        if not result :
            console.print(Panel.fit("[red]Buku dengan judul tersebut tidak ditemukan[/]"))
        else :
            console.print("[green]Buku ditemukan : [/]")
            for b in result :
                console.print(Panel.fit(f"[cyan]-{b.id}.[/] [greeb]'{b.judul}'[/]"))
                
    # show member
    def show_members(self) :
        if not self.member :
            console.print(Panel.fit("[red]Belum ada member.[/]"), justify="center")
            return
                
        table = Table(title="MEMBER", expand=True)
        
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("NAMA", justify="center", style="magenta")
        table.add_column("ALAMAT", justify="center", style="green")
        table.add_column("PINJAMAN", justify="right", style="green")
        
        for m in self.member :
            pinjaman = m.daftar_pinjaman
            table.add_row(f"{m.id_member}", f"{m.name}", f"{m.alamat}", f"{pinjaman}")

        if table.columns :
            console.print(table)
        else :
            console.print("[i]Tidak ada data[/]")

    # show book
    def show_books(self) :
        if not self.books :
            console.print(Panel.fit("[red]Belum ada buku.[/]"), justify="center")
            return

        table = Table(title="BUKU", expand=True)
        
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("PENULIS",justify="center", style="magenta")
        table.add_column("JUDUL", justify="right", style="green")
        table.add_column("TANGGAL", justify="right", style="green")
        table.add_column("STATUS", justify="center", style="green")
        
        for b in self.books :
            sts = "Dipinjam" if b.status else "Tersedia"
            table.add_row(f"{b.id}", f"{b.penulis}", f"{b.judul}", f"{b.tanggal}", f"{sts}")

        if table.columns :
            console.print(table)
        else :
            console.print("[i]Tidak ada data[/]")