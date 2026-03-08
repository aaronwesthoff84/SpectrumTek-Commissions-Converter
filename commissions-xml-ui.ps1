<#
.SYNOPSIS
    Commissions XML Python Controller (UI).
.DESCRIPTION
    Provides Setup, Run, Ship, and Exit actions for the Python parser
    using the same compact WPF menu style as the existing UI scripts.
.NOTES
    Type: UI Script
#>

Add-Type -AssemblyName PresentationFramework
Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class ConsoleWindow {
    [DllImport("kernel32.dll")]
    public static extern IntPtr GetConsoleWindow();
    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}
"@

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$parseScriptPath = Join-Path $projectRoot 'parse_commissions_xml.py'
$requirementsPath = Join-Path $projectRoot 'requirements.txt'
$venvPythonPath = Join-Path $projectRoot '.venv\Scripts\python.exe'

function Hide-ConsoleWindow {
    $handle = [ConsoleWindow]::GetConsoleWindow()
    if ($handle -ne [IntPtr]::Zero) {
        [ConsoleWindow]::ShowWindow($handle, 0) | Out-Null
    }
}

function Show-ErrorBox {
    param([string]$Message, [string]$Title = 'Commissions XML Python')

    [System.Windows.MessageBox]::Show($Message, $Title, 'OK', 'Error') | Out-Null
}

function Show-InfoBox {
    param([string]$Message, [string]$Title = 'Commissions XML Python')

    [System.Windows.MessageBox]::Show($Message, $Title, 'OK', 'Information') | Out-Null
}

function Get-SystemPythonPath {
    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if ($null -eq $pythonCommand) {
        throw 'python was not found in PATH.'
    }

    return $pythonCommand.Source
}

function Get-PreferredPythonPath {
    if (Test-Path -LiteralPath $venvPythonPath) {
        return $venvPythonPath
    }

    return Get-SystemPythonPath
}

function Invoke-CapturedCommand {
    param(
        [Parameter(Mandatory = $true)][string]$FilePath,
        [string[]]$ArgumentList = @()
    )

    $previousLocation = Get-Location
    Set-Location -LiteralPath $projectRoot

    try {
        $output = & $FilePath @ArgumentList 2>&1 | Out-String
        $exitCode = $LASTEXITCODE
        if ($null -eq $exitCode) {
            $exitCode = 0
        }

        return [pscustomobject]@{
            ExitCode = $exitCode
            Output   = $output.Trim()
        }
    }
    finally {
        Set-Location -LiteralPath $previousLocation
    }
}

function New-BaseWindowXaml {
    param(
        [string]$Title,
        [double]$Height,
        [double]$Width,
        [string]$Body
    )

    return @"
<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="$Title" Height="$Height" Width="$Width"
        WindowStartupLocation="CenterScreen" ResizeMode="NoResize"
        Background="#F3F3F3">
    <Window.Resources>
        <Style TargetType="Button">
            <Setter Property="FontSize" Value="14"/>
            <Setter Property="FontWeight" Value="SemiBold"/>
            <Setter Property="Margin" Value="0,5,0,5"/>
            <Setter Property="Padding" Value="10"/>
            <Setter Property="Background" Value="White"/>
            <Setter Property="BorderBrush" Value="#CCCCCC"/>
            <Setter Property="BorderThickness" Value="1"/>
            <Setter Property="Cursor" Value="Hand"/>
        </Style>
        <Style TargetType="TextBox">
            <Setter Property="FontSize" Value="13"/>
            <Setter Property="Padding" Value="8"/>
            <Setter Property="BorderBrush" Value="#CCCCCC"/>
            <Setter Property="BorderThickness" Value="1"/>
            <Setter Property="Background" Value="White"/>
        </Style>
    </Window.Resources>
    <Border Padding="20">
$Body
    </Border>
</Window>
"@
}

function Show-MainMenu {
    [xml]$xaml = New-BaseWindowXaml -Title 'Commissions XML Python' -Height 355 -Width 320 -Body @"
        <StackPanel VerticalAlignment="Center">
            <TextBlock Text="Commissions XML Python"
                       FontSize="18"
                       FontWeight="Bold"
                       HorizontalAlignment="Center"
                       Margin="0,0,0,15"
                       Foreground="#333333"/>
            <Button x:Name="BtnSetup" Content="Setup" Height="45" IsDefault="True"/>
            <Button x:Name="BtnRun" Content="Run" Height="45"/>
            <Button x:Name="BtnShip" Content="Ship" Height="45"/>
            <Button x:Name="BtnExit" Content="Exit" Height="45"/>
        </StackPanel>
"@

    $reader = New-Object System.Xml.XmlNodeReader $xaml
    $window = [Windows.Markup.XamlReader]::Load($reader)
    $selection = $null

    $window.FindName('BtnSetup').Add_Click({ $script:selection = 'Setup'; $window.Close() })
    $window.FindName('BtnRun').Add_Click({ $script:selection = 'Run'; $window.Close() })
    $window.FindName('BtnShip').Add_Click({ $script:selection = 'Ship'; $window.Close() })
    $window.FindName('BtnExit').Add_Click({ $script:selection = 'Exit'; $window.Close() })

    $window.ShowDialog() | Out-Null
    return $selection
}

function Show-PostSetupMenu {
    [xml]$xaml = New-BaseWindowXaml -Title 'Commissions XML Python' -Height 255 -Width 320 -Body @"
        <StackPanel VerticalAlignment="Center">
            <TextBlock Text="Setup Complete"
                       FontSize="18"
                       FontWeight="Bold"
                       HorizontalAlignment="Center"
                       Margin="0,0,0,15"
                       Foreground="#333333"/>
            <Button x:Name="BtnRun" Content="Run" Height="45" IsDefault="True"/>
            <Button x:Name="BtnExit" Content="Exit" Height="45"/>
        </StackPanel>
"@

    $reader = New-Object System.Xml.XmlNodeReader $xaml
    $window = [Windows.Markup.XamlReader]::Load($reader)
    $selection = $null

    $window.FindName('BtnRun').Add_Click({ $script:selection = 'Run'; $window.Close() })
    $window.FindName('BtnExit').Add_Click({ $script:selection = 'Exit'; $window.Close() })

    $window.ShowDialog() | Out-Null
    return $selection
}

function Show-XmlInputWindow {
    [xml]$xaml = New-BaseWindowXaml -Title 'Commissions XML Python' -Height 265 -Width 520 -Body @"
        <StackPanel VerticalAlignment="Center">
            <TextBlock Text="Enter Full XML File Path"
                       FontSize="18"
                       FontWeight="Bold"
                       HorizontalAlignment="Center"
                       Margin="0,0,0,15"
                       Foreground="#333333"/>
            <TextBox x:Name="XmlPathText" Height="34" Margin="0,0,0,10"/>
            <StackPanel Orientation="Horizontal" HorizontalAlignment="Center">
                <Button x:Name="BtnBrowse" Content="Browse" Width="110" Margin="0,5,10,5"/>
                <Button x:Name="BtnRun" Content="Run" Width="110" Margin="0,5,10,5" IsDefault="True"/>
                <Button x:Name="BtnCancel" Content="Exit" Width="110" Margin="0,5,0,5"/>
            </StackPanel>
        </StackPanel>
"@

    $reader = New-Object System.Xml.XmlNodeReader $xaml
    $window = [Windows.Markup.XamlReader]::Load($reader)

    $xmlPathText = $window.FindName('XmlPathText')
    $selectedPath = $null

    $window.FindName('BtnBrowse').Add_Click({
        $dialog = New-Object System.Windows.Forms.OpenFileDialog
        $dialog.Filter = 'XML Files (*.xml)|*.xml|All Files (*.*)|*.*'
        $dialog.Title = 'Select SAP Commissions XML File'

        if ($dialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
            $xmlPathText.Text = $dialog.FileName
        }
    })

    $window.FindName('BtnRun').Add_Click({
        $candidate = $xmlPathText.Text.Trim()
        if ([string]::IsNullOrWhiteSpace($candidate)) {
            Show-ErrorBox -Message 'Enter the full path to an XML file.'
            return
        }

        if (-not (Test-Path -LiteralPath $candidate)) {
            Show-ErrorBox -Message "File not found: $candidate"
            return
        }

        $selectedPath = $candidate
        $window.Close()
    })

    $window.FindName('BtnCancel').Add_Click({
        $selectedPath = $null
        $window.Close()
    })

    $window.ShowDialog() | Out-Null
    return $selectedPath
}

function Get-OutputWorkbookPath {
    param([Parameter(Mandatory = $true)][string]$XmlPath)

    $generatedDir = Join-Path $projectRoot 'generated'
    if (-not (Test-Path -LiteralPath $generatedDir)) {
        New-Item -ItemType Directory -Path $generatedDir -Force | Out-Null
    }

    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($XmlPath)
    $cleanName = $baseName -replace '([_\-\s]?Plan)$', ''
    if ([string]::IsNullOrWhiteSpace($cleanName)) {
        $cleanName = $baseName
    }

    return Join-Path $generatedDir ($cleanName + '_parsed_plan.xlsx')
}

function Invoke-Setup {
    try {
        $systemPythonPath = Get-SystemPythonPath
    }
    catch {
        Show-ErrorBox -Message $_.Exception.Message -Title 'Setup Failed'
        return $false
    }

    $venvResult = Invoke-CapturedCommand -FilePath $systemPythonPath -ArgumentList @('-m', 'venv', '.venv')
    if ($venvResult.ExitCode -ne 0) {
        Show-ErrorBox -Title 'Setup Failed' -Message ("Unable to create .venv.`r`n`r`n{0}" -f $venvResult.Output)
        return $false
    }

    $pipResult = Invoke-CapturedCommand -FilePath $venvPythonPath -ArgumentList @('-m', 'pip', 'install', '-r', 'requirements.txt')
    if ($pipResult.ExitCode -ne 0) {
        Show-ErrorBox -Title 'Setup Failed' -Message ("Dependency install failed.`r`n`r`n{0}" -f $pipResult.Output)
        return $false
    }

    Show-InfoBox -Title 'Setup Complete' -Message 'Setup completed successfully.'
    return $true
}

function Invoke-Run {
    param([Parameter(Mandatory = $true)][string]$XmlPath)

    try {
        $pythonPath = Get-PreferredPythonPath
    }
    catch {
        Show-ErrorBox -Title 'Run Failed' -Message $_.Exception.Message
        return $false
    }

    $outputWorkbookPath = Get-OutputWorkbookPath -XmlPath $XmlPath
    $result = Invoke-CapturedCommand -FilePath $pythonPath -ArgumentList @($parseScriptPath, $XmlPath, '-o', $outputWorkbookPath)

    if ($result.ExitCode -ne 0) {
        Show-ErrorBox -Title 'Run Failed' -Message ("Parser execution failed.`r`n`r`n{0}" -f $result.Output)
        return $false
    }

    Show-InfoBox -Title 'Run Complete' -Message ("Workbook created:`r`n{0}" -f $outputWorkbookPath)
    return $true
}

function Invoke-Ship {
    $folderName = Split-Path -Leaf $projectRoot
    $parent = Split-Path -Parent $projectRoot
    $match = [regex]::Match($folderName, '^(?<base>.+)_V(?<version>\d+)$')

    if (-not $match.Success) {
        Show-ErrorBox -Title 'Ship Failed' -Message "Current folder name does not match the expected version pattern: $folderName"
        return $false
    }

    $baseName = $match.Groups['base'].Value
    $currentVersion = [int]$match.Groups['version'].Value
    $nextVersion = $currentVersion + 1

    do {
        $targetName = '{0}_V{1}' -f $baseName, $nextVersion
        $targetRoot = Join-Path $parent $targetName
        $nextVersion++
    } while (Test-Path -LiteralPath $targetRoot)

    $shipItems = @(
        '.gitignore',
        'commissions-xml-ui.ps1',
        'Example_Plan_For_Testing_D_B.xlsx',
        'parse_commissions_xml.py',
        'README.md',
        'requirements.txt',
        'sap_commissions_xml'
    )

    try {
        New-Item -ItemType Directory -Path $targetRoot -Force | Out-Null

        foreach ($item in $shipItems) {
            $sourcePath = Join-Path $projectRoot $item
            if (-not (Test-Path -LiteralPath $sourcePath)) {
                throw "Required ship item not found: $sourcePath"
            }

            $destinationPath = Join-Path $targetRoot $item
            Copy-Item -LiteralPath $sourcePath -Destination $destinationPath -Recurse -Force
        }
    }
    catch {
        Show-ErrorBox -Title 'Ship Failed' -Message $_.Exception.Message
        return $false
    }

    Show-InfoBox -Title 'Ship Complete' -Message ("Created clean ship folder:`r`n{0}" -f $targetRoot)
    return $true
}

Hide-ConsoleWindow

foreach ($requiredPath in @($parseScriptPath, $requirementsPath)) {
    if (-not (Test-Path -LiteralPath $requiredPath)) {
        Show-ErrorBox -Title 'Missing Project File' -Message "Required file not found: $requiredPath"
        exit 1
    }
}

$mainSelection = Show-MainMenu

switch ($mainSelection) {
    'Setup' {
        if (Invoke-Setup) {
            $postSetupSelection = Show-PostSetupMenu
            if ($postSetupSelection -eq 'Run') {
                $xmlPath = Show-XmlInputWindow
                if ($xmlPath) {
                    Invoke-Run -XmlPath $xmlPath | Out-Null
                }
            }
        }
    }
    'Run' {
        $xmlPath = Show-XmlInputWindow
        if ($xmlPath) {
            Invoke-Run -XmlPath $xmlPath | Out-Null
        }
    }
    'Ship' {
        Invoke-Ship | Out-Null
    }
    default {
    }
}
