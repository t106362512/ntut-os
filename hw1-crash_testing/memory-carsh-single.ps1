function New-Top {
    param (
        [Parameter(Mandatory = $true)][string]$ProcessName,
        [Parameter(Mandatory = $false)][string]$DisplayFirst = 30
    )
    invoke-expression "cmd /c start powershell -Command {
        while (1) {
            ps -Name $ProcessName | select -first $DisplayFirst; sleep -seconds 1; cls; 
            ps -Name $ProcessName | measure | select Count;
            ps -Name $ProcessName | Group-Object -Property ProcessName | Format-Table Name, @{n='Mem (KB)';e={'{0:N0}' -f (($_.Group|Measure-Object WorkingSet64 -Sum).Sum / 1KB)};a='right'} -AutoSize
            write-host 'Handles  NPM(K)    PM(K)      WS(K) VM(M)   CPU(s)     Id ProcessName'; 
            write-host '-------  ------    -----      ----- -----   ------     -- -----------';
        }
    }"
}

function Start-MemoryTesting {
    param (
        [Parameter(Mandatory = $false)]$times = 5
    )
    $WindowCount = 0
    
    0..$times |% {
        Start-Sleep -Seconds 3
        $ProcessPath="C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        $Url="https://www.youtube.com/watch?v=idA90cwDG9Y?autoplay=1"
        Start-Process $ProcessPath -ArgumentList '--new-window', "--app=$Url"
        $WindowCount++
        Write-Host "Number of opened window: $WindowCount"
    }
}

# #====Main====#
try {
    # Disable-MMAgent -mc
    New-Top -ProcessName msedge
    Start-MemoryTesting -times 9999999
}
catch {
    Write-Error "PowerShell run failed on TIME: $((Get-Date).ToUniversalTime())"
    throw $_.Exception
}