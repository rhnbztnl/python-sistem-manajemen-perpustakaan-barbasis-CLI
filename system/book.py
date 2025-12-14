class Book :
        
    def __init__(self, book_id,  judul,  penulis,  tanggal, kategori, status=False ) :
            self.id = book_id
            self.judul = judul
            self.penulis = penulis
            self.tanggal = tanggal
            self.status = status
            self.kategori = kategori
            
    def borrow(self) :
        if self.status : return False
                
        self.status = True
        return True
            
    def return_book(self) :
        if not self.status : return False
        
        self.status = False
        return True
        
    def info(self) :
        return{
            "ID": self.id,
            "Judul": self.judul,
            "Penulis": self.penulis,
            "Tanggal": self.tanggal,
            "Kategori": self.kategori,
            "Status": self.status,
            }
        
        
    @staticmethod
    def from_dict(dict) :
        return Book(
            dict["ID"],
            dict["Judul"],
            dict.get("Penulis", []),
            dict["Tanggal"],
            dict.get("Kategori", []),
            dict["Status"]
        )