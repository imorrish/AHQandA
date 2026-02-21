# set the environment variable
# $env:BEARER_TOKEN = "your_bearer_token_here"
#
#get file ID from http://192.168.1.97:5175/flower/tasks
$fileid = "970d4583-2e18-445e-8cf7-37bc6e2075f2"

#Get file details from 

# Get yesterday's date in yyyymmdd format
$yesterday = (Get-Date).AddDays(-3).ToString("yyyyMMdd")

# Build the output filename
$contentDir = "e:\git\ahqanda\content"
if (-not (Test-Path $contentDir)) {
  New-Item -ItemType Directory -Path $contentDir | Out-Null
}

$outFile = "$contentDir\$yesterday.json"

# Call the API and save the JSON
# todo: get bearer from env variable or file
$bearerToken = $env:BEARER_TOKEN
#or from http://192.168.1.97:5174/api/auth/login

$fileDetails = Invoke-RestMethod `
  -Method GET `
  -Uri "http://192.168.1.97:5174/api/files/$fileid" `
  -Headers @{
    "accept" = "application/json"
    "Authorization" = "Bearer $bearerToken"
  } |
  ConvertTo-Json -Depth 2
 #$fileDetails -split "`n" | Select-Object -First 30
 ($fileDetails | ConvertFrom-Json).filename


$Summary =Invoke-RestMethod `
  -Method GET `
  -Uri "http://192.168.1.97:5174/api/files/$fileid/summary" `
  -Headers @{
    "accept" = "application/json"
    "Authorization" = "Bearer $bearerToken"
  } |
  ConvertTo-Json -Depth 50 |
  Out-File -Encoding utf8 $outFile