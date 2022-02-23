import time as t
import datetime as dt


class MtCracker():
    generator = None
    
    def __init__(self, client):
        self.reg_date = client.del_date - dt.timedelta(hours=3)
        if not client.real_numbers:
            client.play(1, 1)
            
        self.state = client.real_numbers[-1]
        
    def get_seed(self, seed, state):
        seed = next(iter(MT19937(seed)))
        return seed == state
    
    def set_generator(self):
        time_delta = 30000
        start = int(t.mktime(self.reg_date.timetuple())) - time_delta
        end = start + time_delta * 2
        
        found_seed = None
        for stamp in range(start, end + 1):
            if self.get_seed(stamp, self.state):
                found_seed = stamp
                
        if not found_seed:
            raise(Exception("No seed found"))
        else:
            self.seed = found_seed
            self.generator = iter(MT19937(found_seed))
            next(self.generator)
        
    def predict(self):
        if not self.generator:
            self.set_generator()
        return next(self.generator)


class BetterMtCracker():
    generator = None
    
    def __init__(self, client):
        self.client = client
        
        n_nums = len(client.real_numbers)
        if n_nums <= 624:
            for i in range(624 - n_nums):
                client.play(1, 1)
                
        assert len(client.real_numbers) == 624
        
    def set_generator(self):
        state = [self.untemper(num) for num in self.client.real_numbers]
        self.generator = MT19937(state=state)
        
    def predict(self):
        if not self.generator:
            self.set_generator()
        return next(self.generator)
        
    def untemper(self, y):
        (w, n, m, r) = (32, 624, 397, 31)
        a = 0x9908B0DF
        (u, d) = (11, 0xFFFFFFFF)
        (s, b) = (7, 0x9D2C5680)
        (t, c) = (15, 0xEFC60000)
        l = 18
        f = 1812433253

        def int_to_bit_list(x):
            return [int(b) for b in '{:032b}'.format(x)]

        def bit_list_to_int(l):
            return int(''.join(str(x) for x in l), base=2)

        def invert_shift_mask_xor(y, direction, shift, mask=0xFFFFFFFF):
            y = int_to_bit_list(y)
            mask = int_to_bit_list(mask)

            if direction == 'left':
                y.reverse()
                mask.reverse()
            else:
                assert direction == 'right'

            x = [None]*32
            for n in range(32):
                if n < shift:
                    x[n] = y[n]
                else:
                    x[n] = y[n] ^ (mask[n] & x[n-shift])

            if direction == 'left':
                x.reverse()

            return bit_list_to_int(x)

        xx = y
        xx = invert_shift_mask_xor(xx, direction='right', shift=l)
        xx = invert_shift_mask_xor(xx, direction='left', shift=t, mask=c)
        xx = invert_shift_mask_xor(xx, direction='left', shift=s, mask=b)
        xx = invert_shift_mask_xor(xx, direction='right', shift=u, mask=d)

        return xx

def MT19937(seed=5489, state=None):
    '''Mersenne-Twister PRNG, 32-bit version'''
    # parameters for MT19937
    (w, n, m, r) = (32, 624, 397, 31)
    a = 0x9908B0DF
    (u, d) = (11, 0xFFFFFFFF)
    (s, b) = (7, 0x9D2C5680)
    (t, c) = (15, 0xEFC60000)
    l = 18
    f = 1812433253

    # masks (to apply with an '&' operator)
    # ---------------------------------------
    # zeroes out all bits except "the w-r highest bits"
    # (i.e. with our parameters the single highest bit, since w-r=1)
    high_mask = ((1<<w) - 1) - ((1<<r) - 1)
    # zeroes out all bits excepts "the r lowest bits"
    low_mask = (1<<r)-1

    def twist(x):
        return (x >> 1)^a if (x % 2 == 1) else x >> 1

    if state == None:
        # initialization (populating the state)
        state = list()
        state.append(seed)
        for i in range(1, n):
            prev = state[-1]
            # the "& d" is to take only the lowest 32 bits of the result
            x = (f * (prev ^ (prev >> (w-2))) + i) & d
            state.append(x)

    while True:
        x = state[m] ^ twist((state[0] & high_mask) + (state[1] & low_mask))

        # tempering transform and output
        y = x ^ ((x >> u) & d)
        y = y ^ ((y << s) & b)
        y = y ^ ((y << t) & c)
        yield y ^ (y >> l)

        # note that it's the 'x' value
        # that we insert in the state
        state.pop(0)
        state.append(x)
