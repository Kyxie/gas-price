class Info:
    def __init__(self, day, date, regu, regu_change, prem, prem_change):
        self.day = day
        self.date = date
        self.regu = regu
        self.regu_change = regu_change
        self.prem = prem
        self.prem_change = prem_change

    def __repr__(self):
        # 打印类
        return f"Info(day={self.day}, date={self.date}, regu={self.regu}, regu_change={self.regu_change}, prem={self.prem}, prem_change={self.prem_change})"
