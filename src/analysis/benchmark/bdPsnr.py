import numpy

def bdPsnr(bitrate_original:list[float], psnr_original:list[float], bitrate_compared:list[float], psnr_compared:list[float]) -> float:
    lR1 = numpy.log(bitrate_original)
    lR2 = numpy.log(bitrate_compared)

    psnr_original = numpy.array(psnr_original)
    psnr_compared = numpy.array(psnr_compared)

    p1 = numpy.polyfit(lR1, psnr_original, 3)
    p2 = numpy.polyfit(lR2, psnr_compared, 3)

    # integration interval
    min_int = max(min(lR1), min(lR2))
    max_int = min(max(lR1), max(lR2))

    # find integral
    p_int1 = numpy.polyint(p1)
    p_int2 = numpy.polyint(p2)

    int1 = numpy.polyval(p_int1, max_int) - numpy.polyval(p_int1, min_int)
    int2 = numpy.polyval(p_int2, max_int) - numpy.polyval(p_int2, min_int)

    # find avg diff
    avg_diff = (int2 - int1) / (max_int - min_int)

    return avg_diff
