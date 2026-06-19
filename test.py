try:
    with open("docs/Google.txt", "r", encoding="utf-8") as f:
        print(f.read())
except Exception as e:
    print(type(e))
    print(e)