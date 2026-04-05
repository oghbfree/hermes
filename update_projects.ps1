 = Get-Content 'C:\OpenClaw\.openclaw\workspace\memory\projects.md'
 = @()
foreach ( in ) {
    if ( -match 'Akoma Robotics') {
         +=  -replace 'STEM education, school pilots, content automation', 'STEM education, school pilots, content automation, John''s Facebook ads initiative'
    } else {
         += 
    }
}
Set-Content -Path 'C:\OpenClaw\.openclaw\workspace\memory\projects.md' -Value 
