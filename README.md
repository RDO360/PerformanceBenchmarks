# Performance Benchmarks

## Encoding Speed Benchmark

Example usage :

```powershell
.\encodingSpeedBenchmark.ps1 -tiles "Rockets1.y4m", "Rockets2.y4m", "Rockets3.y4m", "Rockets4.y4m", "Rockets5.y4m", "Rockets6.y4m", "Rockets7.y4m", "Rockets8.y4m", "Rockets9.y4m", "Rockets10.y4m", "Rockets11.y4m", "Rockets12.y4m", "Rockets13.y4m", "Rockets14.y4m", "Rockets15.y4m", "Rockets16.y4m", "Rockets17.y4m", "Rockets18.y4m", "Rockets19.y4m", "Rockets20.y4m", "Rockets21.y4m", "Rockets22.y4m", "Rockets23.y4m", "Rockets24.y4m", "Rockets25.y4m", "Rockets26.y4m", "Rockets27.y4m", "Rockets28.y4m", "Rockets29.y4m", "Rockets30.y4m", "Rockets31.y4m", "Rockets32.y4m", "Rockets33.y4m", "Rockets34.y4m", "Rockets35.y4m", "Rockets36.y4m" -codecs "h264_nvenc", "hevc_nvenc" -efforts "p1", "p2", "p3", "p4", "p5", "p6", "p7" -cqs 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38 ,40 -heights 0, 320 -repetitions 5 -segmentTime 2 -segmentGOP 60 -segmentDirectory ".\segment" -dataFile data.csv
```