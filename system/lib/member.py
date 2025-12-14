class Member :
    
    def __init__(self, id_member, name, alamat, daftar_pinjaman=None, maksimal_pinjaman = 4) :
        self.id_member = id_member
        self.name = name
        self.alamat = alamat
        self.daftar_pinjaman = daftar_pinjaman or []
        self.maksimal_pinjaman = maksimal_pinjaman
        
    def can_borrow_a_book(self) :
        return len(self.daftar_pinjaman) < self.maksimal_pinjaman

    def borrow_a_book(self, book) :
        if not self.can_borrow_a_book() :
            print("Buku yang dipinjam sudah mencapai batas!")
            return
        
        self.daftar_pinjaman.append(book)
        print(f"Buku '{book}' berhasil dipinjam atas nama {self.name}.")
    
    def return_a_book(self, book) :
        if book not in self.daftar_pinjaman :
            print("Buku tesebut tidak ada dalam daftar pinjaman.")
            return
        
        self.daftar_pinjaman.remove(book)
        print(f"Buku '{book}' telah berhasil dikembalikan oleh {self.name}.")
        
    def into_dict(self) :
        return{
            "ID_Member" : self.id_member,
            "Name" : self.name,
            "Alamat" : self.alamat,
            "Borrowing" : self.daftar_pinjaman,
            "Max_borrow": self.maksimal_pinjaman
        }
        
    @staticmethod
    def from_dict(data) :
        return Member(
            data["ID_Member"],    
            data["Name"],
            data["Alamat"],
            data.get("Borrowing", []),
            data.get("Max_borrow", 4)
        )