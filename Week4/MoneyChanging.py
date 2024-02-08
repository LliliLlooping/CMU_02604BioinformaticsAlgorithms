from typing import List, Dict
import numpy as np
from copy import deepcopy

class MoneyChanging:
    def __init__(self):
        pass
    
    def dp_change_naive(self, money: int, coins: List[int]) -> int:
        """
            Args:
                money (int): an integer money
                coins (List[int]): an array Coins = (coin1, ..., coind).

            Returns:
                int: The minimum number of coins with denominations Coins that changes money.
        """
        
        # Identify the min coin
        min_coin = min(coins)
        
        # Allocate space for the dp array
        dp_array = np.zeros(money + 1, dtype=int)
        
        for i in range(min_coin, money + 1):
            
            # starts from the min_coin, but the array starts from zero
            # calculate the offset here
            i_adjusted = i - min_coin
            
            # is one of the coin
            if i in coins:
                dp_array[i_adjusted] = 1
                
            # otherwise
            else:
                dp_array[i_adjusted] = min([dp_array[i_adjusted-coin] for coin in coins if i > coin]) + 1
        
        return dp_array[money - min_coin]
    
    def dp_change(self, money: int, coins: List[int]) -> int:
        """
            No sacrifice in speed, but decrease space complexity from O(money) to O(max(coins))
            Args:
                money (int): an integer money
                coins (List[int]): an array Coins = (coin1, ..., coind).

            Returns:
                int: The minimum number of coins with denominations Coins that changes money.
        """
        
        # Identify the min coin
        min_coin, width = min(coins), max(coins)
        
        # Allocate space for the dp array
        dp_array = np.zeros(width, dtype=int)
        
        for i in range(min_coin, money + 1):
            
            # starts from the min_coin, but the array starts from zero
            # calculate the offset here
            i_adjusted = i - min_coin
            
            # calculate the write-to position in the dp array
            write_index = i_adjusted % width
            
            # is one of the coin
            if i in coins:
                dp_array[write_index] = 1
                
            # otherwise
            else:
                dp_array[write_index] = min([dp_array[(i_adjusted - coin) % width] for coin in coins if i > coin]) + 1
                
        return dp_array[(money - min_coin) % width]
    
    def dp_change_verbose(self, money: int, coins: List[int]) -> Dict[int, int]:
        """
            Displays the composition of coins instead of a single count.
            Args:
                money (int): an integer money
                coins (List[int]): an array Coins = (coin1, ..., coind).

            Returns:
                Dict[int, int]: The composition of coins when achieving the minimum number of coins with denominations Coins that changes money.
        """
        
        # Identifies the min coin
        min_coin, width = min(coins), max(coins) + 1
        
        # Generates the coin index
        coins_map = {coin: i for i, coin in enumerate(coins)}
        
        # Allocates space for the dp array
        dp_array = np.zeros((width, len(coins)), dtype=int)
        
        for i in range(min_coin, money + 1):
            
            # Starts from the min_coin, but the array starts from zero
            # Calculates the offset here
            i_adjusted = i - min_coin
            
            # Calculates the write-to position in the dp array
            write_index = i_adjusted % width
            
            # Re-initializes the write-to row
            dp_array[write_index, :] = 0
            
            # Is one of the coin
            if i in coins:
                dp_array[write_index, coins_map[i]] = 1
                
            # Otherwise
            else:
                
                # Lists all potential pre-steps
                potential_rows = []
                potential_coins = []
                for coin in coins:
                    if i > coin:
                        potential_rows.append(dp_array[(i_adjusted - coin) % width, :])
                        potential_coins.append(coin)
                
                # picks one
                picked_row_idx = np.argmin(np.sum(np.array(potential_rows), axis=1))
                picked_row = potential_rows[picked_row_idx]
                picked_coin = potential_coins[picked_row_idx]
                
                # updates the array
                dp_array[write_index, :] = picked_row
                dp_array[write_index, coins_map[picked_coin]] += 1
        
        # Slice the row corresponds to 'money'
        coins_count = dp_array[(money - min_coin) % width, :]
        
        # Maps the coins to their count
        result = {coin: coins_count[i] for i, coin in enumerate(coins)}
        
        return result
    
    def test(self):
        
        # money = 7
        # coins = [1, 5]
        
        money = 8074
        coins = [24, 13, 12, 7, 5, 3, 1]
        
        result = self.dp_change_naive(money, coins)
        assert result == 338
        
        result = self.dp_change(money, coins)
        assert result == 338
        
        result = self.dp_change_verbose(money, coins)
        print('Do these (denomination, count) pairs add up to 8074?')
        print(result)
        print()