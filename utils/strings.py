



class Strings():

    def add_commas(num: str):
        """ add commas to large numbers to make them more readable """
        new_num = ""
        rev_num = num[::-1]
        if len(num) < 4: return num

        for idx, char in enumerate(rev_num):
            if idx % 3 == 0 and idx != 0:
                new_num = char + "," + new_num
            else:
                new_num = char + new_num

        return new_num