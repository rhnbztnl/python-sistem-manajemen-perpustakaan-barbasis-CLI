from datetime import date

class Borrowing :
     
    def __init__(self, transaction_id, book_id, member_id, date_borrowed, due_date):
        self.transaction_id = transaction_id
        self.book_id = book_id
        self.member_id = member_id
        self.date_borrowed = date_borrowed 
        self.due_date = due_date 
        self.return_date = None
        
    def return_book(self) :
        self.return_date = date.today()
    
    def is_late(self) :
        if self.return_date is None :
            return False
        return self.return_date > self.due_date
    
    def calculate_fine(self, fine_per_day=5000) :
        if not self.is_late() :
            return 0
        
        late_days = (self.return_date - self.due_date).days
        return late_days * fine_per_day
    
    def into_dict(self) :
        return {
            "transaction_id" : self.transaction_id, 
            "book_id" : self.book_id,
            "member_id" : self.member_id,
            "date_borrowed" : self.date_borrowed.isoformat(), 
            "due_date" : self.due_date.isoformat(),
            "return_date" : self.return_date.isoformat() if self.return_date else None
        }
        
    @classmethod
    def from_dict(cls, data) :
        obj = cls(
            transaction_id = data["transaction_id"],
            book_id = data["book_id"],
            member_id = data["member_id"],
            date_borrowed = date.fromisoformat(data["date_borrowed"]), 
            due_date = date.fromisoformat(data["due_date"]), 
        )
        
        obj.return_date = (
            date.fromisoformat(data["return_date"])
            if data.get("return_date",) else None
        )
        
        return obj
