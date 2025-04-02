import numpy

def bdRate(bitrate_original:list[float], psnr_original:list[float], bitrate_compared:list[float], psnr_compared:list[float]) -> float:
    lR1 = numpy.log(bitrate_original)
    lR2 = numpy.log(bitrate_compared)

    # rate method
    p1 = numpy.polyfit(psnr_original, lR1, 3)
    p2 = numpy.polyfit(psnr_compared, lR2, 3)

    # integration interval
    min_int = max(min(psnr_original), min(psnr_compared))
    max_int = min(max(psnr_original), max(psnr_compared))

    # find integral
    p_int1 = numpy.polyint(p1)
    p_int2 = numpy.polyint(p2)

    int1 = numpy.polyval(p_int1, max_int) - numpy.polyval(p_int1, min_int)
    int2 = numpy.polyval(p_int2, max_int) - numpy.polyval(p_int2, min_int)

    # find avg diff
    avg_exp_diff = (int2 - int1) / (max_int - min_int)
    avg_diff = (numpy.exp(avg_exp_diff) - 1) * 100
    
    return avg_diff
