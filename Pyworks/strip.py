def main():
    str = "\"hello\" \"mushroom\""
    print str
    strlen = len(str.split("\""))
    print strlen
    print str.split("\"")[1].strip()
    print str.split("\"")[1]

main();
