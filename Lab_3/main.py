from account import CasionClient, CasinoMode
import random

def get_report(client, mode):
    client.become_a_billionaire()
    print(f'{mode.value} mode:balance {client.balance}', end='\n\n')


if __name__ == "__main__":
    
    for  mode in CasinoMode:
        client = CasionClient(random.randint(1e2, 1e6), mode)
        get_report(client, mode)

        


         
