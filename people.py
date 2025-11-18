import random

class PeopleGenerator:
 #Möglichkeiten
    def __init__(self, total_users: int):
        self.total_users = total_users

        self.ranges = {
            "Economic": (0.30, 0.70),
            "moderate": (0.10, 0.25),
            "luxurious": (0.01, 0.10),
        }

    def generate(self):
        #genel bir oran
        c_raw = random.uniform(*self.ranges["Economic"])
        m_raw = random.uniform(*self.ranges["moderate"])
        l_raw = random.uniform(*self.ranges["luxurious"])

        # oran tam bir değilse oranları toplayıp bölüyor hepsine böylelikle yüzde olarak her zaman sadece %100 oluyor elimizde
        #wunderlich
        total_raw = c_raw + m_raw + l_raw
        Economic_p = c_raw / total_raw
        moderate_p = m_raw / total_raw
        luxurious_p = l_raw / total_raw

        # Yukarıdan aldığımız oranlarla çarpıyoruz böylelikle yüzdelik dilimlerimiz doğru oluyor her zaman (=-=)
        Economic_count = int(self.total_users * Economic_p)
        moderate_count = int(self.total_users * moderate_p)

        # eğer gine beceremezsek sona kalan 1-2 kişiyi luxuriousa atıyoruz
        luxurious_count = self.total_users - Economic_count - moderate_count

        # liste çıkartıyoruz
        users = {
            "Economic": [f"user_{i}" for i in range(1, Economic_count + 1)],
            "moderate": [
                f"user_{i}" for i in range(
                    Economic_count + 1,
                    Economic_count + moderate_count + 1
                )
            ],
            "luxurious": [
                f"user_{i}" for i in range(
                    Economic_count + moderate_count + 1,
                    self.total_users + 1
                )
            ],
        }

        return users
#Studie Deutsch