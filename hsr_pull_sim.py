import random

ch_rateup = 0.5625
lc_rateup = 0.78125
ch_odds = 0.006
lc_odds = 0.008
ch_soft_pity = 74
lc_soft_pity = 66
ch_hard_pity = 90
lc_hard_pity = 80
ch_pity_inc = 0.06
lc_pity_inc = 0.07

#0 = rateup won
#1 = rateup lost
#2 = didn't get
def pull(current_pity, is_char, has_guarantee):
    if is_char:
        odds = ch_odds
        if current_pity == ch_hard_pity:
            odds = 1
        elif current_pity >= ch_soft_pity:
            odds = ch_odds + (current_pity - ch_soft_pity + 1) * ch_pity_inc
        if random.random() < odds:
            if has_guarantee or random.random() < ch_rateup:
                return 0
            else:
                return 1
        else:
            return 2
    else:
        odds = lc_odds
        if current_pity == lc_hard_pity:
            odds = 1
        elif current_pity >= lc_soft_pity:
            odds = lc_odds + (current_pity - lc_soft_pity + 1) * lc_pity_inc
        if random.random() < odds:
            if has_guarantee or random.random() < lc_rateup:
                #print("LC")
                return 0
            else:
                #print("Other LC")
                return 1
        else:
            return 2
        

def pull_sim(attempts, pulls, desired_num_ch, desired_num_lc, current_pity_ch_param, current_pity_lc_param, has_guarantee_ch, has_guarantee_lc, ch_banner_first):
    print(f"Simming {attempts} attempts of {pulls} pulls trying to get E{desired_num_ch-1}S{desired_num_lc}")
    successes = 0
    result_dict = dict()
    for i in range(attempts):
        #print("Attempt " + str(i + 1))
        remaining_pulls = pulls
        obtained_ch = 0
        obtained_lc = 0
        have_guarantee_ch = has_guarantee_ch
        have_guarantee_lc = has_guarantee_lc
        current_pity_ch = current_pity_ch_param
        current_pity_lc = current_pity_lc_param

        while remaining_pulls > 0 or (obtained_ch == 7 and obtained_lc == 5):
            if ch_banner_first == True:
                if obtained_lc < desired_num_lc:
                    pull_lc = pull(current_pity_lc, True, have_guarantee_lc)
                    remaining_pulls -= 1
                    if pull_lc == 0:
                        obtained_lc += 1
                        have_guarantee_lc = False
                        current_pity_lc = 0
                    elif pull_lc == 1:
                        have_guarantee_lc = True
                        current_pity_lc = 0
                    else:
                        current_pity_lc += 1
                elif obtained_ch < desired_num_ch:
                    pull_ch = pull(current_pity_ch, True, have_guarantee_ch)
                    remaining_pulls -= 1
                    if pull_ch == 0:
                        obtained_ch += 1
                        have_guarantee_ch = False
                        current_pity_ch = 0
                    elif pull_ch == 1:
                        have_guarantee_ch = True
                        current_pity_ch = 0
                    else:
                        current_pity_ch += 1
                else:
                    successes += 1
                    break
            else:
                if obtained_ch < desired_num_ch:
                    pull_ch = pull(current_pity_ch, True, have_guarantee_ch)
                    remaining_pulls -= 1
                    if pull_ch == 0:
                        obtained_ch += 1
                        have_guarantee_ch = False
                        current_pity_ch = 0
                    elif pull_ch == 1:
                        have_guarantee_ch = True
                        current_pity_ch = 0
                    else:
                        current_pity_ch += 1
                elif obtained_lc < desired_num_lc:
                    pull_lc = pull(current_pity_lc, True, have_guarantee_lc)
                    remaining_pulls -= 1
                    if pull_lc == 0:
                        obtained_lc += 1
                        have_guarantee_lc = False
                        current_pity_lc = 0
                    elif pull_lc == 1:
                        have_guarantee_lc = True
                        current_pity_lc = 0
                    else:
                        current_pity_lc += 1
                else:
                    successes += 1
                    break
        result = f"E{obtained_ch - 1}S{obtained_lc}" + (" with guaranteed character" if have_guarantee_ch else "") + (" with guaranteed LC" if have_guarantee_lc else "")
        result_dict[result] = result_dict.get(result, 0) + 1
        #print("Attempt " + str(i) + ": " + result + " with " + str(remaining_pulls) + " remaining pulls")
    print("Success Rate: " + str(successes / attempts))
    print("Results:")
    for i in sorted(result_dict):
        print((i, result_dict[i]), end="\n")

def main():
    pull_sim(100000, 750, 7, 1, 8, 1, False, False, True)

if __name__ == '__main__':
    main()
                
                
        
