import textwrap as t

task = {'Query 1 ': t.dedent("""
                        A customer claims she forgot her bag in a car and asks to help. She was using 
                        cars several times this day, but she believes the right car was red and its 
                        plate starts with “AN”. Find all possible cars that match the description. 
                        """),
        'Query 2 ': t.dedent("""
                        Company management wants to get a statistics on the efficiency of charging stations 
                        utilization. Given a date, compute how many sockets were occupied each hour. 
                         """),
        'Query 3 ': t.dedent("""
                        Company management considers using price increasing coefficients. They need to gather 
                        statistics for one week on how many cars are busy (% to the total amount of taxis) during  
                        the morning (7AM - 10 AM), afternoon (12AM - 2PM) and evening (5PM - 7PM) time. 
                       """),
        'Query 4 ': t.dedent("""A
                        customer claims that he was charged twice for the trip, but he can’t say exactly what 
                        day it happened (he deleted notification from his phone and he is too lazy to ask the bank) 
                        so you need to check all his payments for the last month to be be sure that nothing was doubled. 
                       """),
        'Query 5 ': t.dedent("""
                        The department of development has requested the following statistics: 
                        - Average distance a car has to travel per day to customer’s order location 
                        - Average trip duration 
                        Given a date as an input, compute the statistics above. 
                        """),
        'Query 6 ': t.dedent("""
                        In order to accommodate traveling demand, the company decided to distribute cars 
                        according to demand locations. Your task is to compute top-3 most popular pick-up locations 
                        and travel destination for each time of day: morning (7am-10am), afternoon 
                        (12am-2pm) and evening (5pm-7pm). 
                        """),
        'Query 7 ': t.dedent("""
                        Despite the wise management, the company is going through hard times and can’t afford 
                        anymore to maintain the current amount of self-driving cars. The management decided to stop 
                        using 10% of all self-driving cars, which take least amount of orders for the last 3 months. 
                        """),
        'Query 8 ': t.dedent("""
                        The company management decided to participate in the research on “does customer location 
                        of residence depend on how many charging station the self-driving cars was using the same 
                        day”. Now you as DB developer need to provide this data. You’ve  decided to collect the data 
                        for each day within one month and then sum them up. 
                        """),
        'Query 9 ': t.dedent("""
                        The company management decided to optimize repair costs by buying parts in bulks from 
                        providers for every workshop. Help them decide which parts are used the most every week 
                        by every workshop and compute the necessary amount of parts to order. 
                        """),
        'Query 10 ': t.dedent("""
                        The company management decided to cut costs by getting rid of the most expensive car to 
                        maintain. Find out which car type has had the highest average (per day) cost of repairs and 
                        charging (combined). 
                        """)}
