import datetime

def exp_date(dc, t, ed):
    created = datetime.datetime.strptime(dc, "%d/%m/%Y")
    
    if t == "fruit" or t == "vegetable":
        exp = created + datetime.timedelta(days=7)
        return exp.day + "/" + exp.month + "/" + exp.year
    
    elif t == "canned":
        exp = created + datetime.timedelta(days=365*2)
        return exp.day + "/" + exp.month + "/" + exp.year
    
    elif t in ["beans", "rice", "honey", "ketchup", "syrup", "mustard", "oil", "salsa"]:
        exp = created + datetime.timedelta(days=365)
        return exp.day + "/" + exp.month + "/" + exp.year
    
    else:
        pass
        
    return ed
    