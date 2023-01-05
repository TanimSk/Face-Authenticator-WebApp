def sec_to_hm(sec) -> str:
    delay_hr = int(abs(sec))
    delay_mins = int((abs(sec) - delay_hr)*60)
    return f"{delay_hr} hr {delay_mins} mins" 
