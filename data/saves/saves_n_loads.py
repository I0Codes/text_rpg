import json 


def savings(playeeeeeeeer_tat):
    try:
        with open("savegame.json", "w") as f:
            json.dump(playeeeeeeeer_tat, f)
        print("спи спокійно, гра збережена")
    except Exception as e:
        print(f"шось сталось, це не я якшо шо: {e}")
        
def london():
    try:
        with open("savegame.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("сейвів нема, починай з нуля.")
        return None