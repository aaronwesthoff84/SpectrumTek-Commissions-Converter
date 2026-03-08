; SpectrumTek Commissions Converter - Inno Setup Script
; -----------------------------------------------------
; This script creates a Windows installer for the SpectrumTek Commissions Converter application.
;
; Prerequisites:
;   1. Build the directory version first: pyinstaller build/spectrumtek_installer.spec
;   2. Download Inno Setup from: https://jrsoftware.org/isinfo.php
;   3. Open this .iss file in Inno Setup Compiler and click Build
;
; The installer will be created in the 'Output' folder.

#define MyAppName "SpectrumTek Commissions Converter"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "SpectrumTek"
#define MyAppURL "https://www.spectrumtek.com"
#define MyAppExeName "SpectrumTek_Commissions_Converter.exe"
#define MyAppAssocName "SAP Commissions XML File"
#define MyAppAssocExt ".xml"
#define MyAppAssocKey StringChange(MyAppAssocName, " ", "") + MyAppAssocExt

; SpectrumTek brand colors (for reference in custom wizard pages if needed)
; Primary: #449877 (RGB: 68, 152, 119)
; Secondary: #062B33 (RGB: 6, 43, 51)

[Setup]
; Application identity
AppId={{A5B7C9D1-E3F5-4A7B-9C1D-3E5F7A9B1C3D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Installation directories
DefaultDirName={autopf}\{#MyAppPublisher}\{#MyAppName}
DefaultGroupName={#MyAppPublisher}
AllowNoIcons=yes

; Output settings
OutputDir=..\dist\installer
OutputBaseFilename=SpectrumTek_Commissions_Converter_Setup_{#MyAppVersion}

; Compression settings
Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes

; Installer appearance
WizardStyle=modern
; Uncomment and update these lines if you have custom images:
; WizardImageFile=..\assets\installer_banner.bmp
; WizardSmallImageFile=..\assets\installer_icon.bmp

; Privileges and compatibility
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; Icon (uncomment if you have an icon file)
; SetupIconFile=..\assets\icon.ico

; Uninstaller settings
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}

; Architecture
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; Misc
DisableProgramGroupPage=yes
LicenseFile=
InfoAfterFile=

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; Main application files from PyInstaller output
Source: "..\dist\SpectrumTek_Commissions_Converter\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\SpectrumTek_Commissions_Converter\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
; Start Menu shortcuts
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Comment: "Convert SAP Commissions XML to Excel"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

; Desktop shortcut (optional)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; Comment: "Convert SAP Commissions XML to Excel"

; Quick Launch shortcut (for older Windows versions)
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Registry]
; Associate .xml files with the application (optional - commented out as users may have other XML editors)
; Uncomment these lines if you want the app to be an option for opening XML files:
;
; Root: HKA; Subkey: "Software\Classes\{#MyAppAssocExt}\OpenWithProgids"; ValueType: string; ValueName: "{#MyAppAssocKey}"; ValueData: ""; Flags: uninsdeletevalue
; Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocName}"; Flags: uninsdeletekey
; Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"
; Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""
; Root: HKA; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes"; ValueType: string; ValueName: ".xml"; ValueData: ""

[Run]
; Option to launch app after installation
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
// Custom Pascal Script code for additional functionality

function InitializeSetup(): Boolean;
begin
  Result := True;
  // Add any pre-installation checks here
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Post-installation tasks can be added here
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    // Cleanup tasks after uninstallation
  end;
end;
