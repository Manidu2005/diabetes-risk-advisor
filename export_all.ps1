$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open("c:\Users\USER\Downloads\Programs\AI project\Diabetes_AI_Presentation.pptx")
$slidesToCheck = @(2, 3, 5, 6, 7, 9, 10, 11, 12)
foreach ($num in $slidesToCheck) {
    $pres.Slides.Item($num).Export("c:\Users\USER\Downloads\Programs\AI project\slide${num}_preview.png", "PNG", 960, 540)
}
$pres.Close()
$ppt.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null
Write-Output "All requested slides exported"
