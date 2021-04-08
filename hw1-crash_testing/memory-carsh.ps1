$Throttle = 99999
$RunspacePool = [RunspaceFactory]::CreateRunspacePool(1, $Throttle)
$RunspacePool.Open()
$Jobs = @()
$URL = "https://www.youtube.com/watch?v=idA90cwDG9Y?autoplay=1"

$CoedBlock = {
    # param (
    #     [Parameter(Mandatory = $true)][string]$ProcessPath="C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    #     [Parameter(Mandatory = $true)][string]$Url="https://www.youtube.com/watch?v=idA90cwDG9Y?autoplay=1"
    # )

    $ProcessPath="C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    $Url="https://www.youtube.com/watch?v=idA90cwDG9Y?autoplay=1"
    Start-Process $ProcessPath -ArgumentList '--new-window', "--app=$Url"
}

function New-Top {
    param (
        [Parameter(Mandatory = $true)][string]$ProcessName,
        [Parameter(Mandatory = $false)][string]$DisplayFirst = 30
    )
    invoke-expression "cmd /c start powershell -Command {
        while (1) {
            ps -Name $ProcessName | select -first $DisplayFirst; sleep -seconds 1; cls; 
            ps -Name $ProcessName | measure | select Count;
            write-host 'Handles  NPM(K)    PM(K)      WS(K) VM(M)   CPU(s)     Id ProcessName'; 
            write-host '-------  ------    -----      ----- -----   ------     -- -----------';
        }
    }"
}

function Start-MemoryTesting {
    param (
        [Parameter(Mandatory = $true)]$URL,
        [Parameter(Mandatory = $false)]$times = 5
    )
    $WindowCount = 0
    $Browser = Start-Process $URL -PassThru 
    # Browser path issue.
    # $BrowserPath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    $Job = [powershell]::Create().AddScript($CoedBlock)
    $Job.RunspacePool = $RunspacePool
    
    0..$times | % {
        Start-Sleep -Seconds 0.1
        try {
            $Jobs += New-Object PSObject -Property @{
                Pipe   = $Job
                Result = $Job.BeginInvoke()
            }
        }
        catch {
            Start-Sleep -Seconds 6
            $Jobs += New-Object PSObject -Property @{
                Pipe   = $Job
                Result = $Job.BeginInvoke()
            }
        }
        $WindowCount++
        Write-Host "Number of opened window: $WindowCount"
    }
    
    Write-Host "Waiting.." -NoNewline
    Do {
        Write-Host "." -NoNewline
        Start-Sleep -Seconds 1
    } While ( $Jobs.Result.IsCompleted -contains $false)
    Write-Host "Jobs completed!"

    return $Jobs | % { $_.Pipe.EndInvoke($_.Result) }
}

# #====Main====#
try {
    New-Top -ProcessName msedge
    Start-MemoryTesting -URL $URL -times 99999

    Write-Information "PowerShell run success on TIME: $((Get-Date).ToUniversalTime())"
}
catch {
    Write-Error -Message $_.Exception
    Write-Error "PowerShell run failed on TIME: $((Get-Date).ToUniversalTime())"
    throw $_.Exception
}
finally {
    Write-Host -NoNewLine 'Press any key to exit...';
    # $RunspacePool.Dispose()
}