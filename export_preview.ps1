$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open("c:\Users\USER\Downloads\Programs\AI project\Diabetes_AI_Presentation.pptx")
$pres.Slides.Item(1).Export("c:\Users\USER\Downloads\Programs\AI project\slide1_preview.png", "PNG", 960, 540)
$pres.Slides.Item(4).Export("c:\Users\USER\Downloads\Programs\AI project\slide4_preview.png", "PNG", 960, 540)
$pres.Slides.Item(8).Export("c:\Users\USER\Downloads\Programs\AI project\slide8_preview.png", "PNG", 960, 540)
$pres.Close()
$ppt.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null
Write-Output "Previews exported successfully"
